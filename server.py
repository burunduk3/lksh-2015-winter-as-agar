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
import physics
from time import *
from threading import *

time_step = 0.03

class AgarioPlayer:
    def __init__(self, name, cursor):
        self.name = name
        self.id = random.randint(1, 10 ** 36)
        self.circles = [(random.randint(0, 8000), random.randint(0, 4000), 10)]
        self.cursor = (0, 0)


class AgarioServer:
    def __init__(self):
        """
            call init у сокетов
        """
        self.playerLock = Lock()
        self.cursorLock = Lock()
        self.players = dict()

    def addPlayer(self, name):
        self.playerLock.acquire()
        player = AgarioPlayer(name)
        self.player[player.id] = player
        self.playerLock.release()

    def updateCursor(self, cursor):
        """
            cursor['x'] = x курсора
            cursor['y'] = y курсора
            cursor['id'] = id игрока
        """
        self.cursorLock.acquire()
        self.player[cursor['id']].cursor = (cursor['x'], cursor['y'])
        self.cursorLock.release()


server = AgarioServer()

addPlayerCallback = lambda name: server.addPlayer(name)
updateCursorCallback = lambda cursor: server.updateCursor(cursor)

lastTime = time()

while True:
    now = time()
    if (lastTime + time_step < now):
        """
            часть где всё обновляется
        """
        server.cursorLock.acquire()
        server.playerLock.acquire()
        cursors = []
        circles = []

        for pl in server.players:
            id = pl.id
            cursors.append({'x' : pl.cursor[0], 'y' : pl.cursor[1], 'id' : id})
            for circle in pl.circles:
                circles.append({'x' : circles[0], 'y' : circle[1], 'm' : circle[2], 'id' : id})
        server.cursorLock.release()
        server.playerLock.release()
        newcirlces = physics.updateMap0(cursors, circles, time_step)
        """
            рассказать всем о новых полях
        """
        pass
    else:
        sleep(0.01)
