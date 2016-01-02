#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server import *
import server_protocol as protocol
from threading import *

# изначальное количество еды
INIT_NUM_OF_FOOD = 30

server = AgarioServer()
server.addFood(INIT_NUM_OF_FOOD)

t1 = Thread(target=protocol.initserver, daemon=True, args=[server])

t1.start()

addPlayerCallback = lambda name, id: server.addPlayer(name, id)
updateCursorCallback = lambda cursor: server.updateCursor(cursor)

lastTime = time()

while True:
    now = time()
    if (lastTime + time_step < now):
        """
            часть где всё обновляется
        """
        dt = now - lastTime
        lastTime = now
        server.applUpdate(0)
        cursors = []
        circles = []
        for pl in server.players.values():
            id = pl.id
            cursors.append({'x' : pl.cursor[0], 'y' : pl.cursor[1], 'id' : id})
            for circle in pl.circles:
                circles.append({'x' : circle[0], 'y' : circle[1], 'm' : circle[2], 'id' : id})
        newcirlces = physics.update_map(cursors, circles, dt)
        server.updateCirlces(newcirlces)
        """
            рассказать всем о новых полях
        """
        for player in server.players.values():
            if (player.id is not 0):
                protocol.sendMap(player.id, server.makeFieldMessage(player.id))
        # print(now, newcirlces)
        # print(server.players.keys())
    else:
        sleep(0.01)
