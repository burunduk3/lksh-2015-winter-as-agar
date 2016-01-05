#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server import *
import server_protocol as protocol
from threading import *

from constants import *

server = AgarioServer()
server.addFood(FOOD_NUM) #added this line

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
        if (server.getFood() < FOOD_NUM):
            server.addFood(FOOD_GROWTH)
        server.applUpdate()
        # print('upd', now)
        cursors = []
        circles = []
        # print(server.players[0].circles, end=' ')
        for pl in server.players.values():
            id = pl.id
            if len(pl.circles) > 0:
                cursors.append({'x' : pl.cursor[0], 'y' : pl.cursor[1], 'id' : id})
            for circ in pl.circles:
                circles.append(circ)
        newcircles = physics.update_map3(cursors, circles, dt)
        server.updateCirlces(newcircles)
        # print(server.players[0].circles)
        # print(len(newcirlces), len(circles))
        """
            рассказать всем о новых полях
        """
        for player in server.players.values():
            if (player.id is not 0):
                protocol.sendMap(player.id, server.makeFieldMessage(player.id))
        if DEBUG_SERVER_PRINT:
            print(now, newcircles)
        # print(server.players.keys())
    # else:
    #     sleep(0.01)
