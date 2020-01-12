'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import random

class Minesweeper(object):
    BOMB = 9 
    
    #states
    UNKNOWN = 0
    KNOWN = 1
    FLAGGED = 2
    EXPLODED = 3
    SAFE = 4
     
    def __init__(self, x, y=None, bombs=None):
        if not y: y = x
        if not bombs: bombs = x*y//10
        
        self.x = x
        self.y = y
        self._size = x * y
        self.flags = bombs
        self.grid = [0]*(self._size)
        self.gridstate = [Minesweeper.UNKNOWN]*(self._size)
        
        for place in random.sample(range(self._size), bombs):
            self.grid[place] = Minesweeper.BOMB
        self.update_clues()
        
        
    def update_clues(self):
        for i in range(self._size):
            if self.grid[i] == Minesweeper.BOMB:
                continue
            row = i // self.x
            col = i % self.x
            
            conditions = [col>0 and row>0, row>0, col<self.x-1 and row>0,
                          col>0, col<self.x-1,
                          col>0 and row<self.y-1, row<self.y-1, col<self.x-1 and row<self.y-1]
            X, Y = 1, self.x
            
            nbd = [-X-Y, -Y, X-Y,
                   -X,       X,
                   -X+Y, Y, X+Y]
            for nbr, condition in zip(nbd, conditions):
                if condition and self.grid[i+nbr] == Minesweeper.BOMB:
                    self.grid[i]+=1
                    
    def test(self, x, y):
        self.test_by_index(y*self.x + x)
    
    def test_by_index(self, i):
        if self.grid[i] == Minesweeper.BOMB:
            self.gridstate = Minesweeper.EXPLODED
        elif self.gridstate[i] == Minesweeper.UNKNOWN:
            self.gridstate[i] = Minesweeper.KNOWN
            if self.grid[i] == 0:
                #no bombs in the nbd. safely check them all
                row = i // self.x
                col = i % self.x
                
                conditions = [col>0 and row>0, row>0, col<self.x-1 and row>0,
                              col>0, col<self.x-1,
                              col>0 and row<self.y-1, row<self.y-1, col<self.x-1 and row<self.y-1]
                X, Y = 1, self.x
                
                nbd = [-X-Y, -Y, X-Y,
                       -X,       X,
                       -X+Y, Y, X+Y]
                for nbr, condition in zip(nbd,conditions):
                    if condition:
                        self.test_by_index(i+nbr)
                
    def toggle_flag(self, x,y):
        self.toggle_flag_by_index(y*self.x + x)
        
    def toggle_flag_by_index(self, i):
        if self.gridstate[i] == Minesweeper.UNKNOWN:
            self.gridstate[i] = Minesweeper.FLAGGED
            self.flags -= 1
        elif self.gridstate[i] == Minesweeper.FLAGGED:
            self.gridstate[i] = Minesweeper.UNKNOWN
            self.flags += 1
        else:
            print("Cannot Flag")

            
    def __str__(self):
        return '\n'.join([' '.join(map(str,self.grid[i:i+self.x])) for i in range(0, len(self.grid), self.x)]) 

if __name__ == '__main__':
    print(Minesweeper(10))  