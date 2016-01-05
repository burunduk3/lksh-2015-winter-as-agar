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
import physics_main as physics
from time import *
from threading import *
from constants import *

class AgarioPlayer:
    def __init__(self, name, id, mass = INITIAL_MASS):
        self.name = name
        self.id = id
        #FIXED THIS
        x = random.randint(0, FIELD_X)
        y = random.randint(0, FIELD_Y)
        self.circles = [physics.circle(x, y, mass, id, 0, 0, 10, 0)]
        #self.circles = [(random.randint(0, 8000), random.randint(0, 4000), mass)]
        self.cursor = (x, y, 0)
        r = lambda: random.randint(0, 150)
        self.color = ('#%02X%02X%02X' % (r(),r(),r()))


    def addCircle(self, mass = INITIAL_MASS):
        x = random.randint(0, FIELD_X)
        y = random.randint(0, FIELD_Y)
        circ = physics.circle(x, y, mass, self.id, 0, 0, 10, 0)
        self.circles.append(circ)

    def circleSplit(self, cursor):
        buf = []
        i = random.randint(0, len(self.circles) - 1)
        circ = self.circles[i]
        if circ.mass > INITIAL_MASS:
            self.circles[i].mass //= 2
            self.circles.append(physics.circle(cursor['x'], cursor['y'], circ.mass // 2, circ.id, cursor['x'], cursor['y']))


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
    # return True
    return a[0] - r <= p[0] and p[0] <= c[0] + r and a[1] - r <= p[1] and p[1] <= c[1] + r
    # return min(distSegmentPoint(p, a, b), distSegmentPoint(p, b, c), distSegmentPoint(p, c, d), distSegmentPoint(p, d, a)) <= r


class AgarioServer:
    def __init__(self):
        """
            call init у сокетов
        """
        self.playerLock = Lock()
        self.cursorLock = Lock()
        food = AgarioPlayer('', 0, 1) #FTFY ('Food', 1) -> ('Food', 0, 1)
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
        # food = self.players[0]
        for i in range(cnt):
            self.players[0].addCircle(random.randint(FOOD_MASS, 3 * FOOD_MASS))

    def getFood(self):
        # print('getting')
        ans = len(self.players[0].circles)
        # print('get', ans)
        return ans

    def UserExit(self, id):
        self.playerLock.acquire()
        self.eUpdates.append(id)
        self.playerLock.release()

    def updatecursor(self, cursor):
        """
            cursor['x'] = x курсора
            cursor['y'] = y курсора
            cursor['id'] = id игрока
            cursor['s'] = заспличено?
        """
        self.cursorLock.acquire()
        # self.player[cursor['id']].cursor = (cursor['x'], cursor['y'])
        self.cUpdates.append(cursor)
        self.cursorLock.release()

    def applUpdate(self):
        self.cursorLock.acquire()
        self.playerLock.acquire()

        for player in self.pUpdates:
            self.players[player.id] = player
        self.pUpdates.clear()
        for id in self.eUpdates:
            if id in self.players:
                del self.players[id]
        self.eUpdates.clear()
        for cursor in self.cUpdates:
            if cursor['id'] in self.players:
                self.players[cursor['id']].cursor = (cursor['x'], cursor['y'], cursor['s'])
                # if cursor['s'] > 0:
                #     self.players[cursor['id']].circleSplit(cursor)
        self.cUpdates.clear()

        self.cursorLock.release()
        self.playerLock.release()

    def updateCirlces(self, circles):
        for plid in self.players:
            self.players[plid].circles = []
        for circ in circles:                        
            circ.center.x = max(min(circ.center.x, FIELD_X), 0)
            circ.center.y = max(min(circ.center.y, FIELD_Y), 0)
            # circ.x = circ.center.x
            # circ.y = circ.center.y
            # if circ.x >= FIELD_X:
            #     circ.x -= FIELD_X
            # if circ.x < 0:
            #     circ.x += FIELD_X
            # if circ.y >= FIELD_Y:
            #     circ.y -= FIELD_Y
            # if circ.y < 0:
            #     circ.y += FIELD_Y
            # circ.x = circ.center.x % FIELD_X
            # circ.y = circ.center.y % FIELD_Y
            self.players[circ.id].circles.append(circ)
    
    def findColor(self, id):       
        return self.players[id].color

    def getLeaderboard(self):
        lb = []
        for player in self.players.values():
            if player.id is not 0:
                lb.append([player.name, sum(c.mass for c in player.circles)])
        lb.sort(key = lambda a: -a[1])
        lb = list({'name' : a[0]} for a in lb[:10])
        # print(lb)
        return(lb)

    def makeFieldMessage(self, id, leaderboard):
        try:
            center = self.players[id].circles[0].center
        except IndexError:
            return []
        ans = []
        for player in self.players.values():
            player_balls = []
            for circ in player.circles:
                if doCircleAndRectIntersect((circ.center.x, circ.center.y), calculateRadius(circ.mass),
                                            (center.x - WINDOW_WIDTH // 2, center.y - WINDOW_HEIGHT // 2),
                                            (center.x - WINDOW_WIDTH // 2, center.y + WINDOW_HEIGHT // 2),
                                            (center.x + WINDOW_WIDTH // 2, center.y + WINDOW_HEIGHT // 2),
                                            (center.x + WINDOW_WIDTH // 2, center.y - WINDOW_HEIGHT // 2)):
                    player_balls.append({'x' : int(circ.center.x), 'y': int(circ.center.y), 'm': circ.mass})
            ans.append({'name': player.name, 'color' : self.findColor(player.id), 'id': player.id, 'balls': player_balls})
        ans = {'leaderboard' : leaderboard, 'players' : ans}
        # print(ans)
        return ans
