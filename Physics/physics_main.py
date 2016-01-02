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
	def __str__(s):
		return "pnt <" + str(s.x) + ", " + str(s.y) + ">"
	def __sub__(a, b):
		return pnt(a.x - b.x, a.y - b.y)

class circle:
  def __init__(self, x, y, r):
    self.center = pnt(x, y)
    self.r = r
  def
  def __str__(s):
    return "circle <" + str(s.center) + ", " + str(s.r) + ">"
#==================================================

# cursors - list of dicts
# circles - list of dicts
# t_step - real number, time of update in seconds

# very stupid version
def updateMap0(cursors, circles, t_step):
	return circles

# still a stupid version
def updateMap1(cursors, circles, t_step):
	ans = []
	curs_dict = {}
	for c in cursors : 
		curs_dict[c["id"]] = pnt(c["x"], c["y"])
	for c in circles :
		cur_circ = circle(c["x"], c["y"], math.sqrt(c["m"])
		cursor = curs_dict[c["id"]]
		displace_vec = cursor - cur_circ.center


