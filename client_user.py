#!/usr/bin/env python3

from tkinter import *
from draw import *
from client_protocol import *
from leaderboard import *
import threading
import time
import sys
from constants import *



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
        sendMe({"id": player_id, "x": ourx - WINDOW_WIDTH // 2 + curx, "y": oury - WINDOW_HEIGHT // 2 + cury, "s": 0})
        # {'x': 1, 'y': 1, 's': 0}
        time.sleep(0.01)

def asking():
    global curList
    fail = 0
    tm = time.time()
    cnt = 0
    while True:
        # print("abacabadabacaba")
        curList = getField()

        if curList == []:
            fail += 1
            if fail > FAIL_COUNT:
                print(fail)
                root.quit()
                exit(0)
        else:
            fail = 0
            now = time.time()
            cnt += 1
            if DEBUG_PROTOCOL_PRINT:
                if (now - tm > 3):
                    print(cnt, cnt  / (now - tm))
                    cnt = 0
                    tm = now
        # print('getField: '+str(curList))
        # print("abacaba")
        time.sleep(0.01)


def drawing():
    global canvas, player_id, curList
    ourx, oury, m = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 0
    ll = curList
    for p in ll:
        if p["id"] == player_id:
            ourx, oury = p["balls"][0]["x"], p["balls"][0]["y"]
            for b in p["balls"]:
                m += b['m']
            break
            # [{'name': 'Vasya', 'color': 'blue', 'id': 1, 'balls': [{'x': 1, 'm': 1, 'y': 1}]}]
    canvas.delete("all")
    canvas = draw_bg(canvas, (ourx - WINDOW_WIDTH // 2, oury - WINDOW_HEIGHT // 2))
    canvas = draw_players(canvas, (ourx - WINDOW_WIDTH // 2, oury - WINDOW_HEIGHT // 2), ll)
    canvas = draw_mass(canvas, 'm:' + str(m) + ' x:' + str(int(round(ourx))) + ' y:' + str(int(round(oury))))
    root.after(10, drawing)


root = Tk()
root.wm_resizable(0, 0)
root.geometry(str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT))
root.title("agar.io_test")

userName, ip, port = None, None, None
if len(sys.argv) > 1:
    userName = sys.argv[1]
if len(sys.argv) > 2:
    ip = sys.argv[2]
if len(sys.argv) > 2:
    port = sys.argv[3]

ip = '192.168.3.83'
port = '3030'

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

canvas = Canvas(root, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
canvas.pack()

t1 = threading.Thread(target=asking, daemon=True)
t2 = threading.Thread(target=sending, daemon=True)
t1.start()
t2.start()
root.after(0, drawing)

root.mainloop()
