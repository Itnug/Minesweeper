'''
Created on 16-Jan-2020

@author: Srinivas Gunti
'''
from main.model import State

FLAG_VECTOR = [4, 2, 16, 2, 16, 20, 14, 20, 14, 10, 10, 10]

WIN_TEXT = 'You Win!!'
LOSS_TEXT = 'Game Over'


class MinesweeperView(object):
    CS = 20
        
    def __init__(self, app):
        self.app = app
        self.model = app.model
        
        W = self.model.x
        H = self.model.y
        
        self.header = app.header_canvas
        self.header.config(width=W * self.CS, height=1 * self.CS, bg='#33B5E5', highlightthickness=0)
        
        self.flags = self.header.create_text(self.CS//4, self.CS//2, anchor='w')
        self.timer = self.header.create_text(W*self.CS - self.CS//4, self.CS//2, anchor='e')
        self.canvas = app.canvas
        self.canvas.config(width=W * self.CS, height=H * self.CS, highlightthickness=0)        
        self.cells = [{'x':i % W, 'y':i // W} for i in range(W * H)]
        for i, cell in enumerate(self.cells):
            X = cell['x'] * self.CS
            Y = cell['y'] * self.CS
            clue_str = str(self.model.clues[i]).replace("0", " ")
            
            cell['frame'] = self.canvas.create_rectangle(X, Y, X + self.CS, Y + self.CS)
            cell['clue'] = self.canvas.create_text(X + self.CS // 2, Y + self.CS // 2, text=clue_str)
            cell['cover'] = self.canvas.create_rectangle(X, Y, X + self.CS, Y + self.CS, fill='grey')
            cell['flag'] = None
            cell['bomb'] = None
            
        self.update()
        
    def update_clues(self):
        for i, cell in enumerate(self.cells):
            self.canvas.itemconfig(cell['clue'], text=str(self.model.clues[i]).replace("0", " "))
            
    def update(self):
        self.header.itemconfig(self.flags, text=f'Flags: {self.model.flags}')
        for i, cell in enumerate(self.cells):
            X = cell['x'] * self.CS 
            Y = cell['y'] * self.CS
            
            if self.model.gridstate[i] == State.KNOWN:
                if cell['cover']:
                    self.canvas.delete(cell['cover'])
                    cell['cover'] = None
                    
            if self.model.gridstate[i] == State.FLAGGED:
                if not cell['flag']:
                    cell['flag'] = self.canvas.create_polygon(*map(lambda x: x*self.CS/20, FLAG_VECTOR), fill='red')
                    self.canvas.move(cell['flag'], X, Y)
            elif cell['flag']:
                self.canvas.delete(cell['flag'])
                cell['flag'] = None
                
            if self.model.game_over and self.model.clues[i] == self.model.BOMB:
                if self.model.gridstate[i] == State.EXPLODED:
                    cell['bomb'] = self.canvas.create_oval(3, 3, self.CS - 3, self.CS - 3, fill='black')
                    self.canvas.move(cell['bomb'], X, Y)
                if self.model.gridstate[i] == State.UNKNOWN:
                    cell['bomb'] = self.canvas.create_oval(3, 3, self.CS - 3, self.CS - 3, fill='black')
                    self.canvas.move(cell['bomb'], X, Y)

        if self.model.game_over:              
            if self.model.win:
                self.draw_ending_text(WIN_TEXT)
            else:                
                self.draw_ending_text(LOSS_TEXT)
    
    def draw_ending_text(self, ending_text):
        X = self.model.x * self.CS // 2
        Y = self.model.y * self.CS // 2
        self.canvas.create_text(X + 1, Y - 1, fill="black", font=("consolas", 22), text=ending_text)
        self.canvas.create_text(X - 1, Y + 1, fill="black", font=("consolas", 22), text=ending_text)
        self.canvas.create_text(X - 1, Y - 1, fill="black", font=("consolas", 22), text=ending_text)
        self.canvas.create_text(X + 1, Y + 1, fill="black", font=("consolas", 22), text=ending_text)
        self.canvas.create_text(X, Y, fill="white", font=("consolas", 22), text=ending_text)
    
    def update_timer(self):
        self.header.itemconfig(self.timer, text=f'time: {int(self.app.timer.get_time()):03}')
        
