'''
Created on 15-Jan-2020

@author: Srinivas Gunti
'''
import unittest
import tkinter as tk
from main.app import App
from main.model import State
import atexit
from collections import namedtuple

class AppTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.testapp = App(None)
        
    def test_added_to_app_flags_when_flagged(self):
        self.testapp.model.clues[0] = 0 #make it so it has no bombs
        self.testapp.model.gridstate[0] = State.UNKNOWN #make it so it can be flag-able
        event = tk.Event()
        event.x = 10
        event.y = 10
        self.testapp.flag(event) #make a flag
        self.assertIsNotNone(self.testapp.flags[0], "flagged a cell, polygon not saved in flags")

    def test_removed_from_app_flags_when_unflagged(self):
        self.testapp.model.clues[0] = 0 #make it so it has no bombs
        self.testapp.model.gridstate[0] = State.UNKNOWN #make it so it can be flag-able
        event = tk.Event()
        event.x = 10
        event.y = 10
        self.testapp.flag(event) #make a flag
        self.testapp.flag(event) #unmake a flag
        self.assertFalse(self.testapp.flags[0] in self.testapp.canvas.find_all(),
                          "unflagged a cell, but flags has " + str(self.testapp.flags[0]))

if __name__ == "__main__":
    unittest.main()