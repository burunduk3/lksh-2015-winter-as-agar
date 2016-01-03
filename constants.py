time_step = 0.05
INITIAL_MASS = 30

FIELD_X = 200
FIELD_Y = 200

MAX_LENGTH = 4096

FOOD_NUM = 200
FOOD_MASS = 5

FAIL_COUNT = 50

DEBUG_ON = False
DEBUG_OFF = False

def debug(D):
    return (D | DEBUG_ON) & (not DEBUG_OFF)

DEBUG_PROTOCOL = debug(True)
DEBUG_PROTOCOL_PRINT = debug(False)
