from math import *

# Server

MAX_MASS = 500

time_step = 0.05
INITIAL_MASS = 495 

FIELD_X = 2500
FIELD_Y = 2500

WINDOW_HEIGHT = 650
WINDOW_WIDTH = 1300

MAX_LENGTH = 4096

FOOD_NUM = 600
FOOD_MASS = 4
FOOD_GROWTH = 30
FOOD_VAR = 3

FAIL_COUNT = 50

# Physics

#Relation that must be satisfied in order to be absorbed
ABSORB_REL = 1.25
ABSORB_RAD = 0.98

#Various formulas for velocity
MAX_VEL = 1
MIN_VEL = 0.03
MAX_MASS = 1000
VEL_CONST = 1000
LOG_CONST = 1

#Handles absorbtions
MAX_DIST = (min(WINDOW_WIDTH, WINDOW_HEIGHT) / 2 - 50) * 0.8
LIMIT_DIST = MAX_DIST * 0.85
SLIDE_COEF = 0.7 # in range [0;1] - antibot const, adds more sliding
SPLIT_LOSS = 0.9
SPLIT_TIME = 15
deltaAcceleration = 0.5
SPLIT_ACCELERATION = 20

# Client

DELTA_MF = 0.003

# Debug

DEBUG_ON = False
DEBUG_OFF = False

def debug(D):
    return (D | DEBUG_ON) & (not DEBUG_OFF)

DEBUG_PROTOCOL = debug(False)
DEBUG_PROTOCOL_PRINT = debug(False)
DEBUG_SERVER_PRINT = debug(False)

def calculateRadius(mass):
    return 4 * sqrt(mass)

def massFactor(mass):
    return min(max(sqrt(mass) / sqrt(INITIAL_MASS) * (log(INITIAL_MASS) / log(mass)) - 1, 1), 2)