import sys, time, json, threading
from client_protocol import *
from constants import *
from random import *

killed = False

name = 'Still_stupid_Bot'

my_id = registerMe(name)
print(my_id)
x, y, m = 0, 0, 0
table = {}

def getData():
	global killed, table
	cnt = 0;
	while not killed:
		pam = getField()
	#	print(pam)
		if(pam != []):
			table = pam
			cnt=0
		else:
			cnt += 1
			if(cnt > 10):
				killed = True		
		time.sleep(0.01)
	
def getBestPlayerBall(player):
	maxWeight, bestx, besty = -1, -1, -1
	for ball in player['balls']:
		if maxWeight < ball['m']:
			maxWeight, bestx, besty = ball['m'], ball['x'], ball['y']
	return bestx, besty, maxWeight 
			

def getPosition():
	global table, my_id
	for player in table:
		if player['id'] == my_id:
			if len(player['balls']) == 0:
				killed = True
				killMe()
				return 0, 0, 0   
		#	print(player)
			return getBestPlayerBall(player)
#	print('!')
#	killed = True
#	killMe()
	return 0, 0, 0

def getDist(ball):
	global x, y
	dist = sqrt((ball['x'] - x) ** 2 + (ball['y'] - y) ** 2)
	return dist              

def goodVictim(ball):
	return m > 1.25 * ball['m']


def getBestVictim():
	global table, my_id, x, y

	meow = 100000000
	victim_x, victim_y = -1, -1

	for player in table:
		if player['id'] == my_id:
			continue
		for ball in player['balls']:
			if goodVictim(ball) and getDist(ball) / ball['m'] < meow:
				meow = getDist(ball) / ball['m']
				victim_x, victim_y = ball['x'], ball['y']

	
	if victim_x == -1:
		victim_x = randint(0, 10000)
	#	print(victim_x)
		victim_y = randint(0, 10000)
	#	print(victim_y)
	
	return victim_x, victim_y
			 
			
		


def createMove():
	global killed, my_id, x, y, m
	while not killed:
		x, y, m = getPosition()
		victim_x, victim_y = getBestVictim()
		dx, dy = (victim_x - x) * 10000000, (victim_y - y) * 10000000
		arr = {'id': my_id,'x': x + dx, 'y': y + dy, 's': 0}
		sendMe(arr)
		print(m)
		time.sleep(0.01)
	
threading.Thread(target = getData).start()
threading.Thread(target = createMove).start() 	
sys.stdin.readline()
killMe()
killed = True