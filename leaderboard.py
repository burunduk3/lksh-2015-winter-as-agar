from tkinter import *


def draw_leader_board(c, p):
    mx = c.winfo_reqwidth()
    szx = 100
    szy = 300
    c.create_rectangle(mx - szx, 0, mx + 2, szy, outline = 'red')
    h = 10
    c.create_text(5 + mx - szx / 2, h, text='Leaders', font='ComicSans')
    for i in range(10):
        s = str(i + 1) + '.'
        if i < len(p):
            s += ' ' + p[i]['name']
        c.create_text(mx-szx + 10, h + 10 + i*(szy - h - 10)/10 + 10, fill='red', text=s, anchor='w')
    return c
