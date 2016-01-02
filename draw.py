from math import sqrt


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
        if r > 20:
            c.create_text(lx, ly,
                          font=('Comic Sans MS', 5 * r // (3 * len(b['name']) + 1) + 1),
                          text=b['name'])
    return c
