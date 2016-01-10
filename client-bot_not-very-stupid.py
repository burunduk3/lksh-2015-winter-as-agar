#!/usr/bin/env python3

import sys, time, json, threading
from client_protocol import *
from constants import *
from random import *

killed = False

name = 'Quite_clever_Bot'

my_id = int(registerMe(name))
print(my_id)
x, y, m, add_m = 0, 0, 0, randint(0, 30)
table = []

def getData():
	global killed, table
	cnt = 0;
	while not killed:
		pam = getField()['players']
	#	print(pam)
		if(pam != []):
			table = pam
		#	print(pam)
			cnt=0
		else:
			cnt += 1
			if(cnt > 50):
				print("Game over")
				killMe()
				killed = True		
		time.sleep(0.01)
	
def getBestPlayerBall(player):
	maxWeight, bestx, besty = -1, -1, -1
	for ball in player['balls']:
		if maxWeight < ball['m']:
			maxWeight, bestx, besty = ball['m'], ball['x'], ball['y']
	return bestx, besty, maxWeight 	


bad = 0
def getPosition():
	global table, my_id, bad
	for player in table:
		if player['id'] == my_id:
			if len(player['balls']) == 0:
				print("Game over")
				killed = True
				killMe()
				return 0, 0, 0   
		#	print(player)
			return getBestPlayerBall(player)
	if(table != []):
		bad += 1
		if(bad > 50) :
			print("Game over")
			killMe()
			killed = True

	return 0, 0, 0

def getBestBot():
	global table, my_id, m

	maxWeight, bot_x, bot_y = -1, -1, -1
	for player in table:
		if player['id'] == my_id:
			continue
		if player['name'] == 'Quite_clever_Bot':
			for ball in player['balls']:
				if ball['m'] > maxWeight:
					maxWeight = ball['m']
					bot_x = ball['x']
					bot_y = ball['y']
	if maxWeight > 1.25 * m:
		return bot_x, bot_y			
	return -1, -1

def getDist(ball):
	global x, y
	dist = sqrt((ball['x'] - x) ** 2 + (ball['y'] - y) ** 2)
	return dist              

def getBestVictim():
	global table, my_id, x, y, m

	meow = 100000000
	victim_x, victim_y = -1, -1

	for player in table:
		if player['id'] == my_id:
			continue
		for ball in player['balls']:
			if m > 1.25 * ball['m'] and getDist(ball) / ball['m'] < meow:
				meow = getDist(ball) / ball['m']
				victim_x, victim_y = ball['x'], ball['y']

	
	if victim_x == -1:
		victim_x = randint(0, 10000)
		victim_y = randint(0, 10000)
	
	return victim_x, victim_y

def createMove():
	global killed, my_id, x, y, m
	while not killed:
		x, y, m = getPosition()
		victim_x, victim_y = getBestVictim()
		bot_x, bot_y = getBestBot()
		dx, dy = 0, 0
		if bot_x != -1 and m > 50 + add_m:
			dx, dy = (bot_x - x) * 10000000, (bot_y - y) * 10000000
		else:
			dx, dy = (victim_x - x) * 10000000, (victim_y - y) * 10000000
		arr = {'id': my_id,'x': x + dx, 'y': y + dy, 's': 0}
		sendMe(arr)
		print(str(x) + " " + str(y) + " " + str(m))
		time.sleep(0.01)
	
threading.Thread(target = getData).start()
threading.Thread(target = createMove).start() 	
sys.stdin.readline()
killMe()
killed = True