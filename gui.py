import tkinter as tk
from tkinter import ttk
from solution import *
import math

COLOR_DICT = {0:"gray", 1:"yellow", 2:"yellow", 3:"blue", 4:"blue", 5:"purple", 6:"purple", 7:"green", 8:"green", 9:"red", 10:"red"}

class Piece():

    def __init__(self, number, x, y):
        self.number = number
        self.x0 = x
        self.y0 = y
        if self.number % 2 == 0:
            self.shape = 'r'
        else:
            self.shape = 't'
        # TODO
        self.shape = 'r'
        self.color = COLOR_DICT[self.number] 
        self.size = 35
        self.text_offset = 18


    def draw(self, canvas):
        if self.shape == 'r':
            x1, y1 = self.x0 + self.size, self.y0 + self.size
            canvas.create_rectangle(self.x0, self.y0, x1, y1, fill=self.color, outline="black")
            canvas.create_text(self.x0 + self.text_offset, self.y0 + self.text_offset, text=str(self.number), fill="black", font=("Helvetica 10 bold"))


def left_cw():
    pass

def right_cw():
    pass

def left_ccw():
    pass

def right_ccw():
    pass

def solve():
    pass

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
    root.title('Two Wheel Puzzle Gui')
    geometry = '900x700+50+50'
    root.geometry(geometry)

    button_frame = ttk.Frame(root)
    button_frame.pack(side=tk.RIGHT)

    button1 = ttk.Button(button_frame, text='1', command=left_cw)
    button2 = ttk.Button(button_frame, text='2', command=right_cw)
    button3 = ttk.Button(button_frame, text='3', command=left_ccw)
    button4 = ttk.Button(button_frame, text='4', command=right_ccw)
    buttonsolve = ttk.Button(button_frame, text='Solve', command=solve)
    
    PAD = 8
    button1.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)
    button2.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)
    button3.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)
    button4.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)
    buttonsolve.pack(side=tk.TOP, ipadx=PAD, ipady=PAD)

    canvas = tk.Canvas(root, width=700, height=500)
    draw_state(canvas, INITIAL_STATE)
    canvas.pack()
    
    root.mainloop()
