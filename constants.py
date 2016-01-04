from math import sqrt

time_step = 0.05
INITIAL_MASS = 20

FIELD_X = 6000
FIELD_Y = 500

WINDOW_HEIGHT = 650
WINDOW_WIDTH = 1300

MAX_LENGTH = 4096

FOOD_NUM = 600
FOOD_MASS = 1
FOOD_GROWTH = 10

FAIL_COUNT = 50

DEBUG_ON = False
DEBUG_OFF = False

def debug(D):
    return (D | DEBUG_ON) & (not DEBUG_OFF)

DEBUG_PROTOCOL = debug(True)
DEBUG_PROTOCOL_PRINT = debug(False)
DEBUG_SERVER_PRINT = debug(False)

def calculateRadius(mass):
    return 4 * sqrt(mass)