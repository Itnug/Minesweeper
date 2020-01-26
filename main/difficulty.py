'''
Created on 26-Jan-2020

@author: Srinivas Gunti
'''
import tkinter as tk
from collections import namedtuple

Difficulty = namedtuple('Difficulty', ['width', 'height', 'bombs'])

Beginner = Difficulty(9, 9, 10)
Intermediate = Difficulty(15, 15, 40)
Expert = Difficulty(30, 16, 99)

class Custom(tk.Toplevel):

    def __init__(self, app):
        tk.Toplevel.__init__(self)
        self.wm_title("Custom...")
        self.app = app
        
        l = tk.Label(self, text="Width")
        l.grid(row=0, column=0)
    
        self.width_scale = tk.Scale(self, from_=10, to=30, orient=tk.HORIZONTAL)
        self.width_scale.grid(row=0, column=1)
        self.width_scale.set(app.difficulty.width);
        
        l = tk.Label(self, text="Height")
        l.grid(row=1, column=0)

        self.height_scale = tk.Scale(self, from_=10, to=30, orient=tk.HORIZONTAL)
        self.height_scale.grid(row=1, column=1)
        self.height_scale.set(app.difficulty.height);

        l = tk.Label(self, text="Bombs %")
        l.grid(row=2, column=0)

        self.bombs_pct_scale = tk.Scale(self, from_=10, to=90, orient=tk.HORIZONTAL)
        self.bombs_pct_scale.grid(row=2, column=1)
        self.bombs_pct_scale.set(app.difficulty.bombs * 100 // (app.difficulty.width * app.difficulty.height));

        b = tk.Button(self, text="Okay", command=self.on_okay)
        b.grid(row=3, column=1)
           
    def on_okay(self):
        try:
            w = self.width_scale.get()
            h = self.height_scale.get()
            b = w * h * self.bombs_pct_scale.get() // 100  
            custom_difficulty = Difficulty(w, h, b)
            self.app.set_difficulty(custom_difficulty)
            self.destroy()
        except:
            print("Wrong")