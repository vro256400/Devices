import socket
import time
from srv_discovery import getPwServer

class Pwio():
    deviceType = None
    port = 7777
    login = None
    passwd = None
    socketClient = None
    lastComm = None
    justConnected = False
    _PROTOCOLNAMELOG = "Log"
    _PROTOCOLNAMESETTINGS = "Settings"
    
    _recvMsgLen = -1
    _recvBuf = [] 
    
    def __send(self, msg):
        if self.socketClient != None :
            try:
                self.socketClient.settimeout(1)
                self.socketClient.sendall(msg)
                self.socketClient.settimeout(None)
                self.lastComm  = time.time(); 
            except:
                print("Send error - close socket")
                self.socketClient.close()
                self.socketClient = None
                self.justConnected = False    
                
    def __receiveDataFromServer1sec(self, bytesCount):
        try:
            # oldTimeout = socketClient.gettimeout()
            self.socketClient.settimeout(1) # 1 seconds
            tmp = self.socketClient.recv(bytesCount)
            # socketClient.settimeout(oldTimeout)
            if (tmp != None) :
                self.lastComm  = time.time(); 
            return tmp
        except OSError as e:
            if (errno.ETIMEDOUT == e.errno) :
                return None
            print("Receive error - close socket ", e)
            self.socketClient.close()
            self.socketClient = None
            self.justConnected = False   
            return None
            
    def __sendMsg(self, msg):
        value = len(msg)
        two_byte_array = bytearray([value // 256, value % 256])
        self.__send(two_byte_array)
        self.__send(msg) 
        
    def __recvMsg(self) :
        # idea do not read from socket more data than need for the one message
        if (self._recvMsgLen == -1) :
            newData = self.__receiveDataFromServer1sec(2 - len(self._recvBuf))
            if (newData == None):
                return None
            self._recvBuf += newData
            newData = None
            if (len(self._recvBuf) < 2):
                return None
            self._recvMsgLen = ((int)(self._recvBuf[0])) * 256 + (int)(self._recvBuf[1])
            del self._recvBuf[0:2]
        if (self._recvMsgLen > len(self._recvBuf)):
            newData = self.__receiveDataFromServer1sec(self._recvMsgLen - len(self._recvBuf))
            if (newData == None):
                return None
            self._recvBuf += newData
            newData = None

        if (self._recvMsgLen <= len(self._recvBuf)):
            msg = ""
            for i in range(0, self._recvMsgLen):
                msg += chr(self._recvBuf[i])
            del self._recvBuf[0:self._recvMsgLen]
            self._recvMsgLen = -1
            return msg
        return None
        
                
    #def __sendLogMsg(self, msg):
    #    self.__sendMsg(self._PROTOCOLNAMELOG + "\t" + msg)

    def __log(self, logType, *args):
        msg = "Log:" + logType + ":"
        for a in args:
            msg = msg + str(a)
        print(msg) # to log in console
        self.__sendMsg(msg)

    def logError(self, *args):
        self.__log("Error", *args)
    
    def logInfo(self, *args):
        self.__log("Info", *args)
        
    def logWarning(self, *args):
        self.__log("Warning", *args)

    def __receiveProtocolsData(self):
        msg = self.__recvMsg()
        if (msg == None):
            return
        if (msg.startswith("gset")) :
            content = self.onGetSettings()
            msg = "Sts:" + content
            self.__sendMsg(msg)
        elif (msg.startswith("pset")) :
            content = msg[4:]
            #print(content)
            self.onNewSettings(content) 
        elif (msg.startswith("ping")) :
            print("ping")
     
    def connect(self):
        if self.socketClient == None:
            self.logInfo("Server discovery")
            ip = getPwServer()
            if ip == None :
                self.logInfo("Can't detect server")
                return
            self.logInfo("Connect PW")
            self.socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socketClient.settimeout(1)
                self.socketClient.connect((self.ip, self.port))
                self.socketClient.settimeout(None)
                self.justConnected = True
                answer = "PW\t" + self.deviceType
                l = len(answer)
                for i in range(l, 48):
                    answer += "\t"
                self.__send(answer)
                self.__sendMsg(self.login) #instead of handshake for now
            except:
                self.socketClient.close()
                self.socketClient = None
                self.logInfo("Connect PW fail")
            
    def isJustConnected(self):
        jc = self.justConnected
        self.justConnected = False
        return jc
        
    def run(self) -> bool:
        self.connect()
        if (self.isJustConnected()):
            self.lastComm  = time.time()
            self.logInfo("pwio: just connected - send variables info")
        
        if self.socketClient == None:
            return True
        
        self.__receiveProtocolsData()
        curTime = time.time()
        if (curTime - self.lastComm  > 3) : # > 3 sec
            self.__sendMsg("ping")

        return True
    
    def onGetSettings(self):
        return None
    
    def onNewSettings(self, content):
        return