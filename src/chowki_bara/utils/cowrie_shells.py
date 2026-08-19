# (0) Docstring
"""Contains utility functions and other utility objects for the project."""


# (1) Imports
import random as r
import math as m
from numbers import Real


# (2) "Cowrie Shells" object and methods
class CowrieShells:
    """Object class for cowrie shells. 
    Accepts (3) optional args:
    - [num: int >= 1] to pass the number of cowrie shell pieces, 
    - [nudge: Real 0 >= nudge >= 1] to pass the probability of one side, and 
    - [zm: int >= 0] to pass the multiplier to [num] to return [num]*[zm] if return of [object].roll() is 0 (default=2). 
    Has (1) method: 
    - [object].roll()"""
    
    # (2.1) "Initialization" method
    def __init__(self, num=4, nudge=0.5, zm=2):
        self.num = num
        self.nudge = nudge
        self.zm = zm
        
        # (2.1.1) Error Handling
        if (not isinstance(num, int)) or (num < 1):
            raise ValueError("[num] should be a non-zero, positive integer.")
            
        if not isinstance(nudge, Real) or not (0 <= nudge <= 1):
            raise ValueError("[nudge] should be a float and should satisfy 0 <= [nudge] <= 1.")
            
        if (not isinstance(zm, int)) or (zm < 0):
            raise ValueError("[zm] should be an integer, greater than or equal to zero.")
        
    # (2.2) "roll" method
    def roll(self, times=1) -> list[int]:
        """Method to roll the shells. 
        Accepts (1) optional arg: 
        - [times: int >= 1] to pass the number of rolls to perform (default=1). 
        
        Returns a list."""
        
        # (2.2.1) Error Handling
        if not ((isinstance(times, int)) and (times >= 1)):
            raise ValueError("[times] should be a non-zero positive integer.")
        
        # (2.2.2) Machinery
        num = self.num
        nudge = self.nudge
        zm = self.zm
        
        index = 0
        results = []
        
        for i in range(times):
            result = 0
            
            for k in range(num):
                rand = r.random()
                got = 1 if rand <= nudge else 0
                result += got
                
            result = num*zm if result == 0 else result
            
            results.append(result)
            
        return results