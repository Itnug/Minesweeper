'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import tkinter as tk
from main.model import Minesweeper
from main.model import State
import logging

W = 10
H = 10
B = 10
CS = 20
FLAG_VECTOR = [4,2,16,2,16,20,14,20,14,10,10,10]

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
        self.covers = [None]*(W*H)
        self.flags = [None]*(W*H)
        for j in range(H):
            for i in range(W):
                self.canvas.create_rectangle(i*CS, j*CS, (i+1)*CS, (j+1)*CS)
                self.canvas.create_text(i*CS + CS // 2, j*CS + CS // 2, text = str(self.model.clues[j*W + i]).replace("0", " "))
                self.covers[j*W + i] = self.canvas.create_rectangle(i*CS, j*CS, (i+1)*CS, (j+1)*CS, fill='grey')
                
                
        
    def peek(self, event):
        logging.debug(event.__dict__)
        logging.debug(event.x)
        logging.debug(event.y)
        logging.debug('left')
        
        if self.model.game_over:
            return
        x = event.x // CS
        y = event.y // CS
        self.model.peek(x, y)
        self.update_view()
    
    def flag(self, event):
        logging.debug(event.__dict__)
        logging.debug(event.x)
        logging.debug(event.y)
        logging.debug('right')
        if self.model.game_over:
            return
        x = event.x // CS
        y = event.y // CS
        self.model.flag(x, y)
        self.update_view()
    

    def update_view(self):
        widgets = self.canvas.find_all();
        for x in range(W):
            for y in range(H):
                i = y*W + x
                if self.model.gridstate[i] == State.KNOWN:
                    if self.covers[i] in widgets:
                        self.canvas.delete(self.covers[i])
                
                if self.model.gridstate[i] == State.FLAGGED:
                    if self.flags[i] not in widgets:
                        X = x*CS 
                        Y = y*CS
                        self.flags[i] = self.canvas.create_polygon(*FLAG_VECTOR, fill='red')
                        self.canvas.move(self.flags[i], X, Y)
                elif self.flags[i] in widgets:
                    self.canvas.delete(self.flags[i])
            
        if self.model.game_over:
            for y in range(H):
                for x in range(W):
                    i = y*W + x
                    if self.model.clues[i] == Minesweeper.BOMB:
                        if self.model.gridstate[i] == State.EXPLODED:
                            self.canvas.create_oval(x*CS + 3, y*CS + 3, (x+1)*CS - 3, (y+1)*CS - 3, fill='black')
                        if self.model.gridstate[i] == State.UNKNOWN:
                            self.canvas.create_oval(x*CS + 3, y*CS + 3, (x+1)*CS - 3, (y+1)*CS - 3, fill='black')
                                  
            self.canvas.create_text(W*CS // 2 + 1 , H*CS // 2 - 1, fill="black", font=("consolas",22), text="Game Over")
            self.canvas.create_text(W*CS // 2 - 1 , H*CS // 2 + 1, fill="black", font=("consolas",22), text="Game Over")
            self.canvas.create_text(W*CS // 2 - 1 , H*CS // 2 - 1, fill="black", font=("consolas",22), text="Game Over")
            self.canvas.create_text(W*CS // 2 + 1 , H*CS // 2 + 1, fill="black", font=("consolas",22), text="Game Over")
            self.canvas.create_text(W*CS // 2, H*CS // 2, fill="white", font=("consolas",22), text="Game Over")
            
if __name__ == '__main__':
    root = tk.Tk()
    App(root).pack()
    root.mainloop()




#Keyframe editor: (DO LATER)

#Displays mouse x and y on workspace:



