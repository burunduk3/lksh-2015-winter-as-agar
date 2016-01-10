import random
from constants import *

LATTICE_STEP = 25
OUTLINE_WIDTH = 2


def draw_bg(c, pos, mf):
    # c - Canvas, pos - (x0, y0)
    x0, y0 = pos
    dx = WINDOW_WIDTH // 2
    dy = WINDOW_HEIGHT // 2
    x1 = dx + x0
    y1 = dx + y0
    LT = int(LATTICE_STEP / mf)
    x1 = x1 % LATTICE_STEP
    y1 = y1 % LATTICE_STEP
    x1 = int(x1 / mf)
    y1 = int(y1 / mf)
    # x0 = LATTICE_STEP - x0 % LATTICE_STEP
    # y0 = LATTICE_STEP - y0 % LATTICE_STEP
    x0 = LT - x1
    y0 = LT - y1
    for i in range(int(WINDOW_WIDTH / LT) + 1):
        c.create_line(i * LT + x0, 0, i * LT + x0, WINDOW_HEIGHT, fill='#D0D0D0')
    for i in range(int(WINDOW_HEIGHT / LT) + 1):
        c.create_line(0, i * LT + y0, WINDOW_WIDTH, i * LT + y0, fill='#D0D0D0')
    return c


def draw_players(c, pos, ps, mf):
    # c - Canvas, pos - (x0, y0), ps - players
    x0, y0 = pos
    q = []
    for p in ps:
        for ball in p['balls']:
            w = dict()
            w['x'] = ball['x']
            w['y'] = ball['y']
            w['m'] = ball['m']
            if p['id'] == 0:
                rand = random.Random(w['x'] * w['y'])
                w['color'] = ('#%02X%02X%02X' % (rand.randint(0, 150),
                                                 rand.randint(0, 150),
                                                 rand.randint(0, 150)))
            else:
                w['color'] = p['color']
            w['name'] = p['name']
            w['id'] = p['id']
            q.append(w)
    q.sort(key=lambda a: (a['m'], a['id']))
    for ball in q:
        lx = ball['x'] - x0
        ly = ball['y'] - y0
        x1 = WINDOW_WIDTH // 2
        y1 = WINDOW_HEIGHT // 2
        rx = lx - x1
        ry = ly - y1
        rx = int(rx / mf)
        ry = int(ry / mf)
        lx = rx + x1
        ly = ry + y1
        radius = calculateRadius(ball['m']) / mf
        r = int(ball['color'][1:3], 16)
        g = int(ball['color'][3:5], 16)
        b = int(ball['color'][5:7], 16)
        r = max(0, r - 20)
        g = max(0, g - 20)
        b = max(0, b - 20)
        c.create_oval(lx - (radius + OUTLINE_WIDTH),
                      ly - (radius + OUTLINE_WIDTH),
                      lx + (radius + OUTLINE_WIDTH),
                      ly + (radius + OUTLINE_WIDTH),
                      fill='#%02X%02X%02X' % (r, g, b),
                      outline='')
        c.create_oval(lx - radius,
                      ly - radius,
                      lx + radius,
                      ly + radius,
                      fill=ball['color'],
                      outline='')
        if len(ball['name']) == 0:
            continue
        if radius // len(ball['name']) > 3:
            c.create_text(lx, ly,
                          font=('Comic Sans MS', int(2.3 * radius // (len(ball['name']) + 1))),
                          text=ball['name'],
                          fill='white')
        else:
            c.create_text(lx, ly-radius-10,
                          font=('Comic Sans MS', 10),
                          text=ball['name'],
                          fill='black')
    return c
