from constants import *

STEP = 25
OUTLINE_WIDTH = 2


def draw_bg(c, pos):
    # c - Canvas, pos - (x0, y0)
    x0, y0 = pos
    x0 = STEP - x0 % STEP
    y0 = STEP - y0 % STEP
    for i in range(int(WINDOW_WIDTH / STEP) + 1):
        c.create_line(i * STEP + x0, 0, i * STEP + x0, WINDOW_HEIGHT, fill='#D0D0D0')
    for i in range(int(WINDOW_HEIGHT / STEP) + 1):
        c.create_line(0, i * STEP + y0, WINDOW_WIDTH, i * STEP + y0, fill='#D0D0D0')
    return c


def draw_players(c, pos, ps):
    # c - Canvas, pos - (x0, y0), ps - players
    x0, y0 = pos
    q = []
    for p in ps:
        for ball in p['balls']:
            w = dict()
            w['x'] = ball['x']
            w['y'] = ball['y']
            w['m'] = ball['m']
            w['color'] = p['color']
            w['name'] = p['name']
            w['id'] = p['id']
            q.append(w)
    q.sort(key=lambda a: (a['m'], a['id']))
    for ball in q:
        lx = ball['x'] - x0
        ly = ball['y'] - y0
        radius = int(calculateRadius(ball['m']))
        r = int(ball['color'][1:3], 16)
        g = int(ball['color'][3:5], 16)
        b = int(ball['color'][5:7], 16)
        r = max(0, r - 20)
        g = max(0, g - 20)
        b = max(0, b - 20)
        c.create_oval(lx - radius - OUTLINE_WIDTH,
                      ly - radius - OUTLINE_WIDTH,
                      lx + radius + OUTLINE_WIDTH,
                      ly + radius + OUTLINE_WIDTH,
                      fill='#%02X%02X%02X' % (r, g, b),
                      outline='')
        c.create_oval(lx - radius,
                      ly - radius,
                      lx + radius,
                      ly + radius,
                      fill=ball['color'],
                      outline='')
        if len(ball['name']) > 0 and radius // len(ball['name']) > 3:
            c.create_text(lx, ly,
                          font=('Comic Sans MS', 2 * radius // (len(ball['name']) + 1)),
                          text=ball['name'],
                          fill='white')
    return c
