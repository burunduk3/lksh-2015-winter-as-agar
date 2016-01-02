import sys, time, json, threading, random
from protocol import *

killed = False

name = 'Still stupid Bot'

id = registerMe(name)
x, y, m = 0, 0, 0
data = {}

def getData():
	global killed, data, id
	while not killed:
		data = getField()
	#	time.sleep(0.1)
	
def getBestPlayerBall(player):
	maxWeight, bestx, besty = -1, -1, -1
	for ball in player['balls']:
		if maxWeight < ball['m']:
			maxWeight, bestx, besty = ball['m'], ball['x'], ball['y']
	return bestx, besty, maxWeight 
			

def getPosition():
	global data, id
	for player in data:
		if player['id'] == id:
			if len(player['balls']) == 0:
				killed = True
				killMe()
				return 0, 0, 0   
			return getBestPlayerBall(player)
	killed = True
	killMe()
	return 0, 0, 0

def getDist(ball):
	global x, y
	dist = sqrt((data['x'] - x) ** 2 + (data['y'] - y) ** 2)

def goodVictim(ball):
	return m > 1.25 * ball['m']


def getBestVictim():
	global data, id, x, y

	dist = 10000
	victim_x, victim_y = -1, -1

	for player in data:
		if player['id'] == id:
			continue
		for ball in player['balls']:
			if goodVictim(ball) and getDist(ball) < dist:
				dist = getDist(ball)
				victim_x, victim_y = ball['x'], ball['y']

	if x == -1:
		return randint(0, 10000), randint(0, 10000)
	return vectim_x, victim_y
			 
			
		


def createMove():
	global killed, data, id, x, y
	while not killed:
		x, y = getPosition()
		
		victim_x, victim_y = getBestVictim()
		dx, dy = (victim_x - x) * 1000, (victim_y - y) * 1000

		arr = {'x': x + dx, 'y': y + dy, 's': 0}
		sendMe(arr)
	
threading.Thread(target = getData).start()
threading.Thread(target = createMove).start() 	
