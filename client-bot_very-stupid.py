import sys, time, json, threading
from protocol import *
from random import randint

killed = False

name = 'name'

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
		dx = randint(-10000, 10000), dy = randint(-10000, 10000)			
		x, y = x + dx, y + dy
		arr = {'x': x, 'y': y, 's': 0}
		sendMe(arr)
	
threading.Thread(target = getData).start()
threading.Thread(target = createMove).start() 	

sys.stdin.readline()
killed = True
