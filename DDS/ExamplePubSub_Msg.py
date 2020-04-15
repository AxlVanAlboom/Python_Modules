import clsDDS
import time
import random

userID = 0

def NewDataAvailable(sTopic,sUserId, sMessage):
    # Own data get's also captured and read! 
    # --> don't show it
    if int(sUserId) == userID:
        return

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
    oDds.AddTopic(sTopic)
    oDds.AddSubscriber(sTopic)

    userID = random.randrange(1, 64535)

    while True:
        
        message = input()
        oDds.Publish(sTopic,userID,message)
        


    