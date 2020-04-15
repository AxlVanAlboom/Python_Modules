import clsDDS
import time

def NewDataAvailable(sTopic,oData):
    print("-------------------------")
    print("New data")
    print("Topic: "+ sTopic)
    print("Data: "+ str(oData))
    print("-------------------------")

if __name__ == "__main__":

    sTopic = 'HelloWorldData_Msg'

    oDds = clsDDS.clsDds('file://DDS_DefaultQoS_All.xml', 'DDS DefaultQosProfile','DataStructs_Msg.idl')
    
    oDds.DataReceived += NewDataAvailable
    
    oDds.AddTopic('HelloWorldData_Msg','DataStructs::Msg')
    oDds.AddSubscriber(sTopic)
