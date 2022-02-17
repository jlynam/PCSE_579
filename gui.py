import tkinter as tk
from tkinter import ttk
from solution import *
import math
import time

COLOR_DICT = {0:"gray", 1:"yellow", 2:"yellow", 3:"blue", 4:"blue", 5:"purple", 6:"purple", 7:"green", 8:"green", 9:"red", 10:"red"}
state = INITIAL_STATE

class Piece():

    def __init__(self, number, x, y):
        self.number = number
        self.x0 = x
        self.y0 = y
        if self.number % 2 == 0:
            self.shape = 'r'
        else:
            self.shape = 't'
        self.color = COLOR_DICT[self.number] 
        self.size = 35
        self.text_offset = 18


    def draw(self, canvas):
        if self.shape == 'r':
            x1, y1 = self.x0 + self.size, self.y0 + self.size
            canvas.create_rectangle(self.x0, self.y0, x1, y1, fill=self.color, outline="black")
            canvas.create_text(self.x0 + self.text_offset, self.y0 + self.text_offset, text=str(self.number), fill="black", font=("Helvetica 10 bold"))
        elif self.shape == 't':
            x1, y1 = self.x0 + self.size / 2, self.y0 + self.size
            x2, y2 = self.x0 + self.size, self.y0 
            canvas.create_polygon(self.x0, self.y0, x1, y1, x2, y2, fill=self.color, outline="black")
            canvas.create_text(self.x0 + self.text_offset, self.y0 + self.text_offset - 2, text=str(self.number), fill="black", font=("Helvetica 10 bold"))

def left_cw(canvas):
    global state
    canvas.delete("all")
    state = state[10:12] + state[0:10] + state[12:21] + state[7:10]
    draw_state(canvas, state)

def right_cw(canvas):
    global state
    canvas.delete("all")
    state = state[0:9] + state[11:23] + state[11:14]
    draw_state(canvas, state)

def left_ccw(canvas):
    global state
    canvas.delete("all")
    state = state[2:12] + state [0:2] + state[12:21] + state[11:12] + state[0:2]
    draw_state(canvas, state)
    
def right_ccw(canvas):
    global state
    canvas.delete("all")
    state = state[0:9] + state[19:21] + state[9:22]
    draw_state(canvas, state)
    
# TODO implement A*
def solve(canvas):
    global state
    # print("BFS solution:", breadth_first_search(state))
    solution = a_star_search(state)
    print("A* solution:", solution)
    for move in solution:
       #  print(move)
        if move == 1:
            # canvas.after(2000, lambda: left_cw(canvas))
            left_cw(canvas)
            canvas.update_idletasks()
            time.sleep(1)
        elif move == 2:
            # canvas.after(2000, lambda: right_cw(canvas))
            right_cw(canvas)
            canvas.update_idletasks()
            time.sleep(1)
        elif move == 3:
            # canvas.after(2000, lambda: left_ccw(canvas))
            left_ccw(canvas)
            canvas.update_idletasks()
            time.sleep(1)
        else:
            # canvas.after(2000, lambda: right_ccw(canvas))
            right_ccw(canvas)
            canvas.update_idletasks()
            time.sleep(1)

    print("-----")
            

def deg_to_rad(deg):
    return deg * math.pi / 180

def draw_state(canvas, state):
    # state will be list of numbers, then we use this function to create Piece objects, then we finally draw the pieces
    r = 100
    x0_offset = 250
    x1_offset = x0_offset + 1.7 * r
    y_offset = 250

    pieces = []
    state_index = 0
    thetas_left = range(60, 420, 30)
    for theta in thetas_left:
        x0, y0 = x0_offset + r*math.cos(deg_to_rad(theta)), y_offset + r*math.sin(deg_to_rad(theta)) 
        temp_piece = Piece(state[state_index], x0, y0)
        pieces.append(temp_piece)
        state_index += 1
    
    thetas_right = range(-240, -510, -30)
    for theta in thetas_right:
        x0, y0 = x1_offset + r*math.cos(deg_to_rad(theta)), y_offset + r*math.sin(deg_to_rad(theta)) 
        temp_piece = Piece(state[state_index], x0, y0)
        pieces.append(temp_piece)
        state_index += 1

    for piece in pieces:
        piece.draw(canvas)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Two Wheel Puzzle')
    geometry = '900x700+50+50'
    root.geometry(geometry)

    button_frame = ttk.Frame(root)
    button_frame.pack(side=tk.RIGHT)

    button1 = ttk.Button(button_frame, text='1', command=lambda: left_cw(canvas))
    button2 = ttk.Button(button_frame, text='2', command=lambda: right_cw(canvas))
    button3 = ttk.Button(button_frame, text='3', command=lambda: left_ccw(canvas))
    button4 = ttk.Button(button_frame, text='4', command=lambda: right_ccw(canvas))
    buttonsolve = ttk.Button(button_frame, text='Solve', command=lambda: solve(canvas))
    
    PAD = 8
    button1.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)
    button2.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)
    button3.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)
    button4.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)
    buttonsolve.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)

    canvas = tk.Canvas(root, width=700, height=500)

    canvas.pack()
    draw_state(canvas, state)
    
    root.mainloop()
