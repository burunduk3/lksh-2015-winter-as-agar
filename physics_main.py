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

#Relation that must be satisfied in order to be absorbed
ABSORB_REL = 1.25
ABSORB_RAD = 0.97

class circle:
	def __init__(self, x, y, m, id):
		self.center = pnt(x, y)
		self.mass = m
		self.r = calculateRadius(m)
		self.id = id
		self.absorbed = False
		self.canAbsorb = True
		if id == 0:
			self.canAbsorb = False

	def __lt__(a, b):
		if (a.canAbsorb ^ b.canAbsorb): return not a.canAbsorb
		return (a.mass < b.mass)

	def __str__(s):
		return "circle <" + str(s.center) + ", " + str(s.r) + ", " + str(s.absorbed) + ">"

	def absorbable(self, other):
		if not self.canAbsorb: return False
		# if (other.id == 0) and (other.mass == 1): return True MM : жрал всю еду на карте
		if (self.mass / other.mass < ABSORB_REL): return False
		if (self.r * ABSORB_RAD < distance(self.center, other.center)): return False
		return True	

def dict2circle (c):
	return circle(c["x"], c["y"], c["m"], c["id"])

def circle2dict (c):
	return {"x" : c.center.x, "y" : c.center.y, "m" : c.mass, "id" : c.id}

#==================================================
# cursors - list of dicts
# circles - list of dicts
# t_step - real number, time of update in seconds

#Various formulas for velocity
MAX_VEL = 0.5
MIN_VEL = 0.03  
MAX_MASS = 1000
VEL_CONST = 1000
LOG_CONST = 0.8

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

# Returns the given map
def update_map0(cursors, circles, t_step):
	return circles

# Merely dislocates circles
def update_map1(in_cursors, in_circles, t_step):
	curs_dict = {}
	for c in in_cursors:
		curs_dict[c["id"]] = pnt(c["x"], c["y"])
	circles = list(map(lambda x: dict2circle(x), in_circles))

	for i in range(len(circles)):
		circ = circles[i]
		print(circ.id)
		if (circ.id == 0): continue
		cursor = curs_dict[circ.id]
		displacement_vec = cursor - circ.center
		velocity = calc_velocity(circ.mass)
		velocity_vec = displacement_vec * velocity * t_step
		circles[i].center = circ.center + velocity_vec

	return list(map(lambda x: circle2dict(x), circles))

#Handles absorbtions

MAX_DIST = 666
                                   
def update_map(in_cursors, in_circles, t_step):
	curs_dict = {}
	for c in in_cursors: 
		curs_dict[c["id"]] = pnt(c["x"], c["y"])
	circles = list(map(lambda x: dict2circle(x), in_circles))
	# circles.sort();

	for i in range(len(circles)):
		if not circles[i].id in curs_dict or circles[i].id is 0:
			circles[i].canAbsorb = False
			continue
		circ = circles[i]
		cursor = curs_dict[circ.id]                                                                                  
		displacement_vec = cursor - circ.center
		if displacement_vec.abs() > MAX_DIST:
			displacement_vec *= MAX_DIST / displacement_vec.abs()
		velocity = calc_log_velocity(displacement_vec.abs(), circ.mass)
		velocity_vec = displacement_vec * velocity * t_step
		circles[i].center = circ.center + velocity_vec
	for i in range(len(circles)):
		cur_c = circles[i]
		if not cur_c.canAbsorb: continue
		for j in range(len(circles)):
			if i == j:
				continue
			prv_c = circles[j]
			if (prv_c.absorbed): continue
			if (cur_c.absorbable(prv_c)):
				prv_c.absorbed = True
				cur_c.mass += prv_c.mass
	result = list(filter(lambda x: x.absorbed == False, circles))
	return list(map(lambda x: circle2dict(x), result))
       

