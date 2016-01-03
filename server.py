#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    TODO
    Что мы имплементим:
    какой-то init, который дёргает init у socket'ов
    callback, который дёргают socket'ы:
    - на чувак подключился
    - на чувак что-то послал
"""

import random
import math
import Physics.physics_main as physics
from time import *
from threading import *

time_step = 0.05
INITIAL_MASS = 30

FIELD_X = 100
FIELD_Y = 200

class AgarioPlayer:
    def __init__(self, name, id, mass = INITIAL_MASS):
        self.name = name
        self.id = id
        #FIXED THIS
        self.circles = [(random.randint(0, FIELD_X), random.randint(0, FIELD_Y), mass)]
        #self.circles = [(random.randint(0, 8000), random.randint(0, 4000), mass)]
        self.cursor = self.circles[0][:2]
        r = lambda: random.randint(0, 150)
        self.color = ('#%02X%02X%02X' % (r(),r(),r()))


    def addCircle(self, mass = INITIAL_MASS):
        #FIXED THIS
        self.circles.append((random.randint(0, FIELD_X), random.randint(0, FIELD_Y), mass))
        #self.circles.append((random.randint(0, 8000), random.randint(0, 4000), mass))


def distLinePoint(p, u, v):
    a = v[1] - u[1]
    b = u[0] - v[0]
    c = -(a * u[0] + b * u[1])
    return abs(a * u[0] + b * u[1] + c) / math.hypot(a, b)


def dp(a, b, c, d):
    ux = b[0] - a[0]
    uy = b[1] - a[1]
    vx = d[0] - c[0]
    vy = d[1] - c[1]
    return ux * vx + uy * vy


def distRayPoint(p, a, b):
    if (dp(a, b, a, p) <= 0):
        return math.hypot(p[0] - a[0], p[1] - a[1])
    else:
        return distLinePoint(p, a, b)


def distSegmentPoint(p, a, b):
    return max(distRayPoint(p, a, b), distRayPoint(p, b, a))


def doCircleAndRectIntersect(p, r, a, b, c, d):
    if a[0] <= p[0] <= c[0] and a[1] <= p[1] <= c[1]:
        return True
    return min(distSegmentPoint(p, a, b), distSegmentPoint(p, b, c), distSegmentPoint(p, c, d), distSegmentPoint(p, d, a)) <= r


class AgarioServer:
    def __init__(self):
        """
            call init у сокетов
        """
        self.playerLock = Lock()
        self.cursorLock = Lock()
        food = AgarioPlayer('Food', 0, 1) #FTFY ('Food', 1) -> ('Food', 0, 1)
        food.id = 0
        self.players = {0 : food}
        self.pUpdates = []
        self.cUpdates = []
        self.eUpdates = []
        self.playersColors = {}

    def addPlayer(self, name, id):
        self.playerLock.acquire()
        player = AgarioPlayer(name, id, INITIAL_MASS)
        # self.player[player.id] = player
        self.pUpdates.append(player)
        # self.realPlayers.add(player.id)
        self.playerLock.release()

    def addFood(self, cnt):
        food = self.players[0]
        for i in range(cnt):
            food.addCircle(1)

    def getFood(self):
        return len(self.players[0].circles)

    def UserExit(self, id):
        self.playerLock.acquire()
        self.eUpdates.append(id)
        self.playerLock.release()

    def updatecursor(self, cursor):
        """
            cursor['x'] = x курсора
            cursor['y'] = y курсора
            cursor['id'] = id игрока
        """
        self.cursorLock.acquire()
        # self.player[cursor['id']].cursor = (cursor['x'], cursor['y'])
        self.cUpdates.append(cursor)
        self.cursorLock.release()

    def applUpdate(self, cnt):
        self.cursorLock.acquire()
        self.playerLock.acquire()
        for player in self.pUpdates:
            self.players[player.id] = player
        self.pUpdates.clear()
        for id in self.eUpdates:
            del self.players[id]
        self.eUpdates.clear()
        for cursor in self.cUpdates:
            if cursor['id'] in self.players:
                self.players[cursor['id']].cursor = (cursor['x'], cursor['y'])
        self.cUpdates.clear()
        self.addFood(cnt)
        self.cursorLock.release()
        self.playerLock.release()

    def updateCirlces(self, circles):
        for plid in self.players:
            self.players[plid].circles = []
        for circle in circles:
            self.players[circle['id']].circles.append((circle['x'], circle['y'], circle['m']))
    
    def findColor(self, id):
    	#FIX this: 'red' -> #FF0000
    	return self.players[id].color

    def makeFieldMessage(self, id):
        try:
            center = self.players[id].circles[0][:2]
        except IndexError:
            return []
        ans = []
        for player in self.players.values():
            for circle in player.circles:
                player_balls = []
                if doCircleAndRectIntersect((circle[0], circle[1]), math.sqrt(circle[2]),
                                            (center[0] - 400, center[1] - 200), (center[0] - 400, center[1] + 200),
                                            (center[0] + 400, center[1] + 200), (center[0] + 400, center[1] - 200)):
                    player_balls.append({'x' : circle[0], 'y': circle[1], 'm': circle[2]})
                ans.append({'name': player.name, 'color' : self.findColor(player.id), 'id': player.id, 'balls': player_balls})
        # print(ans)
        return ans
