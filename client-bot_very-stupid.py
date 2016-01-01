import sys, time, json, threading, random
from protocol import *

killed = False

name = 'Vasya'

id = registerMe(name)
data = {}

def getData():
	global killed, data, id
	while not killed:
		data = getField()
	#	time.sleep(0.1)
	
def getPosition():
	global data, id
	for player in data:
		if player['id'] == id:
			return player['balls'][0]['x'], player['balls'][0]['y']

def createMove():
	global killed, data, id
	while not killed:
		x, y = getPosition()
		dx = random.randint(-10000, 10000)
		dy = random.randint(-10000, 10000)			

		x, y = x + dx, y + dy
		arr = {'x': x, 'y': y, 's': 0, 'id': id}
		sendMe(arr)
	
threading.Thread(target = getData).start()
threading.Thread(target = createMove).start() 	

sys.stdin.readline()
killed = True
sys.exit(0)
