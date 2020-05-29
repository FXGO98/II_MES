
from opcua import ua

ROOT = "ns=4;s=|var|CODESYS Control Win V3 x64.Application"


def as_int(x):
    return ua.Variant(x, ua.VariantType(4))


def as_seconds(x):
    return ua.Variant(x*1000, ua.VariantType(8))


def as_piece(x):
    return ua.Variant(x, ua.VariantType(5))


UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

TOOL_NONE = 0
TOOL_1 = 1
TOOL_2 = 2
TOOL_3 = 3

# Tool time
TEN_SECS = as_seconds(10)
FIFTEEN_SECS = as_seconds(15)
TWENTY_SECS = as_seconds(20)
THIRTY_SECS = as_seconds(30)


def get_opp_dir(dir):
    if dir == UP:
        return DOWN
    if dir == DOWN:
        return UP
    if dir == LEFT:
        return RIGHT
    if dir == RIGHT:
        return LEFT


machs = [4, 16, 28, 5, 17, 29, 6, 18, 30]

M = 10000

conveyor_speed = 4
length_small = 2
length_medium = 3
length_big = 4

tool_change_angle = 120
tool_change_speed = 6

tool_change_time = tool_change_angle/tool_change_speed

time_sml = length_small/conveyor_speed
time_med = length_medium/conveyor_speed
time_big = length_big/conveyor_speed

# TODO: this doesnt account for waiting for the piece
# to leave the rotator, but it's a small error
# shouldn't affect our planning too much
time_rotate_one = 1
