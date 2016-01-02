from server import *

server = AgarioServer()

addPlayerCallback = lambda name, id: server.addPlayer(name, id)
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

        server.addFood(1)
        cursors = []
        circles = []
        for pl in server.players:
            id = pl.id
            cursors.append({'x' : pl.cursor[0], 'y' : pl.cursor[1], 'id' : id})
            for circle in pl.circles:
                circles.append({'x' : circles[0], 'y' : circle[1], 'm' : circle[2], 'id' : id})
        server.updateCirlces(circles)
        newcirlces = physics.updateMap0(cursors, circles, time_step)

        server.cursorLock.release()
        server.playerLock.release()
        """
            рассказать всем о новых полях
        """
        pass
    else:
        sleep(0.01)
