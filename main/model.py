'''
Created on 27-Apr-2017

@author: Srinivas Gunti
'''
import logging
import random
import time
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
    DIFFICULTY = 10
    
    def __init__(self, difficulty):
        self.x = difficulty.width
        self.y = difficulty.height
        self.bombs = difficulty.bombs

        self._size = self.x * self.y
        self.flags = self.bombs
        self.clues = [0]*(self._size)
        self.gridstate = [State.UNKNOWN]*(self._size)
        
        for i in random.sample(range(self._size), self.bombs):
            self.place_bomb(i)
        
        self.game_over = False
        self.start_time = None
        self.stop_time = None
        
    def place_bomb(self, i):
        if self.clues[i] == Minesweeper.BOMB:
            logger.warning(f'Cannot place. Bomb already present at {i}')
            return False
        self.clues[i] = Minesweeper.BOMB
        for nbr in self.get_neighbors(i):
            if self.clues[nbr] != Minesweeper.BOMB:
                self.clues[nbr] += 1
        return True
    
    def remove_bomb(self, i):
        if self.clues[i] != Minesweeper.BOMB:
            logger.warning(f'Cannot remove. No bomb at {i}')
            return False
        self.clues[i] = 0
        for nbr in self.get_neighbors(i):
            if self.clues[nbr] != Minesweeper.BOMB:
                self.clues[nbr] -= 1
            else:
                self.clues[i] += 1
        return True
    
    def first_peek(self, x, y):
        self.start_timer()
        i = y * self.x + x
        if self.clues[i] == Minesweeper.BOMB:
            j = 0
            while not self.place_bomb(j):
                j += 1
            self.remove_bomb(i)
        self.peek(x, y)
        logger.warning(self)
                    
    def peek(self, x, y):
        self.peek_by_index(y*self.x + x)
        if self.gridstate.count(State.KNOWN) == self._size - self.bombs:
            for i in range(self._size):
                if self.gridstate[i] == State.UNKNOWN:
                    self.flag_by_index(i)
            self.game_over = True
            self.win = True
            self.stop_timer()
    
    def peek_by_index(self, i):
        if self.gridstate[i] == State.FLAGGED:
            logger.debug('Cannot peek')
            return
        if self.clues[i] == Minesweeper.BOMB:
            self.gridstate[i] = State.EXPLODED
            self.game_over = True
            self.win = False
            self.stop_timer()
        elif self.gridstate[i] == State.UNKNOWN:
            self.gridstate[i] = State.KNOWN
            if self.clues[i] == 0:
                #no bombs in the nbd. safely check them all
                for nbr in self.get_neighbors(i):
                    self.peek_by_index(nbr)
        elif self.gridstate[i] == State.KNOWN:
            nbr_flags = 0
            for nbr in self.get_neighbors(i):
                if self.gridstate[nbr] == State.FLAGGED:
                    nbr_flags += 1
            if nbr_flags == self.clues[i]: #if all flags have been placed correctly
                for nbr in self.get_neighbors(i): # it safe to peek all unknown nbrs
                    if self.gridstate[nbr] == State.UNKNOWN:
                        self.peek_by_index(nbr)
                
    def flag(self, x,y):
        self.start_timer()
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
                
    def start_timer(self):
        if not self.start_time:
            self.start_time = time.time()
            
    def stop_timer(self):
        if self.start_time and not self.stop_time:
            self.stop_time = time.time()

    def get_time(self):
        if not self.start_time:
            return 0
        elif not self.stop_time:
            return min(999, int(time.time() - self.start_time))
        else:
            return min(999, int(self.stop_time - self.start_time))
        
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