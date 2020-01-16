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
        logging.debug(self.model)

        self.view = MinesweeperView(self.header_canvas, self.canvas, self.model)
        self.header_canvas.pack()
        self.canvas.pack()
                
    def peek(self, event):
        logger.debug(f'({event.x},{event.y})')
        logger.debug('left click')
        
        if self.model.game_over:
            return
        x = event.x // self.view.CS
        y = event.y // self.view.CS
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
        

if __name__ == '__main__':
    root = tk.Tk()
    App(root).pack()
    root.mainloop()
