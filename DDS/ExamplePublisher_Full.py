import clsDDS
import time

if __name__ == "__main__":

    oDds = clsDDS.clsDds('file://DDS_DefaultQoS_All.xml', 'DDS DefaultQosProfile','DataStructs_Msg.idl')

    oDds.AddTopic('HelloWorldData_Msg','DataStructs::Msg')
    oDds.AddPublisher()
    
    i=0
    while i<100:

        Msg = oDds.GetDataClass("DataStructs::Msg")
        oData =  Msg(userID = 1, message = "This is message: " +str(i))

        oDds.Publish('HelloWorldData_Msg',oData)

        print(str(i))
        i = i+1
        time.sleep(2)


