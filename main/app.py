'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import json
import logging
from os import path

from main import difficulty
from main.model import Minesweeper
from main.view import MinesweeperView
import tkinter as tk


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

HOME_DIR = path.dirname(path.realpath(__file__))
MEM_FILE = path.join(HOME_DIR, 'mem.json')

def save_mem(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def load_mem(file_path):
    data = {}
    if not path.exists(file_path):
        save_mem(file_path, data)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Overrides:
# MinesweeperView.CS = 30

class App(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.protocol("WM_DELETE_WINDOW", self.exit)
        menubar = tk.Menu(parent)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label='New', command=self.new_game)
        game_menu.add_command(label='Exit', command=self.exit)
        menubar.add_cascade(label='Game', menu=game_menu)
        
        difficulty_menu = tk.Menu(menubar, tearoff=0)
        difficulty_menu.add_radiobutton(label='Beginner', command=lambda: self.set_difficulty(difficulty.Beginner))
        difficulty_menu.add_radiobutton(label='Intermediate', command=lambda: self.set_difficulty(difficulty.Intermediate))
        difficulty_menu.add_radiobutton(label='Expert', command=lambda: self.set_difficulty(difficulty.Expert))
        difficulty_menu.add_radiobutton(label='Custom...', command=lambda: difficulty.Custom(self))
         
        menubar.add_cascade(label='Difficulty', menu=difficulty_menu)
        
        parent.config(menu=menubar)
        
        self.header_canvas = tk.Canvas(parent)
        self.canvas = tk.Canvas(parent)
        self.canvas.bind('<Button-1>', self.peek)
        self.canvas.bind('<Button-3>', self.flag)
        
        self.mem = load_mem(MEM_FILE)
        raw_data = self.mem.get('difficulty', difficulty.Beginner)
        self.difficulty = difficulty.Difficulty(*raw_data)
        print(self.difficulty)
        self.new_game()
        self.update_clock()
        
    def new_game(self):
        self.header_canvas.delete("all")
        self.canvas.delete("all")
        
        self.model = Minesweeper(self.difficulty)
        self.first_peek = True
        logging.debug(self.model)

        self.view = MinesweeperView(self.header_canvas, self.canvas, self.model)
        self.header_canvas.pack()
        self.canvas.pack()
    
    def set_difficulty(self, difficulty):
        '''will start a new game with chosen difficulty'''
        self.difficulty = difficulty
        self.new_game()
            
    def peek(self, event):
        logger.debug(f'({event.x},{event.y})')
        logger.debug('left click')
        
        if self.model.game_over:
            return
        x = event.x // self.view.CS
        y = event.y // self.view.CS
        if self.first_peek:
            self.model.first_peek(x, y)
            self.view.update_clues()
            self.first_peek = False
        else:
            self.model.peek(x, y)
        
        self.view.update()
    
    def flag(self, event):
        logger.debug(f'({event.x},{event.y})')
        logger.debug('right click')
        
        if self.model.game_over:
            return
        x = event.x // self.view.CS
        y = event.y // self.view.CS
        self.model.flag(x, y)
        self.view.update()

    def update_clock(self):
        self.view.update_timer()
        self.parent.after(500, self.update_clock)
        
    def exit(self):
        self.mem['difficulty'] = self.difficulty
        save_mem(MEM_FILE, self.mem)
        self.parent.destroy()
        
def start():
    root = tk.Tk()
    App(root).pack()
    root.mainloop()

if __name__ == '__main__':
    start()