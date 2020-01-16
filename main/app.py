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
        self.model = Minesweeper(W, H)
        logging.debug(self.model)

        self.view = MinesweeperView(self, self.model)
        self.view.canvas.bind('<Button-1>', self.peek)
        self.view.canvas.bind('<Button-3>', self.flag)
        self.view.canvas.pack()        
        
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


if __name__ == '__main__':
    root = tk.Tk()
    App(root).pack()
    root.mainloop()
