import sys, threading, time, math
from constants import *

#==================================================
# Classes definition
class pnt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @classmethod
    def byAngle(self, a):
        return pnt(math.cos(a), math.sin(a))
    def abs2(s):
        return s.x * s.x + s.y * s.y
    def abs(s):
        return math.sqrt(s.abs2())
    def __add__(a, b):
        return pnt(a.x + b.x, a.y + b.y)
    def __mul__(a, b):
        return pnt(a.x * b, a.y * b)
    def __str__(s):
        return "pnt <" + str(s.x) + ", " + str(s.y) + ">"
    def __sub__(a, b):
        return pnt(a.x - b.x, a.y - b.y)
    
def distance(a, b):
    return (b - a).abs()

class circle:
    def __init__(self, x, y, m, id, to_x, to_y, given_acc):
        self.center = pnt(x, y)
        self.mass = m
        self.r = calculateRadius(m)
        self.id = id
        self.absorbed = False
        self.canAbsorb = True
        self.acceleration = given_acc                    
        if id == 0:
            self.canAbsorb = False
        self.momentum = pnt(to_x, to_y)

    def __lt__(a, b):
        if (a.canAbsorb ^ b.canAbsorb): return not a.canAbsorb
        return (a.mass < b.mass)

    def __str__(s):
        return "circle <" + str(s.center) + ", " + str(s.r) + ", " + str(s.absorbed) + ">"
    def absorbable(self, other):
        if not self.canAbsorb: return False
        if (self.id == other.id): 
            if (self.acceleration != 0) or (other.acceleration != 0): return False
            if (calculateRadius(self.mass) * ABSORB_RAD < distance(self.center, other.center)): return False
            return True
        if (self.mass / other.mass < ABSORB_REL): return False
        if (calculateRadius(self.mass) * ABSORB_RAD < distance(self.center, other.center)): return False
        return True
    def canSplit(self):
        return self.mass > 20

def dict2circle (c):
    return circle(c["x"], c["y"], c["m"], c["id"], c["s"])

def circle2dict (c):
    return {"x" : c.center.x, "y" : c.center.y, "m" : c.mass, "id" : c.id}

#==================================================
# cursors - list of dicts
# circles - list of dicts
# t_step - real number, time of update in seconds

def calc_velocity1(mass):
    ans = (MAX_MASS - mass) / MAX_MASS #VEL_CONST / mass
    ans = min(ans, MAX_VEL)
    ans = max(ans, MIN_VEL)
    return ans
                                       
def calc_velocity2(mass):
    alpha = (MAX_MASS - min(MAX_MASS, mass)) / MAX_MASS
    ans = MIN_VEL + alpha * (MAX_VEL - MIN_VEL)
    return ans
                               
def calc_velocity3(mass):
    ans = min(1.0, VEL_CONST / mass)
    return ans

#Returns a real number in range[0, 1]
def calc_velocity(mass):
    ans = calc_velocity3(mass)
    return ans

def calc_log_velocity(vec_len, mass):
    vec_len = max(vec_len, 1)
    ans = LOG_CONST * math.log(vec_len) / math.sqrt(mass)
    ans = min(ans, MAX_VEL)
    ans = max(ans, MIN_VEL)
    return ans
                                   
#IMPORTANT:
#REQUIRES CIRCLES[] AS CLASS OBJECTS
#ADDS 

def update_map3(in_cursors, circles, t_step):
    curs_dict = {}
    spaceNums = {}     
    for c in in_cursors: 
        curs_dict[c["id"]] = pnt(c["x"], c["y"])
        spaceNums[c["id"]] = c["s"]
    start_len = len(circles)
    for i in range(start_len):
        if circles[i].id == 0 or spaceNums[circles[i].id] == 0 or circles[i].canSplit() == False : continue
        circ = circles[i]
        new_mass = floor(circ.mass / 2 * SPLIT_LOSS)
        new_circ = circle(circ.center.x, circ.center.y, new_mass, circ.id, circ.momentum.x, circ.momentum.y, 10);
        circles.append(new_circ)
        circles[i].mass = new_mass
    for i in range(len(circles)):
        if not circles[i].id in curs_dict or circles[i].id is 0:
            circles[i].canAbsorb = False
            continue
        circ = circles[i]
        cursor = curs_dict[circ.id]
        num = spaceNums[circ.id]
        displacement_vec = cursor - circ.center
        if displacement_vec.abs() > MAX_DIST:
            displacement_vec *= LIMIT_DIST / displacement_vec.abs()
        velocity = calc_log_velocity(displacement_vec.abs(), circ.mass)
        velocity_vec = displacement_vec * velocity * t_step
        new_momentum = circ.momentum * SLIDE_COEF + velocity_vec * (1 - SLIDE_COEF)

        move_vec_len = new_momentum.abs()
        move_vec = pnt(0, 0)
        if move_vec_len > 0 and circ.acceleration > 0:
            move_vec = (new_momentum) * (1 / move_vec_len)
            move_vec = move_vec * circ.acceleration
            circ.acceleration -= deltaAcceleration

        circles[i].center = circ.center + new_momentum + move_vec
        circles[i].momentum = new_momentum
    
    circles.sort()
    for i in range(len(circles)):
        cur_c = circles[i]
        if not cur_c.canAbsorb: continue
        for j in range(i):       
            prv_c = circles[j]
            if (prv_c.absorbed): continue
            if (cur_c.absorbable(prv_c)):
                prv_c.absorbed = True
                cur_c.mass += prv_c.mass
    
    return list(filter(lambda x: x.absorbed == False, circles))

       
