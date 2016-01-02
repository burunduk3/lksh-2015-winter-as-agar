import sys, threading, time, math
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
		return math.sqrt(s.d2())
	def __add__(a, b):
		return pnt(a.x + b.x, a.y + b.y)
	def __mul__(a, b):
		return pnt(a.x * b, a.y * b)
	def __str__(s):
		return "pnt <" + str(s.x) + ", " + str(s.y) + ">"
	def __sub__(a, b):
		return pnt(a.x - b.x, a.y - b.y)

ABSORB_REL = 1.2

class circle:
	def __init__(self, x, y, m, id):
		self.center = pnt(x, y)
		self.mass = m
		self.r = math.sqrt(m)
		self.id = id              
	def __lt__(a, b):
		if (a.id == 0) or (b.id == 0): return (a.id < b.id)
		return (a.mass < b.mass)
	def __str__(s):
		return "circle <" + str(s.center) + ", " + str(s.r) + ">"
	def absorbable(self, other):
		

def dict2circle (c):
	return circle(c["x"], c["y"], c["m"], c["id"])

def circle2dict (c):
	return {"x" : c.center.x, "y" : c.center.y, "m" : c.mass, "id" : c.id}

#==================================================

# cursors - list of dicts
# circles - list of dicts
# t_step - real number, time of update in seconds

# Returns the given map
def update_map0(cursors, circles, t_step):
	return circles

# Merely dislocates circles 
MAX_VEL = 0.3
MIN_VEL = 0.01
VEL_CONST = 5
MAX_MASS = 1000

def calc_velocity(mass):
	ans = (MAX_MASS - mass) / MAX_MASS #VEL_CONST / mass
	print("vel =", ans)
	ans = min(ans, MAX_VEL)
	ans = max(ans, MIN_VEL)
	return ans

def update_map1(in_cursors, in_circles, t_step):
	cursors = []
	curs_dict = {}
	for c in in_cursors: 
		cursors[len(cursors):] = [pnt(c["x"], c["y"])]
		curs_dict[c["id"]] = pnt(c["x"], c["y"])
	circles = list(map(lambda x: dict2circle(x), in_circles))
	
	for i in range(len(circles)):
		circ = circles[i]
		if (circ.id == 0): continue
		cursor = curs_dict[circ.id]
		displacement_vec = cursor - circ.center
		velocity = calc_velocity(circ.mass)
		velocity_vec = displacement_vec * velocity * t_step
		circles[i].center = circ.center + velocity_vec

	return list(map(lambda x: circle2dict(x), circles))

#Handles absorbtions
                                   
def update_map1(in_cursors, in_circles, t_step):
	cursors = []
	curs_dict = {}
	for c in in_cursors: 
		cursors[len(cursors):] = [pnt(c["x"], c["y"])]
		curs_dict[c["id"]] = pnt(c["x"], c["y"])
	circles = list(map(lambda x: dict2circle(x), in_circles))
	circles.sort();

	for i in range(len(circles)):
		circ = circles[i]
		if (circ.id == 0): 
			continue
		cursor = curs_dict[circ.id]                                                                                  
		displacement_vec = cursor - circ.center
		velocity = calc_velocity(circ.mass)
		velocity_vec = displacement_vec * velocity * t_step
		circles[i].center = circ.center + velocity_vec
	
	for i in range(len(circles)):
		for j in range(i):
			cur_c = circles[i]
			prv = circles[j]
			if (prv.absorbed): continue  
			if (cur_c.absorbable(prv))
				prv.absorbed = 1
				cur_c.mass += prv.mass

	return list(map(lambda x: circle2dict(x), result))

a = [{"x" : 0, "y" : 0, "m" : 100, "id" : 1}]
b = [{"x" : 200, "y" : 100, "id" : 1}]

res = update_map1(b, a, 1)

#for c in res :
#	print(c)           

