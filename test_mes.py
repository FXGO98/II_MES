import mes
from opcua import ua

ROOT = "ns=4;s=|var|CODESYS Control Win V3 x64.Application"

m = mes.MES()
tr = m.opc_ua_interp.transmitter

piece = ua.DataValue(ua.Variant(1, ua.VariantType(5)))

# dir_up = ua.Variant(1, ua.VariantType(4))
dir_down = ua.Variant(2, ua.VariantType(4))
dir_left = ua.Variant(3, ua.VariantType(4))
dir_right = ua.Variant(4, ua.VariantType(4))

tool_none = ua.Variant(0, ua.VariantType(5))
tool_1 = ua.Variant(1, ua.VariantType(5))
# tool_2 = ua.Variant(2, ua.VariantType(5))
# tool_3 = ua.Variant(3, ua.VariantType(5))
fifteen_secs = ua.Variant(15000, ua.VariantType(8))

tr.get_node(f"{ROOT}.GVL.ST1_tp").set_value(piece)
tr.get_node(f"{ROOT}.PLC_PRG.DIR1").set_value(dir_right)

# Set conveyors
LL = [
    ("DIR3", dir_right),
    ("DIR8", dir_down),
    ("DIR9", dir_down),
    ("DIR10", dir_left),
    ("DIR4", dir_right),
]

for var, dir_ in LL:
    tr.get_node(f"{ROOT}.PLC_PRG.{var}").set_value(dir_)

# Set MA
tr.get_node(f"{ROOT}.PLC_PRG.TOOL4").set_value(tool_1)

# Wait for MA to start working
print('Waiting for MA')
while not tr.get_node(f"{ROOT}.GVL.ST4_tr").get_value():
    pass

print("Machine working!")
tr.get_node(f"{ROOT}.PLC_PRG.TOOL4").set_value(tool_none)
tr.get_node(f"{ROOT}.PLC_PRG.TOOL4_t").set_value(fifteen_secs)

# Set the rest of the path
LL = [
    ("DIR10", dir_down),
    ("DIR11", dir_down),
    ("DIR12", dir_down),
    ("DIR13", dir_down),
    ("DIR14", dir_left),
    ("DIR7", dir_left),
    ("DIR2", dir_left),
]

for var, dir_ in LL:
    tr.get_node(f"{ROOT}.PLC_PRG.{var}").set_value(dir_)
