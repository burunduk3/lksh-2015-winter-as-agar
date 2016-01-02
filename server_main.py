# -*- coding: utf-8 -*-

from server import *
import server_protocol as protocol

server = AgarioServer()

protocol.initserver(server)

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
        newcirlces = physics.updateMap0(cursors, circles, dt)
        server.updateCirlces(newcirlces)
        """
            рассказать всем о новых полях
        """
        for player in server.players.values():
            protocol.sendMap(player.id, server.makeFieldMessage(player.id))
    else:
        sleep(0.01)
