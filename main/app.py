'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import tkinter as tk
from main.model import Minesweeper
from main.model import State
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

W = 10
H = 10
B = 10
CS = 20
FLAG_VECTOR = [4,2,16,2,16,20,14,20,14,10,10,10]

WIN_TEXT = 'You Win!!'
LOSS_TEXT = 'Game Over'

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.canvas = tk.Canvas(self, width=W * CS, height=H * CS, highlightthickness=0)
        self.canvas.bind('<Button-1>', self.peek)
        self.canvas.bind('<Button-3>', self.flag)
        self.canvas.pack()
        
        self.model = Minesweeper(W,H)
        logging.debug(self.model)
        self.view = [{'x':i % W, 'y':i // W} for i in range(W * H)]
        for i, cell in enumerate(self.view):
            X = cell['x'] * CS 
            Y = cell['y'] * CS
            clue_str = str(self.model.clues[i]).replace("0", " ")
            
            cell['frame'] = self.canvas.create_rectangle(X, Y, X + CS, Y + CS)
            cell['clue'] = self.canvas.create_text(X + CS // 2, Y + CS // 2, text=clue_str)
            cell['cover'] = self.canvas.create_rectangle(X, Y, X + CS, Y + CS, fill='grey')
            cell['flag'] = None
            cell['bomb'] = None
                
    def peek(self, event):
        logger.debug(f'({event.x},{event.y})')
        logger.debug('left click')
        
        if self.model.game_over:
            return
        x = event.x // CS
        y = event.y // CS
        self.model.peek(x, y)
        self.update_view()
    
    def flag(self, event):
        logger.debug(f'({event.x},{event.y})')
        logger.debug('right click')
        
        if self.model.game_over:
            return
        x = event.x // CS
        y = event.y // CS
        self.model.flag(x, y)
        self.update_view()
    

    def draw_ending_text(self, ending_text):
        X = W * CS // 2
        Y = H * CS // 2
        self.canvas.create_text(X + 1, Y - 1, fill="black", font=("consolas", 22), text=ending_text)
        self.canvas.create_text(X - 1, Y + 1, fill="black", font=("consolas", 22), text=ending_text)
        self.canvas.create_text(X - 1, Y - 1, fill="black", font=("consolas", 22), text=ending_text)
        self.canvas.create_text(X + 1, Y + 1, fill="black", font=("consolas", 22), text=ending_text)
        self.canvas.create_text(X, Y, fill="white", font=("consolas", 22), text=ending_text)

    def update_view(self):
        for i, cell in enumerate(self.view):
            X = cell['x']*CS 
            Y = cell['y']*CS
            
            if self.model.gridstate[i] == State.KNOWN:
                if cell['cover']:
                    self.canvas.delete(cell['cover'])
                    cell['cover'] = None
                    
            if self.model.gridstate[i] == State.FLAGGED:
                if not cell['flag']:
                    cell['flag'] = self.canvas.create_polygon(*FLAG_VECTOR, fill='red')
                    self.canvas.move(cell['flag'], X, Y)
            elif cell['flag']:
                self.canvas.delete(cell['flag'])
                cell['flag'] = None
                
            if self.model.game_over and self.model.clues[i] == Minesweeper.BOMB:
                if self.model.gridstate[i] == State.EXPLODED:
                    cell['bomb'] = self.canvas.create_oval(3, 3, CS - 3, CS - 3, fill='black')
                    self.canvas.move(cell['bomb'], X, Y)
                if self.model.gridstate[i] == State.UNKNOWN:
                    cell['bomb'] = self.canvas.create_oval(3, 3, CS - 3, CS - 3, fill='black')
                    self.canvas.move(cell['bomb'], X, Y)

        if self.model.game_over:              
            if self.model.win:
                self.draw_ending_text(WIN_TEXT)
            else:                
                self.draw_ending_text(LOSS_TEXT)
            
if __name__ == '__main__':
    root = tk.Tk()
    App(root).pack()
    root.mainloop()




#Keyframe editor: (DO LATER)

#Displays mouse x and y on workspace:



