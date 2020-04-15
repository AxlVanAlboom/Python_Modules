import clsDDS
import time
import random

if __name__ == "__main__":

    sTopic = 'HelloWorldData_Msg'

    oDds = clsDDS.clsDdsMsg()
    oDds.AddTopic(sTopic)
    oDds.AddSubscriber(sTopic)

    userID = random.randrange(1, 64535)

    i=0
    while i<100:
        message = "This is message: " +str(i)
        oDds.Publish(sTopic,userID, message)

        print(str(i))
        i = i+1
        time.sleep(2)

