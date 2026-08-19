# (0) Docstring
"""Contains several decorators to be used throughout the proiect."""


# (1) Imports
from functools import wraps
import inspect


# (2) Type Error Handling Decorator
def requireType(**kwargs):
    
    def type_decorator(func):
        signature = inspect.signature(func)
        
        for i in kwargs:
            if i not in signature.parameters:
                raise ValueError(f"{i!r} is not a parameter of {func.__name__}.")
        
        # (2.1) 'wrapper' function, which replaces 'func'
        @wraps(func)
        def wrapper(*xargs, **xkwargs):
            bound = signature.bind(*xargs, **xkwargs)
            
            for i in kwargs:
                if i not in bound.arguments:
                    continue
                    
                if not isinstance(bound.arguments[i], kwargs[i]):
                    err_msg = f"{i} must be {kwargs[i].__name__}, got {type(bound.arguments[i]).__name__}."
                    raise TypeError(err_msg)
            
            return func(*xargs, **xkwargs)
            
        return wrapper
        
    return type_decorator
                    

# (3) Range Error Handling Decorator
def requireRange(**kwargs):
    
    def range_decorator(func):
        signature = inspect.signature(func)
        
        for i in kwargs:
            if i not in signature.parameters:
                raise ValueError(f"{i!r} is not a parameter of {func.__name__}.")
        
        # (3.1) 'wrapper' function, which replaces 'func'
        @wraps(func)
        def wrapper(*xargs, **xkwargs):
            bound = signature.bind(*xargs, **xkwargs)
            
            for i in kwargs:
                if i not in bound.arguments:
                    continue
                    
                v = kwargs[i]
                value = bound.arguments[i]
                
                if not isinstance(v, str):
                    raise TypeError(f"Expected a 'str' but got '{type(v).__name__}'.")
                
                # (3.1.1) Parser for the custom notation    
                halfTokens = v.split(",")
                brace_1 = halfTokens[0][0]
                brace_2 = halfTokens[1][-1]
                num_1 = float(halfTokens[0][1:])
                num_2 = float(halfTokens[1][:-1])
                   
                if brace_1 == '[':
                    val_1 = value >= num_1
                elif brace_1 == '(':
                    val_1 = value > num_1
                
                if brace_2 == ']':
                    val_2 = value <= num_2
                elif brace_2 == ')':
                    val_2 = value < num_2
                    
                if not (val_1 and val_2):
                    raise ValueError(f"{i!r} should lie in the interval {v}.")
            
            return func(*xargs, **xkwargs)
            
        return wrapper
    
    return range_decorator
                   