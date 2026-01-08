import socket
import time
from srv_discovery import getPwServer
import errno

class Pwio():
    deviceType = None
    ip = None
    port = 7777
    login = None
    passwd = None
    socketClient = None
    lastSend = None
    lastReceive = None
    
    _recvMsgLen = -1
    _recvBuf = [] 
    
    def __send(self, msg):
        if self.socketClient != None :
            try:
                self.socketClient.settimeout(1)
                self.socketClient.sendall(msg)
                self.socketClient.settimeout(None)
                self.lastSend  = time.time(); 
            except:
                print("Pwio: Send error - close socket")
                self.socketClient.close()
                self.socketClient = None

                
    def __receiveDataFromServer1sec(self, bytesCount):
        if self.socketClient == None :
            return None
        try:
            # oldTimeout = socketClient.gettimeout()
            self.socketClient.settimeout(1) # 1 seconds
            tmp = self.socketClient.recv(bytesCount)
            # socketClient.settimeout(oldTimeout)
            if (tmp != None) :
                self.lastReceive  = time.time(); 
            return tmp
        except OSError as e:
            if (errno.ETIMEDOUT == e.errno) :
                return None
            print("Pwio: Receive error - close socket ", e)
            self.socketClient.close()
            self.socketClient = None
            return None
        except Exception as e:
            print("Pwio: Receive error - close socket ", e)
            self.socketClient.close()
            self.socketClient = None
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
        elif (msg.startswith("ginp")) :
            content = self.onGetInputsVar()
            print("Content:  ", content)
            msg = "Sti:" + content
            self.__sendMsg(msg)

    def connect(self):
        if self.socketClient == None:
            if (self.ip == None):
                self.ip = getPwServer()
                            
            if self.ip == None :
                self.logInfo("Can't detect server")
                return False
            self.logInfo("Connect PW " + self.ip + ":" + str(self.port))
            self.socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socketClient.settimeout(1)
                self.socketClient.connect((self.ip, self.port))
                self.socketClient.settimeout(None)
            except Exception as e:
                self.socketClient.close()
                self.socketClient = None
                self.logInfo("Connect PW fail ", e)
                return False
            
            try:
                answer = "PW\t" + self.deviceType
                l = len(answer)
                for i in range(l, 48):
                    answer += "\t"
                self.__send(answer)
                self.__sendMsg(self.login) #instead of handshake for now
            except Exception as e:
                self.socketClient.close()
                self.socketClient = None
                self.logInfo("Connect PW fail(send initial data) ", e)
                return False
            
            # just connected
            self.lastSend = time.time()
            self.lastReceive = self.lastSend
            self.logInfo("pwio: just connected")

        return True    
        
    def run(self) -> bool:
        if not self.connect():
            return
                       
        self.__receiveProtocolsData()
        curTime = time.time()
        if (curTime - self.lastSend  > 3) : # > 3 sec
            self.__sendMsg("ping")
        if (curTime - self.lastReceive > 10):
            self.socketClient.close()
            self.socketClient = None
            self.logInfo("Comm error")

        return True
    
    def onGetSettings(self):
        return None
    
    def onGetInputsVar(self):
        return None

    def onNewSettings(self, content):
        return
    
    