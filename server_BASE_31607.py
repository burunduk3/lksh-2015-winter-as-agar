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
import time


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
        self.players = dict()

    def addPlayer(self, name):
        player = AgarioPlayer(name)
        self.player[player.id] = player

    def updateCursor(self, cursor):
        """
            cursor['x'] = x курсора
            cursor['y'] = y курсора
            cursor['id'] = id игрока
        """
        self.player[cursor['id']].cursor = (cursor['x'], cursor['y'])


server = AgarioServer()

addPlayerCallback = lambda name: server.addPlayer(name)
updateCursorCallback = lambda cursor: server.updateCursor(cursor)

