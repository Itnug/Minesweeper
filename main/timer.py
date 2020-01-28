'''
Created on 28-Jan-2020

@author: Srinivas Gunti
'''
from time import time, sleep


_transitions = {
    'start': ['pause', 'stop'],
    'pause': ['unpause', 'stop'],
    'unpause': ['pause', 'stop'],
    'stop': ['start'],
    }

def transition(func):
    action = func.__name__
    def wrapper(self, *args, **kwargs):
        if action in self.available_actions:
            func(self,*args, **kwargs)
            self.available_actions = _transitions[action]
#             print(f'performed {repr(action)}. new actions available are {self.available_actions}')
#         else:
#             print(f'Blocked!. {repr(action)} not available. choose from {self.available_actions}')
    return wrapper
    

class Timer(object):
    
    def __init__(self, max_time=999):
        self.available_actions = ['start']
        self.max_time = max_time
        self._start = None
        self.total = None
    
    @transition
    def start(self):
        self._start = time()
        self.total = None
    
    @transition    
    def pause(self):
        self.total = time() - self._start 
        self.total = min(self.max_time, self.total)
    
    @transition             
    def unpause(self):
        self._start = time() - self.total
        self.total = None
    
    @transition
    def stop(self):
        self.total = time() - self._start 
        self.total = min(self.max_time, self.total)
        self._start = None
        
    def get_time(self):
        if self.total:
            return self.total
        elif self._start:
            return min(self.max_time, time() - self._start)
        else:
            return 0

if __name__ == '__main__':
    t= Timer()
    t.pause()
    t.unpause()
    t.stop()
    t.start()    

    t.start()
    t.unpause()
    t.pause()
    
    t.start()
    t.unpause()
    
    t.stop()
    
    t.start()
    for i in range(6):
        sleep(1)
        print(t.get_time())
    t.pause()
    for i in range(6):
        sleep(1)
        print(t.get_time())
    t.unpause()
    for i in range(6):
        sleep(1)
        print(t.get_time())
    t.stop()
    for i in range(6):
        sleep(1)
        print(t.get_time())
        