import TcpIp

def ReceiveData(s):
    print(s)

sIp = "localhost"
iPort = 1

VbBytes = b'Hallo, ik ben Axl. Aangename kennismaking! :-)'
VbMessage = "Hallo, ik ben Axl. Aangename kennismaking! :-)"

# no encoding --> need to send bytes
# encoding --> send string

oTcpClient = TcpIp.clsTcpClient(sIp,iPort)
#oTcpClient = TcpIp.clsTcpClient(sIp,iPort,'utf-16')

oTcpClient.DataReceived += ReceiveData

oTcpClient.Connect()

oTcpClient.SendData(VbBytes)
#oTcpClient.SendData(VbMessage)

input()
oTcpClient.Disconnect()