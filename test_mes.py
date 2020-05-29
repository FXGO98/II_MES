import mes
from opcua import ua

ROOT = "ns=4;s=|var|CODESYS Control Win V3 x64.Application"


def as_int(x):
    return ua.Variant(x, ua.VariantType(4))


def as_time(x):
    return ua.Variant(x, ua.VariantType(8))


dir_up = as_int(1)
dir_down = as_int(2)
dir_left = as_int(3)
dir_right = as_int(4)

tool_none = as_int(0)
tool_1 = as_int(1)
tool_2 = as_int(2)
tool_3 = as_int(3)

ten_secs = as_time(10000)
fifteen_secs = as_time(15000)

m = mes.MES()
tr = m.opc_ua_interp.transmitter

"""
dirs = [dir_right, dir_right, dir_down, dir_down, dir_left,
        dir_right, dir_down, dir_left, dir_right, dir_down,
        dir_left, dir_right, dir_down, dir_down, dir_left,
        dir_left, dir_left]


tools = [tool_1, tool_1, tool_1, tool_2, tool_3]
tool_times = [fifteen_secs, fifteen_secs, fifteen_secs, ten_secs, ten_secs]
tool_count = [as_int(2), as_int(1), as_int(2)]
"""

dirs = [dir_right, dir_right, dir_down, dir_down, dir_down, dir_down, dir_down, dir_down,
        dir_right, dir_right, dir_up, dir_up, dir_up, dir_up, dir_up, dir_up,
        dir_right, dir_right, dir_down, dir_down, dir_down, dir_down, dir_down, dir_down,
        dir_right, dir_up, dir_up, dir_up, dir_up, dir_up, dir_up, dir_left,
        dir_down, dir_down, dir_down, dir_down, dir_down, dir_down, dir_left, dir_left,
        dir_up, dir_up, dir_up, dir_up, dir_up, dir_up, dir_left,  dir_left,
        dir_down, dir_down, dir_down, dir_down, dir_down, dir_down, dir_left, dir_left, dir_left]


for i, dir_ in enumerate(dirs):
    tr.get_node(f"{ROOT}.PLC_PRG.TAP_1.PIECE_T.dirs[{i}]").set_value(dir_)

"""
for i, tool in enumerate(tools):
    tr.get_node(f"{ROOT}.PLC_PRG.TAP_1.PIECE_T.tools[{i}]").set_value(tool)

for i, tool_time in enumerate(tool_times):
    tr.get_node(f"{ROOT}.PLC_PRG.TAP_1.PIECE_T.tool_times[{i}]").set_value(
        tool_time)

for i, tool_cnt in enumerate(tool_count):
    tr.get_node(f"{ROOT}.PLC_PRG.TAP_1.PIECE_T.tool_count[{i}]").set_value(
        tool_cnt)
"""

idx = as_int(0)
tr.get_node(f"{ROOT}.PLC_PRG.TAP_1.PIECE_T.idx").set_value(idx)

piece = ua.DataValue(ua.Variant(1, ua.VariantType(5)))
tr.get_node(f"{ROOT}.GVL.ST1_tp").set_value(piece)
