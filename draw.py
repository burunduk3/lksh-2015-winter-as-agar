from math import sqrt

step = 25


def draw_bg(c, pos):
    # c - Canvas, pos - (x0, y0)
    x0, y0 = pos
    x0 = 20 - x0 % step
    y0 = 20 - y0 % step
    for i in range(int(800 / step) + 1):
        c.create_line(i * step + x0, 0, i * step + x0, 450, fill='#D0D0D0')
    for i in range(int(450 / step) + 1):
        c.create_line(0, i * step + y0, 800, i * step + y0, fill='#D0D0D0')
    return c


def draw_players(c, pos, ps):
    # c - Canvas, pos - (x0, y0), ps - players
    x0, y0 = pos
    q = []
    for p in ps:
        for b in p['balls']:
            w = dict()
            w['x'] = b['x']
            w['y'] = b['y']
            w['m'] = b['m']
            w['color'] = p['color']
            w['name'] = p['name']
            w['id'] = p['id']
            q.append(w)
    q.sort(key=lambda a: (a['m'], a['id']))
    for b in q:
        lx = b['x'] - x0
        ly = b['y'] - y0
        r = int(sqrt(b['m']))
        c.create_oval(lx - r,
                      ly - r,
                      lx + r,
                      ly + r,
                      fill=b['color'],
                      outline='')
        if len(b['name']) > 0 and r // len(b['name']) > 3:
            c.create_text(lx, ly,
                          font=('Comic Sans MS', 2 * r // (len(b['name']) + 1)),
                          text=b['name'],
                          fill='white')
    return c
