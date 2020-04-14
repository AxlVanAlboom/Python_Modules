import time
from TcpIp import clsTcpServer

List = []

def ReceiveData(oClientAddress,data):
    print(oClientAddress)
    print(data)

def NewClient(s):
    List.append(s)
    print('connection from',s)

def ClientDisconnected(s):
    List.remove(s)
    print('The following client disconnected:', s)

sIp = "localhost"
iPort = 1

VbMessage = "Hallo, ik ben Axl. Aangename kennismaking! :-)"
VbBytes = b'Hallo, ik ben Axl. Aangename kennismaking! :-)'


oTcpServer = clsTcpServer(sIp,iPort)
#oTcpServer = TcpIp.clsTcpServer(sIp,iPort, 'utf-8')
oTcpServer.DataReceived += ReceiveData
oTcpServer.NewClient += NewClient
oTcpServer.ClientDisconnected += ClientDisconnected

oTcpServer.StartServer()

time.sleep(5)
oTcpServer.SendData(List[0],VbBytes) # make sure something is connected in 5 seconds
#oTcpServer.SendData(List[0],VbMessage)


input()

#oTcpServer.StopServer()
oTcpServer.StopServerAndDisconnectAllClients()

input()