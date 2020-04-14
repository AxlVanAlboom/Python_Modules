##############################################################################################################
# Made by engineer Axl Van Alboom working for Ghent University
#
# if encoding is none, the data send and received needs to be bytes
# when given an encoding type, this type will be use to encode/decode the message
#
##############################################################################################################

import socket
import select
from threading import Thread, Lock

class Event:
    def __init__(self):
        self.handlers = set()

    def handle(self, handler):
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        return len(self.handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount

class clsTcpClient:
    def __init__(self, sIp, iPort, sEncoding=None):  
        # if encoding is none, the data send and received needs to be bytes
        # when given an encoding type, this type will be use to encode/decode the message
        self.__sIP = sIp
        self.__iPort = iPort
        self.__sEncoding = sEncoding        
        self.DataReceived = Event()

    def Connect(self):
        oClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            oClient.connect((self.__sIP,self.__iPort))
            self.__oClient = oClient 
            Thread(target = self.__receiveData).start()
        except:         
            self.__oClient = None
            raise Exception("No connection available, server not running?")

    def Disconnect(self):  
        if self.__oClient != None:      
            self.__xReceiveData =False
            self.__oClient.shutdown(1)
            self.__oClient.close()
            self.__oClient = None

    def SendData(self, oData):
        if self.__oClient != None: 
            if self.__sEncoding != None:
                    if isinstance(oData, str):
                        oData = oData.encode(self.__sEncoding)
                    else:                   
                        raise Exception("Wrong data type")
            elif not isinstance(oData,bytes):  
                    raise Exception("Wrong data type")    

            self.__oClient.send(oData)

        else:
            raise Exception("No connection available")

    def __receiveData(self):
        self.__xReceiveData =True
        while self.__xReceiveData:
            #data available? --> select
            r, _, _ = select.select([self.__oClient], [], [])
            if r and self.__oClient != None:
                iBufferSize = 1024
                data = self.__oClient.recv(iBufferSize)   
                if data: 
                    if self.__sEncoding != None:
                        data = data.decode(self.__sEncoding)

                    self.DataReceived(data) 
                else:
                    self.__xReceiveData =False
                    print("Server closed the conenction")
                    break

class clsTcpServer:
    def __init__(self, sIp, iPort, sEncoding = None):
        
        self.__sIP = sIp
        self.__iPort = iPort       
        self.__sEncoding = sEncoding

        # events
        self.NewClient = Event()
        self.DataReceived = Event()
        self.ClientDisconnected = Event()

        #thread lock
        self.__oLockServer = Lock()

    def StartServer(self):
        Thread(target = self.__startServer).start()  
    def __startServer(self):
        self.__oServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.__sIP,self.__iPort)
        print('starting up on %s, port %s' % server_address)

        self.__oServer.bind(server_address)

        # client dictionary
        self.__oClientDictionary= {}

        # receive data from clients
        self.__xReceiveData = True

        # Listen for incoming connections
        self.__oServer.listen(1)
        while self.__oServer != None:

            r, _ , _ = select.select([self.__oServer], [], [])
            
            self.__oLockServer.acquire()

            if r and self.__oServer != None:
                oClient, oClientAddress = self.__oServer.accept()          
                oLockClient = Lock()

                oConnector = clsTcpConnector(oClientAddress,oClient,oLockClient)

                self.__oClientDictionary[oClientAddress] = oConnector
                self.NewClient(oClientAddress)
                Thread(target = self.__clientReceiveData,args=(oConnector,)).start()
                
            self.__oLockServer.release()
    
    def StopServer(self):
        self.__oLockServer.acquire()

        self.__oServer.close()
        self.__oServer = None

        self.__oLockServer.release()

    def StopServerAndDisconnectAllClients(self):      
        self.__xReceiveData =False
        self.StopServer()
               
        for oClientAddress in self.__oClientDictionary:
            oConnector = self.__oClientDictionary[oClientAddress]
            oLock = oConnector.getLock()
            oLock.acquire()

            oClient = oConnector.getClient()
            if oClient != None:        
                oClient.shutdown(1)
                oClient.close()
                oClient = None 
                self.ClientDisconnected(oClientAddress)

            oConnector.setClient(oClient)
            oLock.release()

        self.__oClientDictionary = None
   
    def __clientReceiveData(self, oConnector):    
        oClientAddress = oConnector.getClientAddress()
        oClient = oConnector.getClient()
        oLock = oConnector.getLock()

        while self.__xReceiveData:
     
            #data available? --> select
            r, _, _ = select.select([oClient], [], [])
          
            oLock.acquire()

            if r and oClient != None and not oClient._closed:

                iBufferSize = 1024
                data = oClient.recv(iBufferSize)   
                if data: 
                    if self.__sEncoding != None:
                        data = data.decode(self.__sEncoding)

                    self.DataReceived(oClientAddress,data) 
                else:
                    self.ClientDisconnected(oClientAddress)
                    self.__oClientDictionary.pop(oClientAddress)
                    oClient = None
                    oClientAddress = None
                    oConnector = None
                    break 
            
            oLock.release()

    def SendData(self, oClientAddress ,oData):
        if self.__oServer == None:
            raise Exception("The server is not started yet!")

        if oClientAddress != None:
            oConnector = self.__oClientDictionary[oClientAddress]
            oClient = oConnector.getClient()
            if oClient != None:

                if self.__sEncoding != None:
                    if isinstance(oData, str):
                        oData = oData.encode(self.__sEncoding)
                    else:                   
                        raise Exception("Wrong data type")
                elif not isinstance(oData,bytes):  
                    raise Exception("Wrong data type")          

                oClient.sendall(oData)

            else:
                print("No Connection available")
        else:
            print("This adress doesn't exist")

class clsTcpConnector:
    def __init__(self, oClientAddress,oClient,oLock):
        self.__oClientAddress = oClientAddress
        self.__oClient = oClient
        self.__oLock = oLock

    def getClient(self):
        return self.__oClient
    def getLock(self):
        return self.__oLock
    def getClientAddress(self):
        return self.__oClientAddress
    
    def setClient(self,oClient):
        self.__oClient=oClient