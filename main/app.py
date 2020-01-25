'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import logging

from main.model import Minesweeper
from main.view import MinesweeperView
import tkinter as tk
from collections import namedtuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Overrides:
# MinesweeperView.CS = 30
Difficulty = namedtuple('Difficulty', ['width', 'height', 'bombs'])
DIFFICULTY_LEVELS = {
    'easy': Difficulty(9, 9, 10),
    'intermediate': Difficulty(15, 15, 40),
    'hard': Difficulty(30, 16, 99),
}

class App(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        menubar = tk.Menu(parent)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label='New', command=self.new_game)
        game_menu.add_command(label='Exit', command=parent.quit)
        menubar.add_cascade(label='Game', menu=game_menu)
        
        options_menu = tk.Menu(menubar, tearoff=0)
        difficulty_submenu = tk.Menu(options_menu, tearoff=0)
        difficulty_submenu.add_radiobutton(label="Easy", command=lambda: self.set_difficulty(DIFFICULTY_LEVELS['easy']))
        difficulty_submenu.add_radiobutton(label="Intermediate", command=lambda: self.set_difficulty(DIFFICULTY_LEVELS['intermediate']))
        difficulty_submenu.add_radiobutton(label="Hard", command=lambda: self.set_difficulty(DIFFICULTY_LEVELS['hard']))
        options_menu.add_cascade(label='Difficulty', menu=difficulty_submenu, underline=0)
         
        menubar.add_cascade(label='Options', menu=options_menu)
        
        parent.config(menu=menubar)
        
        self.header_canvas = tk.Canvas(parent)
        self.canvas = tk.Canvas(parent)
        self.canvas.bind('<Button-1>', self.peek)
        self.canvas.bind('<Button-3>', self.flag)
        
        self.difficulty = DIFFICULTY_LEVELS['easy']
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
        
def start():
    root = tk.Tk()
    App(root).pack()
    root.mainloop()

if __name__ == '__main__':
    start()