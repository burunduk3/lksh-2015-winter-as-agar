from tkinter import *

def draw_leaderboard(c, p):
    if len(p) == 0:
        return c
    mx = c.winfo_reqwidth()
    szx = 140
    szy = 30 * len(p)
    if len(p) > 0:
        step = szy / len(p)
    else:
        step = 10
    c.create_rectangle(mx - szx, 0, mx + 2, szy + 30, outline = 'red', dash=(3,5))
    h = 10
    c.create_text(5 + mx - szx / 2, h, text='Leaderboard', font=('Comic Sans MS', 15))
    for i in range(len(p)):
        s = str(i + 1) + '.'
        s += ' ' + p[i]['name']
        c.create_text(mx - szx / 2, h + 20 + i*step + 10, fill='grey', text=s, font=('Times New Roman', 12), activefill='red')
        #c.create_text(mx-szx + 10, h + 20 + i*(szy - h - 20)/10 + 10, fill='red', text=s, anchor='w', font=('Times New Roman', 12))
    return c


def draw_mass(c, a):
    my = c.winfo_reqheight()
    c.create_text(5, my-15, anchor='w', font=('Comin Sans MS', 12), text=str(a), fill='grey')
    return c
