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
split = 0

cur_x = 0.
cur_y = 0.

cur_list = dict()

rnd = []
for i in range(10):
    rnd.append(random.random())


def on_motion(_win, x, y):
    global cur_x, cur_y
    cur_x = x
    cur_y = y


def sending():
    global cur_x, cur_y, player_id, splitLock, split
    while True:
        our_x, our_y = 0, 0
        if cur_list:
            for p in cur_list['players']:
                if p["id"] == player_id:
                    our_x, our_y = p["balls"][0]["x"], p["balls"][0]["y"]
                    break
        splitLock.acquire()
        s = split
        split = 0
        splitLock.release()
        sendMe({"id": player_id, "x": our_x - WINDOW_WIDTH // 2 + cur_x, "y": our_y - WINDOW_HEIGHT // 2 + cur_y, "s": s})
        time.sleep(0.01)


def asking():
    global cur_list
    fail = 0
    tm = time.time()
    cnt = 0
    while True:
        cur_list = getField()
        if not cur_list:
            fail += 1
            if fail > FAIL_COUNT:
                print(fail)
                exit(0)
        else:
            fail = 0
            now = time.time()
            cnt += 1
            if DEBUG_PROTOCOL_PRINT:
                if now - tm > 3:
                    print(cnt, cnt / (now - tm))
                    cnt = 0
                    tm = now
        time.sleep(0.01)


def split_me(event):
    global splitLock, split
    splitLock.acquire()
    split = 1
    splitLock.release()


def draw_ball(x, y, r, fill=(0, 0, 0), prec=30, rot=0):
    glColor3f(max(0., fill[0] - 0.05),
              max(0., fill[1] - 0.05),
              max(0., fill[2] - 0.05))
    glBegin(GL_POLYGON)
    for i in range(prec):
        glVertex2f(x + cos(rot + 2 * pi / prec * i) * (r + OUTLINE_WIDTH),
                   y + sin(rot + 2 * pi / prec * i) * (r + OUTLINE_WIDTH))
    glEnd()
    glColor3f(fill[0], fill[1], fill[2])
    glBegin(GL_POLYGON)
    for i in range(prec):
        glVertex2f(x + cos(rot + 2 * pi / prec * i) * r,
                   y + sin(rot + 2 * pi / prec * i) * r)
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
                w['color'] = ((rnd[0] * ball['x'] + rnd[1] * ball['y']) % 1,
                              (rnd[2] * ball['x'] + rnd[3] * ball['y']) % 1,
                              (rnd[4] * ball['x'] + rnd[5] * ball['y']) % 1)
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
        if ball['id'] == 0:
            prec = 5
            rot = rnd[6] * ball['x'] + \
                  rnd[7] * ball['y'] + \
                  time.time() * (((rnd[8] * ball['x'] + rnd[9] * ball['y']) % 1) - 0.5)
            radius += sin(time.time())
        else:
            prec = int(radius) + 3
            rot = 0
        draw_ball(lx, ly, radius, fill=ball['color'], prec=prec, rot=rot)


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
    global player_id, cur_list
    our_x, our_y = WINDOW_WIDTH / 2.0, WINDOW_HEIGHT / 2.0
    if cur_list:
        ll = cur_list['players']
        for p in ll:
            if p['id'] == player_id:
                our_x, our_y = p['balls'][0]['x'], p['balls'][0]['y']
    else:
        our_x, our_y = 0., 0.
        ll = []
    draw_lattice(our_x - WINDOW_WIDTH / 2, our_y - WINDOW_HEIGHT / 2)
    draw_players((our_x - WINDOW_WIDTH / 2, our_y - WINDOW_HEIGHT / 2), ll)


config_file = open('config.txt', 'r')
ip, port, = open('config.txt', 'r').readline().split()
player_id = registerMe('OpenGL')

t1 = threading.Thread(target=asking, daemon=True).start()
t2 = threading.Thread(target=sending, daemon=True).start()

if not glfw.init():
    exit(0)

glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
# glfw.window_hint(glfw.SAMPLES, 8)
window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'agar.io', None, None)
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
glLineWidth(1.)

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
