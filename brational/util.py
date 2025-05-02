#
#   Copyright 2024--2025 Joshua Maglione
#
#   Distributed under MIT License
#

from enum import Enum
from datetime import datetime

DEBUG = True

def my_print(on:bool, string:str, level:int=0):
    if on:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}]" + "\t"*level + f" {string}")

# Return True if and only if at least two inputs are True.
def at_least_two(A:bool, B:bool, C:bool) -> bool:
    return A*B + A*C + B*C > 0

class brat_type(Enum):      
    #                           p.d. = positive degree 
    #                           n.d. = non-negative degree
    # 
    INTEGER = "i"               # num: int,         den: 1
    RATIONAL = "r"              # num: int,         den: int
    INTEGRAL_POLY = "ip"        # num: poly p.d.,   den: 1
    RATIONAL_POLY = "rp"        # num: poly p.d.,   den: int
    INTEGRAL_L_POLY = "ilp"     # num: poly n.d.,   den: monic monomial p.d.
    RATIONAL_L_POLY = "rlp"     # num: poly n.d.,   den: monomial p.d.
    RATIONAL_FUNC = "rf"        # num: poly n.d.,   den: poly p.d.
