import dds
from dds import *
import ddsutil
from threading import Thread
from Event import Event

# important!
# dds without condition
# once the condition is met --> all the data is taken --> !!! solve this !!!

class clsDds():
    def __init__(self,sQualityOfServiceFile, sQualityOfServiceName, sDataStructureFile):
        self.__oQP = dds.QosProvider(sQualityOfServiceFile, sQualityOfServiceName)
        self.__oDP = dds.DomainParticipant(qos = self.__oQP.get_participant_qos())
        self.__sDataStructureFile = sDataStructureFile
        self.__oTopics = None
        self.__oPub = None
        self.DataReceived = Event()

    def AddTopic(self, sTopicName, sDataClassName):
        if (sTopicName == None or sTopicName == ''):
            return

        if (self.__oTopics == None):
            self.__oTopics = []

        gen_info = ddsutil.get_dds_classes_from_idl(self.__sDataStructureFile, sDataClassName)
        oTopic = gen_info.register_topic(self.__oDP, sTopicName, self.__oQP.get_topic_qos())
        self.__oTopics.append(oTopic)

    def AddPublisher(self):
        if (self.__oPub == None):
            self.__oPub = self.__oDP.create_publisher(qos = self.__oQP.get_publisher_qos())

    def Publish(self, sTopic, oData):
        if (self.__oTopics == None):
            return
        if (self.__oPub == None):
            self.AddPublisher()

        for oTopic in self.__oTopics:
            if oTopic.name == sTopic:  
                oWriter = self.__oPub.create_datawriter(oTopic, self.__oQP.get_writer_qos())               
                oWriter.write(oData)
         
    def AddSubscriber(self, sTopic):
        oSub = self.__oDP.create_subscriber(qos = self.__oQP.get_subscriber_qos())
        
        for oTopic in self.__oTopics:
            if oTopic.name == sTopic: 
                oReader = oSub.create_datareader(oTopic, self.__oQP.get_reader_qos())               
                Thread(target = self.Read, args = (oReader,sTopic,)).start()

    def Read(self,oReader, sTopic):
        waitset = dds.WaitSet()
        waitset.attach(dds.ReadCondition(oReader, dds.DDSMaskUtil.all_samples())) 
        while True:
            conditions = waitset.wait()
        
            l = oReader.take(1)

            for sd,si in l:

                self.DataReceived(sTopic, sd)

    def GetDataClass(self,sDataClassName):
        return ddsutil.get_dds_classes_from_idl(self.__sDataStructureFile,sDataClassName).get_class(sDataClassName)

class clsDdsMsg():
    def __init__(self):
        self.__oDds = clsDds('file://DDS_DefaultQoS_All.xml', 'DDS DefaultQosProfile','DataStructs_Msg.idl')
        self.__oDds.DataReceived += self.NewDataAvailable
        self.DataReceived = Event()

    def AddTopic(self, sTopicName):
        self.__oDds.AddTopic(sTopicName,'DataStructs::Msg')

    def AddPublisher(self):
        self.__oDds.AddPublisher()

    def Publish(self, sTopic, sUserID, sMessage):
        Msg = self.__oDds.GetDataClass("DataStructs::Msg")
        self.__oDds.Publish(sTopic, Msg(userID = sUserID, message = sMessage))
         
    def AddSubscriber(self,sTopic):
        self.__oDds.AddSubscriber(sTopic)

    def NewDataAvailable(self, sTopic, oData):
        # if you use: for sd,si in l --> you don't need the .data  
        self.DataReceived(sTopic, oData.userID, oData.message)
        ## if you use: for si in l --> you  need the .data!
        #self.__oFunction(sTopic, oData.data.userID, oData.data.message) 
