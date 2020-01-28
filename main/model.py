'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import logging
import random
from itertools import compress

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class State(object):
    UNKNOWN = 0
    KNOWN = 1
    FLAGGED = 2
    EXPLODED = 3
    
class Minesweeper(object):
    BOMB = 9 
    
    def __init__(self, difficulty):
        self.x = difficulty.width
        self.y = difficulty.height
        self.bombs = difficulty.bombs

        self._size = self.x * self.y
        self.flags = self.bombs
        self.clues = [0]*(self._size)
        self.gridstate = [State.UNKNOWN]*(self._size)
        
        self.game_over = False
        
    def place_bomb(self, i):
        if self.clues[i] == Minesweeper.BOMB:
            logger.warning(f'Cannot place. Bomb already present at {i}')
        self.clues[i] = Minesweeper.BOMB
        for nbr in self.get_neighbors(i):
            if self.clues[nbr] != Minesweeper.BOMB:
                self.clues[nbr] += 1
    
    def first_peek(self, i):
        population = [i for j in (range(i), range(i+1, self._size)) for i in j]
        for j in random.sample(population, self.bombs):
                self.place_bomb(j)

        self.peek(i)
        logger.warning(self)
    
    def peek(self, i):
        if self.gridstate[i] == State.FLAGGED:
            logger.debug('Cannot peek')
            return
        if self.clues[i] == Minesweeper.BOMB:
            self.gridstate[i] = State.EXPLODED
            self.game_over = True
            self.win = False
        elif self.gridstate[i] == State.UNKNOWN:
            self.gridstate[i] = State.KNOWN
            if self.clues[i] == 0:
                #no bombs in the nbd. safely check them all
                for nbr in self.get_neighbors(i):
                    self.peek(nbr)
        elif self.gridstate[i] == State.KNOWN:
            nbr_flags = 0
            for nbr in self.get_neighbors(i):
                if self.gridstate[nbr] == State.FLAGGED:
                    nbr_flags += 1
            if nbr_flags == self.clues[i]: #if all flags have been placed correctly
                for nbr in self.get_neighbors(i): # it safe to peek all unknown nbrs
                    if self.gridstate[nbr] == State.UNKNOWN:
                        self.peek(nbr)
        if self.gridstate.count(State.KNOWN) == self._size - self.bombs:
            for j in range(self._size):
                if self.gridstate[j] == State.UNKNOWN:
                    self.flag(j)
            self.game_over = True
            self.win = True
                
    def flag(self, i):
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
            logger.warning("Cannot Flag")

    def get_neighbors(self, i):
        row = i // self.x
        col = i % self.x
        X, Y = 1, self.x
        
        bounds_filter = [col>0 and row>0, row>0, col<self.x-1 and row>0,
                        col>0, col<self.x-1,
                        col>0 and row<self.y-1, row<self.y-1, col<self.x-1 and row<self.y-1]
                
        nbd = [i-X-Y, i-Y, i+X-Y,
                i-X,        i+X,
               i-X+Y, i+Y, i+X+Y]
        
        return compress(nbd, bounds_filter)
        
    def __str__(self):
        return '\n'.join([' '.join(map(str,self.clues[i:i+self.x])) for i in range(0, len(self.clues), self.x)]) 

if __name__ == '__main__':
    class Difficulty(object):
        pass
    difficulty = Difficulty() 
    difficulty.width = 10
    difficulty.height = 10
    difficulty.bombs = 10
    print(Minesweeper(difficulty))  