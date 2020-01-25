'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import logging

from main.model import Minesweeper
from main.view import MinesweeperView
from os import path
import tkinter as tk
import json
from collections import namedtuple

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
Difficulty = namedtuple('Difficulty', ['width', 'height', 'bombs'])
DIFFICULTY_LEVELS = {
    'Beginner': Difficulty(9, 9, 10),
    'Intermediate': Difficulty(15, 15, 40),
    'Expert': Difficulty(30, 16, 99),
}

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
        
        options_menu = tk.Menu(menubar, tearoff=0)
        difficulty_submenu = tk.Menu(options_menu, tearoff=0)
        difficulty_submenu.add_radiobutton(label='Beginner', command=lambda: self.set_difficulty(DIFFICULTY_LEVELS['Beginner']))
        difficulty_submenu.add_radiobutton(label='Intermediate', command=lambda: self.set_difficulty(DIFFICULTY_LEVELS['Intermediate']))
        difficulty_submenu.add_radiobutton(label='Expert', command=lambda: self.set_difficulty(DIFFICULTY_LEVELS['Expert']))
        difficulty_submenu.add_radiobutton(label='Custom...', command=self.popup_custom_difficulty)
        options_menu.add_cascade(label='Difficulty', menu=difficulty_submenu, underline=0)
         
        menubar.add_cascade(label='Options', menu=options_menu)
        
        parent.config(menu=menubar)
        
        self.header_canvas = tk.Canvas(parent)
        self.canvas = tk.Canvas(parent)
        self.canvas.bind('<Button-1>', self.peek)
        self.canvas.bind('<Button-3>', self.flag)
        
        self.mem = load_mem(MEM_FILE)
        raw_data = self.mem.get('difficulty', DIFFICULTY_LEVELS['Beginner'])
        self.difficulty = Difficulty(*raw_data)
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
    
    def popup_custom_difficulty(self):
        popup = tk.Toplevel()
        popup.wm_title("Window")

        l = tk.Label(popup, text="width")
        l.grid(row=0, column=0)
        e1 = tk.Scale(popup, from_=10, to=30, orient=tk.HORIZONTAL)
        e1.grid(row=0, column=1)
        e1.set(self.difficulty.width);
        l = tk.Label(popup, text="height")
        l.grid(row=1, column=0)
        e2 = tk.Scale(popup, from_=10, to=30, orient=tk.HORIZONTAL)
        e2.grid(row=1, column=1)
        e2.set(self.difficulty.height);
        l = tk.Label(popup, text="bombs %")
        l.grid(row=2, column=0)
        e3 = tk.Scale(popup, from_=10, to=90, orient=tk.HORIZONTAL)
        e3.grid(row=2, column=1)
        e3.set(self.difficulty.bombs * 100 // (self.difficulty.width * self.difficulty.height));
        def custom_difficulty_okay():
            try:
                custom_width = e1.get()
                custom_height = e2.get()
                custom_bombs = custom_width * custom_height * e3.get() // 100  
                custom_difficulty = Difficulty(custom_width,custom_height,custom_bombs)
                self.set_difficulty(custom_difficulty)
                popup.destroy()
            except:
                print("Wrong")
        b = tk.Button(popup, text="Okay", command=custom_difficulty_okay)
        b.grid(row=3, column=1)
        
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