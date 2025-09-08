import socket
import os
import machine
import time
import sys

class PyCodeUpdater():
    portNumber = 9999
    _listenSocket = None
    _acceptedSocket = None
    
    def receiveDataFromServer3sec(self, socketClient, bytesCount):
        try:
            # oldTimeout = socketClient.gettimeout()
            socketClient.settimeout(3) # 3 seconds
            tmp = socketClient.recv(bytesCount)
            # socketClient.settimeout(oldTimeout)
            return tmp
        except:
            return ""
            
    def receiveDataFromServer3secAll(self, socketClient, bytesCount):
        ret = self.receiveDataFromServer3sec(socketClient, 1)
        if (len(ret) != 1):
            return ""
        bytesCount -= 1;    
        while(bytesCount > 0):
            tmp = self.receiveDataFromServer3sec(socketClient, bytesCount)
            if (len(tmp) == 0):
                return ""
            bytesCount = bytesCount - len(tmp);
            ret += tmp
            
        return ret
    
    def sendDataToServer(self, socketClient, data):
        socketClient.sendall(data);
        
    
    def updatesFiles(self, clientConnection) -> bool :
        print("updatesFiles")
        buf = self.receiveDataFromServer3sec(clientConnection, 1)
        if (len(buf) != 1) :
            print("PyCodeUpdater: can't read files count")
            return False
        filesCount = buf[0]
            
        print("Files count to update: ", filesCount)    
        for i in range(filesCount):
            buf = self.receiveDataFromServer3secAll(clientConnection, 3)
            if (len(buf) != 3) :
                print("PyCodeUpdater: can't read file name and file sizes")
                return False
            fileNameLen = buf[0]
            fileLen = buf[1] * 256 + buf[2]
    
            buf = self.receiveDataFromServer3secAll(clientConnection, fileNameLen)
            if (len(buf) != fileNameLen):
                print("PyCodeUpdater: can't read file name")
                return False
            fileName = buf;
            
            if (fileLen == 0):
                print("Delete file: ", fileName)
                os.remove(fileName)
                continue
                
            print("Updating file: ", fileName)
            
            buf = self.receiveDataFromServer3secAll(clientConnection, fileLen)
            if (len(buf) != fileLen):
                print("PyCodeUpdater: can't read file")
                return False
                
            with open(fileName.decode("utf-8"), "wb") as f:
                f.write(buf)
                f.close()
                
            
        return True
            

    def deleteFiles(self, clientConnection) -> bool :
        print("deleteFiles")
        buf = self.receiveDataFromServer3sec(clientConnection, 1)
        if (len(buf) != 1) :
            print("PyCodeUpdater: can't read files count")
            return False
        filesCount = buf[0]
            
        print("Files count to delete: ", filesCount)    
        for i in range(filesCount):
            buf = self.receiveDataFromServer3secAll(clientConnection, 1)
            if (len(buf) != 1) :
                print("PyCodeUpdater: can't read size of file name")
                return False
            fileNameLen = buf[0]
                        
            buf = self.receiveDataFromServer3secAll(clientConnection, fileNameLen)
            if (len(buf) != fileNameLen):
                print("PyCodeUpdater: can't read file name")
                return False
            fileName = buf;
            print("Delete file: ", fileName)
            os.remove(fileName.decode("utf-8"))
                  
        return True
        
    def listFiles(self, clientConnection) -> bool :
        print("listFiles")
        answer = bytearray()
        count = 0;
        for filename in os.listdir():
            #if not os.path.isfile(filename):
            #    continue;
            print(filename)
            file_len = len(filename)
            answer.append(file_len)
            answer = answer + bytes(filename, "utf-8")
            count = count + 1
        answer2 = bytearray()
        dataLen = len(answer) + 1 # 1 byte count of files
        v = int(dataLen / 256)
        answer2.append(v)
        v = dataLen - v * 256
        answer2.append(v)
        answer2.append(count)
        answer2 = answer2 + answer
        self.sendDataToServer(clientConnection, answer2)
        return True
        
    def getFile(self, clientConnection) -> bool :
        print("getFile\n")
        buf = self.receiveDataFromServer3secAll(clientConnection, 1)
        if (len(buf) == 0) :
            return False
        nameSize = buf[0]
        buf = self.receiveDataFromServer3secAll(clientConnection, nameSize)
        if (len(buf) != nameSize) :
            return False
        fileName = buf;
        print("getFile: ", fileName)
        with open(fileName.decode("utf-8"), "rb") as f:
            buf = f.read()
            f.close()
        
        dataLen = len(buf)
        answer = bytearray()
        v = int(dataLen / 256)
        answer.append(v)
        v = dataLen - v * 256
        answer.append(v)
        answer = answer + buf
        self.sendDataToServer(clientConnection, answer)
        return True
    
    def run(self) -> bool:
        if (self._listenSocket == None):
            self._listenSocket = socket.socket();
            self._listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._listenSocket.bind(('0.0.0.0', self.portNumber))
            self._listenSocket.settimeout(0.2)
            self._listenSocket.listen();
        
        if (self._listenSocket != None):
            clientConnection = None        
            try:        
                (clientConnection, clientAddress) = self._listenSocket.accept()
            except:
                return True
                
            print("New client to update program")    
            
            buf = self.receiveDataFromServer3secAll(clientConnection, 1)
            ret = False
            if (len(buf) == 1) :
                print("len(buf) == 1 ", buf[0])
                if (buf[0] == 85) : # 'U'
                    ret = self.updatesFiles(clientConnection)
                    if (ret):
                        clientConnection.sendall("1")
                    else:
                        clientConnection.sendall("0")
                elif (buf[0] == 68) : # 'D'
                    ret = self.deleteFiles(clientConnection)
                    if (ret):
                        clientConnection.sendall("1")
                    else:
                        clientConnection.sendall("0")
                elif (buf[0] == 76) : # 'L'
                    self.listFiles(clientConnection)
                elif (buf[0] == 71) : # 'G'
                    self.getFile(clientConnection)
                elif (buf[0] == 69) : # 'E'
                    print("Exit Script")
                    ret = True
                    if (ret):
                        clientConnection.sendall("1")
                    else:
                        clientConnection.sendall("0")
                # TODO: other operations
            
            clientConnection.close()
            if (buf[0] == 85) :
                time.sleep(1)
                machine.reset()
            elif (buf[0] == 69) : # 'E'
                time.sleep(1)
                sys.exit()
            
        return True
                
