import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
import random
from constants import *
import threading
import time
import sys
from client_protocol import *

LATTICE_STEP = 50
OUTLINE_WIDTH = 3

splitLock = threading.Lock()
splitted = 0


def on_motion(w, x, y):
    global curx, cury
    curx = x
    cury = y


def sending():
    global curx, cury, player_id, splitLock, splitted
    while True:
        ourx, oury = 0, 0
        if curList != []:
            for p in curList['players']:
                if p["id"] == player_id:
                    ourx, oury = p["balls"][0]["x"], p["balls"][0]["y"]
                    break
        splitLock.acquire()
        s = splitted
        splitted = 0
        splitLock.release()
        sendMe({"id": player_id, "x": ourx - WINDOW_WIDTH // 2 + curx, "y": oury - WINDOW_HEIGHT // 2 + cury, "s": s})
        # {'x': 1, 'y': 1, 's': 0}
        time.sleep(0.01)


def asking():
    global curList
    fail = 0
    tm = time.time()
    cnt = 0
    while True:
        curList = getField()

        if not curList:
            fail += 1
            if fail > FAIL_COUNT:
                print(fail)
                exit(0)
        else:
            fail = 0
            now = time.time()
            cnt += 1
            if DEBUG_PROTOCOL_PRINT:
                if (now - tm > 3):
                    print(cnt, cnt / (now - tm))
                    cnt = 0
                    tm = now
        time.sleep(0.01)


def splitMe(event):
    global splitLock, splitted
    splitLock.acquire()
    splitted = 1
    splitLock.release()


def draw_circle(x, y, r, c, prec, rot=0):
    glColor3f(c[0], c[1], c[2])
    glBegin(GL_POLYGON)
    for i in range(prec):
        glVertex2f(x + cos(rot + 2 * pi / prec * i) * r, y + sin(rot + 2 * pi / prec * i) * r)
    glEnd()


def draw_players(pos, ps):
    x0, y0 = pos
    q = []
    for p in ps:
        for ball in p['balls']:
            w = dict()
            w['x'] = ball['x']
            w['y'] = ball['y']
            w['m'] = ball['m']
            if p['id'] == 0:
                w['color'] = ((1.12 * ball['x'] + 1.04 * ball['y']) % 1,
                              (1.24 * ball['x'] + 1.13 * ball['y']) % 1,
                              (1.03 * ball['x'] + 1.27 * ball['y']) % 1)
            else:
                w['color'] = (int(p['color'][1:3], 16) / 255,
                              int(p['color'][3:5], 16) / 255,
                              int(p['color'][5:7], 16) / 255)
            w['id'] = p['id']
            q.append(w)
    q.sort(key=lambda a: (a['m'], a['id']))
    for ball in q:
        lx = ball['x'] - x0
        ly = ball['y'] - y0
        radius = calculateRadius(ball['m'])
        r = ball['color'][0]
        g = ball['color'][1]
        b = ball['color'][2]
        r = max(0, r - 0.05)
        g = max(0, g - 0.05)
        b = max(0, b - 0.05)
        if ball['id'] == 0:
            prec = 5
            rot = ball['x'] + ball['y']
        else:
            prec = int(radius) + 3
            rot = 0
        draw_circle(lx, ly, radius + OUTLINE_WIDTH, (r, g, b), prec, rot=rot)
        draw_circle(lx, ly, radius, ball['color'], prec, rot=rot)


def draw_lattice(x0, y0):
    glColor3f(0.5, 0.5, 0.5)
    x0 = LATTICE_STEP - x0 % LATTICE_STEP
    y0 = LATTICE_STEP - y0 % LATTICE_STEP
    for i in range(int(WINDOW_WIDTH / LATTICE_STEP) + 1):
        glBegin(GL_LINES)
        glVertex2f(i * LATTICE_STEP + x0, 0)
        glVertex2f(i * LATTICE_STEP + x0, WINDOW_HEIGHT)
        glEnd()
    for i in range(int(WINDOW_HEIGHT / LATTICE_STEP) + 1):
        glBegin(GL_LINES)
        glVertex2f(0, i * LATTICE_STEP + y0)
        glVertex2f(WINDOW_WIDTH, i * LATTICE_STEP + y0)
        glEnd()


def draw():
    global player_id, curList
    ourx, oury, = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
    if curList:
        ll = curList['players']
        for p in ll:
            if p["id"] == player_id:
                ourx, oury = p["balls"][0]["x"], p["balls"][0]["y"]
    else:
        ourx, oury, m = 0, 0, 1
        ll = []
    draw_lattice(ourx - WINDOW_WIDTH // 2, oury - WINDOW_HEIGHT // 2)
    draw_players((ourx - WINDOW_WIDTH // 2, oury - WINDOW_HEIGHT // 2), ll)


config_file = open("config.txt", "r")
ip, port, = open("config.txt", "r").readline().split()
player_id = registerMe('OpenGL')

curx, cury = 400, 225
curList = []

t1 = threading.Thread(target=asking, daemon=True).start()
t2 = threading.Thread(target=sending, daemon=True).start()

if not glfw.init():
    exit(0)

glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
# glfw.window_hint(glfw.GLFW_SAMPLES, 4)
window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "agar.io", None, None)
w, h = glfw.get_video_mode(glfw.get_primary_monitor())[0]
glfw.set_window_pos(window, (w - WINDOW_WIDTH) // 2, (h - WINDOW_HEIGHT) // 2)
glfw.set_cursor_pos_callback(window, on_motion)

if not window:
    glfw.terminate()
    exit(0)

glfw.make_context_current(window)
glfw.swap_interval(1)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
glLineWidth(0.5)

glClearColor(1., 1., 1., 1.)
glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    draw()
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
