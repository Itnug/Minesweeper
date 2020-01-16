'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import random

class State(object):
    UNKNOWN = 0
    KNOWN = 1
    FLAGGED = 2
    EXPLODED = 3
    
class Minesweeper(object):
    BOMB = 9 
    
    def __init__(self, x, y=None, bombs=None):
        if not y: y = x
        if not bombs: bombs = x*y//10
        
        self.x = x
        self.y = y
        self._size = x * y
        self.bombs = bombs
        self.flags = bombs
        self.clues = [0]*(self._size)
        self.gridstate = [State.UNKNOWN]*(self._size)
        
        for place in random.sample(range(self._size), bombs):
            self.clues[place] = Minesweeper.BOMB
        self.update_clues()
        self.game_over = False
        
    def update_clues(self):
        for i in range(self._size):
            if self.clues[i] == Minesweeper.BOMB:
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
                if condition and self.clues[i+nbr] == Minesweeper.BOMB:
                    self.clues[i]+=1
                    
    def peek(self, x, y):
        self.peek_by_index(y*self.x + x)
        if self.gridstate.count(State.KNOWN) == self._size - self.bombs:
            for i in range(self._size):
                if self.gridstate[i] == State.UNKNOWN:
                    self.flag_by_index(i)
            self.game_over = True
            self.win = True
    
    def peek_by_index(self, i):
        if self.clues[i] == Minesweeper.BOMB:
            self.gridstate[i] = State.EXPLODED
            self.game_over = True
            self.win = False
        elif self.gridstate[i] == State.UNKNOWN:
            self.gridstate[i] = State.KNOWN
            if self.clues[i] == 0:
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
                        self.peek_by_index(i+nbr)
                
    def flag(self, x,y):
        self.flag_by_index(y*self.x + x)
        
    def flag_by_index(self, i):
        if self.gridstate[i] == State.UNKNOWN:
            if not self.flags:
                print("out of flags")
                return
            self.gridstate[i] = State.FLAGGED
            self.flags -= 1
        elif self.gridstate[i] == State.FLAGGED:
            self.gridstate[i] = State.UNKNOWN
            self.flags += 1
        else:
            print("Cannot Flag")

            
    def __str__(self):
        return '\n'.join([' '.join(map(str,self.clues[i:i+self.x])) for i in range(0, len(self.clues), self.x)]) 

if __name__ == '__main__':
    print(Minesweeper(10))  