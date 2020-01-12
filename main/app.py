'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import tkinter as tk
from main.model import Minesweeper

global mouse_x
global mouse_y
mouse_x = 0
mouse_y = 0

W = 10
H = 10
B = 10
CS = 20

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.canvas = tk.Canvas(self, width=W * CS, height=H * CS, highlightthickness=0)
        self.canvas.bind("<Button-1>",find_mouse_xy)
        self.canvas.pack()
        
        for i in range(W):
            for j in range(H):
                self.canvas.create_rectangle(i*CS, j*CS, (i+1)*CS, (j+1)*CS)
        
        self.model = Minesweeper(W,H)

if __name__ == '__main__':
    root = tk.Tk()
    App(root).pack()
    root.mainloop()




#Keyframe editor: (DO LATER)

#Displays mouse x and y on workspace:
def find_mouse_xy(event):
    mouse_x = event.winfo_pointerx()
    mouse_y = event.winfo_pointery()
    print ("x: " + str(mouse_x))
    print ("y: " + str(mouse_y))



