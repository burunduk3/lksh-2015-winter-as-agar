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

#Realation that must be satisfied in order to be absorbed
ABSORB_REL = 1.25
ABSORB_RAD = 0.97

class circle:
	def __init__(self, x, y, m, id):
		self.center = pnt(x, y)
		self.mass = m
		self.r = math.sqrt(m)
		self.id = id
		self.absorbed = False             
	def __lt__(a, b):
		if (a.id == 0) or (b.id == 0): return (a.id < b.id)
		return (a.mass < b.mass)
	def __str__(s):
		return "circle <" + str(s.center) + ", " + str(s.r) + ", " + str(s.absorbed) + ">"
	def absorbable(self, other):
		#print ("vot", distance(self.center, other.center), self.r * ABSORB_RAD)
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
                                   
def update_map2(in_cursors, in_circles, t_step):
	curs_dict = {}
	for c in in_cursors: 
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
			prv_c = circles[j]
			if (prv_c.absorbed): continue
			if (cur_c.absorbable(prv_c)):
				prv_c.absorbed = True
				cur_c.mass += prv_c.mass

#	for c in circles: print(c)
	result = list(filter(lambda x: x.absorbed == False, circles))
	return list(map(lambda x: circle2dict(x), result))

a = []
b = []
a.append({"x" : 0, "y" : 0, "m" : 100, "id" : 1})
a.append({"x" : 9, "y" : 0, "m" : 1, "id" : 0})
b.append({"x" : 0, "y" : 0, "id" : 1})
#b.append({"x" : 9, "y" : 0, "id" : 2})

res = update_map2(b, a, 1)

for c in res :
	print(c)
	          

