from tkinter import *
from draw import *
from server import *

import sys, json, threading, time	
                 
def onMotion(e):
	global curx, cury, canvas
	curx = e.x
	cury = e.y

def sending():
	global curx, cury, player_id
	

	while True:
		ourx, oury = 0, 0
		for p in curList:
			if (p["id"] == player_id):
				ourx, oury = p["balls"][0]["x"], p["balls"][0]["y"]
				break
		SendMe({"id" : player_id, "x" : ourx - 400 + curx, "y" : oury - 225 + cury, "s" : 0})
		#{'x': 1, 'y': 1, 's': 0}
		time.sleep(0.1)

def drawing():
	global canvas, player_id, curList

	while True:
		ourx, oury = 0, 0
		curList = getField()
		
		for p in curList:
			if (p["id"] == player_id):
				ourx, oury = p["balls"][0]["x"], p["balls"][0]["y"]
				break 

		#[{'name': 'Vasya', 'color': 'blue', 'id': 1, 'balls': [{'x': 1, 'm': 1, 'y': 1}]}]
		canvas = draw_players(canvas, (ourx - 400, ourx - 225), curList)
		time.sleep(0.1)
	

root = Tk()
root.geometry("800x450")
root.title("agar.io_test")

userName = sys.stdin.readline()
print("OK. Your username is " + userName)
#At first get name from keyboard
player_id = registerMe(userName)

curx, cury = 0, 0
curList = []
root.bind("<Motion>", onMotion)

canvas = Canvas(root, height=450, width=800)
canvas.pack()

t1 = threading.Thread(target=drawing, daemon=True)
t2 = threading.Thread(target=sending, daemon=True)
t1.start()
t2.start()

root.mainloop()