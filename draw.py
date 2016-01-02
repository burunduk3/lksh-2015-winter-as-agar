from math import sqrt


def draw_players(c, pos, ps):
    # c - Canvas, pos - (x0, y0), ps - players
    x0, y0 = int(pos[0]), int(pos[1])
    for i in range(800):
        if 40 - i % 40 - 1 == x0 % 40:
            c.create_line(i, 0, i, 450, fill='#D0D0D0')
    for i in range(450):
        if 40 - i % 40 - 1 == y0 % 40:
            c.create_line(0, i, 800, i, fill='#D0D0D0')
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
        lx = int(b['x']) - x0
        ly = int(b['y']) - y0
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
