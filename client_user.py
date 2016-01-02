#!/usr/bin/env python3

from tkinter import *
from draw import *
from client_protocol import *
from leaderboard import *
import threading
import time
import sys


def onMotion(e):
    global curx, cury, canvas
    curx = e.x
    cury = e.y


def sending():
    global curx, cury, player_id
    while True:
        ourx, oury = 0, 0
        for p in curList:
            if p["id"] == player_id:
                ourx, oury = p["balls"][0]["x"], p["balls"][0]["y"]
                break
        sendMe({"id": player_id, "x": ourx - 400 + curx, "y": oury - 225 + cury, "s": 0})
        # {'x': 1, 'y': 1, 's': 0}
        time.sleep(0.01)


def asking():
    global curList
    while True:
        # print("abacabadabacaba")
        curList = getField()
        print('getField: '+str(curList))
        # print("abacaba")
        time.sleep(0.01)


def drawing():
    global canvas, player_id, curList
    ourx, oury, m = 400, 225, 0
    ll = curList
    for p in ll:
        if p["id"] == player_id:
            ourx, oury = p["balls"][0]["x"], p["balls"][0]["y"]
            for b in p["balls"]:
                m += b['m']
            break
            # [{'name': 'Vasya', 'color': 'blue', 'id': 1, 'balls': [{'x': 1, 'm': 1, 'y': 1}]}]
    canvas.delete("all")
    canvas = draw_bg(canvas, (ourx - 400, oury - 225))
    canvas = draw_players(canvas, (ourx - 400, oury - 225), ll)
    canvas = draw_mass(canvas, m)
    root.after(10, drawing)


root = Tk()
root.wm_resizable(0, 0)
root.geometry("800x450")
root.title("agar.io_test")

userName, ip, port = None, None, None
if len(sys.argv) > 1:
    userName = sys.argv[1]
if len(sys.argv) > 2:
    ip = sys.argv[2]
if len(sys.argv) > 2:
    port = sys.argv[3]

if userName is None:
    print('enter your user name: ', end='', flush=True)
    userName = " ".join(sys.stdin.readline().split())
print("OK. Your username is " + userName)

if ip is None:
    print('enter server ip: ', end='', flush=True)
    ip = sys.stdin.readline().split()[0]
print("OK. ip is " + ip)

if port is None:
    print('enter port: ', end='', flush=True)
    port = sys.stdin.readline().split()[0]
print("OK. port is " + port)

out = open("config.txt", "w")
out.write(ip + " " + port)
out.close()
# At first get name from keyboard
player_id = registerMe(userName)
print("connected")

curx, cury = 0, 0
# curList = getField()
curList = []
root.bind("<Motion>", onMotion)

canvas = Canvas(root, height=450, width=800)
canvas.pack()

t1 = threading.Thread(target=asking, daemon=True)
t2 = threading.Thread(target=sending, daemon=True)
t1.start()
t2.start()
root.after(0, drawing)

root.mainloop()
