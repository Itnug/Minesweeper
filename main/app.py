'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import logging

from main.model import Minesweeper
from main.view import MinesweeperView
import tkinter as tk

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Overrides:
# MinesweeperView.CS = 30

W = 10
H = 10
B = 10


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
        difficulty_submenu.add_radiobutton(label="Easy", command=lambda: self.set_difficulty(10))
        difficulty_submenu.add_radiobutton(label="Medium", command=lambda: self.set_difficulty(8))
        difficulty_submenu.add_radiobutton(label="Hard", command=lambda: self.set_difficulty(6))
        options_menu.add_cascade(label='Difficulty', menu=difficulty_submenu, underline=0)
        
        size_submenu = tk.Menu(options_menu, tearoff=0)
        size_submenu.add_radiobutton(label='small', command=lambda: self.set_size(10))
        size_submenu.add_radiobutton(label='medium', command=lambda: self.set_size(20))
        size_submenu.add_radiobutton(label='large', command=lambda: self.set_size(30))
        options_menu.add_cascade(label='Size', menu=size_submenu, underline=0)
         
        menubar.add_cascade(label='Options', menu=options_menu)
        
        parent.config(menu=menubar)
        
        self.header_canvas = tk.Canvas(parent)
        self.canvas = tk.Canvas(parent)
        self.canvas.bind('<Button-1>', self.peek)
        self.canvas.bind('<Button-3>', self.flag)
        
        self.new_game()
        self.update_clock()
        
    def new_game(self):
        self.header_canvas.delete("all")
        self.canvas.delete("all")
        
        self.model = Minesweeper(W, H)
        self.first_peek = True
        logging.debug(self.model)

        self.view = MinesweeperView(self.header_canvas, self.canvas, self.model)
        self.header_canvas.pack()
        self.canvas.pack()
    
    def set_difficulty(self, n):
        '''one bomb for every n cells'''
        Minesweeper.DIFFICULTY = n
        self.new_game()
    
    def set_size(self, n):
        '''n width and n height'''
        global W
        global H
        W = n
        H = n
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