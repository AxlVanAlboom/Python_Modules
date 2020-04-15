import clsDDS
import time

def NewDataAvailable(sTopic,sUserId, sMessage):
    print("-------------------------")
    print("New data")
    print("Topic: "+ sTopic)
    print("User id: "+ str(sUserId))
    print("Message: "+ sMessage)
    print("-------------------------")

if __name__ == "__main__":

    sTopic = 'HelloWorldData_Msg'

    oDds = clsDDS.clsDdsMsg()
    
    oDds.DataReceived += NewDataAvailable
    
    oDds.AddTopic('HelloWorldData_Msg')
    oDds.AddSubscriber(sTopic)
