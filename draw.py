import tkinter as tk
from math import sqrt


def draw_player(c, p):
    r = sqrt(p['mass'])
    c.create_oval(p['x'] - r,
                  p['y'] - r,
                  p['x'] + r,
                  p['y'] + r,
                  fill=p['color']
                  )
    return c
