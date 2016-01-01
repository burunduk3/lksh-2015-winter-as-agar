from tkinter import *
import sys, json, threading, time	

def onMotion(e):
	global curx, cury, canvas
	curx = e.x
	cury = e.y

def sending():
	global curx, cury
	while True:
		send(curx, cury, 0)
		time.sleep(0.1)

def drawing():
	global canvas
	while True:
		ls = getAllPlayers()
		canvas = draw_player(ls, canvas)
		time.sleep(0.1)
	

root = Tk()
root.geometry("800x450")
root.title("agar.io_test")

userName = sys.stdin.readline()
print("OK. Your username is " + userName)
w
curx, cury = 0, 0

root.bind("<Motion>", onMotion)

canvas = Canvas(root, height=450, width=800)
canvas.pack()

t1 = threading.Thread(target=drawing, daemon=True)
t2 = threading.Thread(target=sending, daemon=True)
t1.start()
t2.start()

root.mainloop()