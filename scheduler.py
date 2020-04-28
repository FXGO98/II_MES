from opcua import ua

"""
Null = 0
Boolean = 1
SByte = 2
Byte = 3
Int16 = 4
UInt16 = 5
Int32 = 6
UInt32 = 7
Int64 = 8
UInt64 = 9
Float = 10
Double = 11
String = 12
DateTime = 13
Guid = 14
ByteString = 15
XmlElement = 16
NodeId = 17
ExpandedNodeId = 18
StatusCode = 19
QualifiedName = 20
LocalizedText = 21
ExtensionObject = 22
DataValue = 23
Variant = 24
DiagnosticInfo = 25
"""



dir_up = ua.Variant(1, ua.VariantType(4))
dir_down = ua.Variant(2, ua.VariantType(4))
dir_left = ua.Variant(3, ua.VariantType(4))
dir_right = ua.Variant(4, ua.VariantType(4))

tool_none = ua.Variant(0, ua.VariantType(5))
tool_1 = ua.Variant(1, ua.VariantType(5))
#tool_2 = ua.Variant(2, ua.VariantType(5))
#tool_3 = ua.Variant(3, ua.VariantType(5))

ten_secs = ua.Variant(10000, ua.VariantType(8))
fifteen_secs = ua.Variant(15000, ua.VariantType(8))
twenty_secs = ua.Variant(20000, ua.VariantType(8))
thirty_secs = ua.Variant(30000, ua.VariantType(8))

tool_time = {
    (('P1', 'P4'), ('P4', 'P8'), ('P8', 'P9')) : ten_secs,
    (('P1', 'P2'), ('P2', 'P3'), ('P2', 'P6'), ('P6', 'P9'), ('P3', 'P4')) : fifteen_secs,
    (('P1', 'P3'), ('P3', 'P7'), ('P7', 'P9')) : twenty_secs,
    (('P4', 'P5')) : thirty_secs
}




class BasicScheduler():

    def __init__(self, tr):
        self.order_list = []
        self.transmitter = tr

    def add(self, order):
        self.order_list.append(order)

    def schedule(self):
        ROOT = "ns=4;s=|var|CODESYS Control Win V3 x64.Application"
        ini_type=self.order_list[0].from_
        fin_type=self.order_list[0].to

        for key in tool_time:
            for elem in key:
                typ = (str(ini_type), str(fin_type))
                if (elem == typ):
                    time_tool=tool_time[key]

        ini_t = int(ini_type[len(ini_type)//2:len(ini_type)])
        piece = ua.DataValue(ua.Variant(ini_t, ua.VariantType(5)))
        tr = self.transmitter
        tr.get_node(f"{ROOT}.GVL.ST1_tp").set_value(piece)
        

        # Set conveyors
        LL = [
            (1, 3),
            (3, 8),
            (8, 9),
            (9, 10),
            (10, 4),
        ]

        for i in range (len(LL)):
            ll = LL[i]
            if ((ll[0]==39 and ll[1]==40) or (ll[0]==46 and ll[1]==47)):
                var = 'DIR['+str(i+1)+']' 
                tr.get_node(f"{ROOT}.GVL.{var}").set_value(dir_right)
            
            elif ((ll[0]==40 and ll[1]==39) or (ll[0]==47 and ll[1]==46)):
                var = 'DIR['+str(ll[0])+']' 
                tr.get_node(f"{ROOT}.GVL.{var}").set_value(dir_left)

            elif (ll[0]==39 and ll[1]==41):
                var = 'DIR['+str(ll[0])+']' 
                tr.get_node(f"{ROOT}.GVL.{var}").set_value(dir_down)

            elif (ll[0]==41 and ll[1]==39):
                var = 'DIR['+str(ll[0])+']' 
                tr.get_node(f"{ROOT}.GVL.{var}").set_value(dir_up)

            elif (ll[1]==ll[0]+1):
                var = 'DIR['+str(ll[0])+']' 
                tr.get_node(f"{ROOT}.GVL.{var}").set_value(dir_down)

            elif (ll[1]==ll[0]-1):
                var = 'DIR['+str(ll[0])+']' 
                tr.get_node(f"{ROOT}.GVL.{var}").set_value(dir_up)

            elif (ll[1] > ll[0]+1):
                var = 'DIR['+str(ll[0])+']' 
                tr.get_node(f"{ROOT}.GVL.{var}").set_value(dir_right)

            elif (ll[1] < ll[0]-1):
                var = 'DIR['+str(ll[0])+']' 
                tr.get_node(f"{ROOT}.GVL.{var}").set_value(dir_left)


        # Set MA
        tr.get_node(f"{ROOT}.PLC_PRG.TOOL4").set_value(tool_1)

        # Wait for MA to start working
        print('Waiting for MC')
        while not tr.get_node(f"{ROOT}.GVL.ST4_tr").get_value():
            pass

        print("Machine working!")
        tr.get_node(f"{ROOT}.PLC_PRG.TOOL4").set_value(tool_none)
        tr.get_node(f"{ROOT}.PLC_PRG.TOOL4_t").set_value(time_tool)

        # Set the rest of the path
        LL = [
            ("DIR[4]", dir_right),
            ("DIR[10]", dir_down),
            ("DIR[11]", dir_down),
            ("DIR[12]", dir_down),
            ("DIR[13]", dir_down),
            ("DIR[14]", dir_left),
            ("DIR[7]", dir_left),
            ("DIR[2]", dir_left),
        ]

        for var, dir_ in LL:
            tr.get_node(f"{ROOT}.GVL.{var}").set_value(dir_)
