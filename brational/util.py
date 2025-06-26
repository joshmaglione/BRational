#
#   Copyright 2024--2025 Joshua Maglione
#
#   Distributed under MIT License
#

from enum import Enum
from datetime import datetime
from functools import reduce
import re

DEBUG = False

def my_print(on:bool, string:str, level:int=0):
    if on:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}]" + "\t"*level + f" {string}")

# Return True if and only if at least two inputs are True.
def at_least_two(A:bool, B:bool, C:bool) -> bool:
    return A*B + A*C + B*C > 0

# Given an expression for a numerator, determine if we need to wrap with
# parentheses.
def parenthesis_wrap(expr:str) -> str:
    for l, m, r in zip(expr, expr[1:], expr[2:]):
        if l == '(':
            return expr
        if l + m + r in [" + ", " - "]:
            return f"({expr})"
    return expr

# The length of the function name is unnecessarily long.
def remove_unnecessary_braces_and_spaces(latex_text):
	patt_braces = re.compile(r'[\^\_]\{.\}')
	patt_spaces = re.compile(r'[0-9] [a-zA-Z0-9]')
	patt_spaces2 = re.compile(r'\} [a-zA-Z0-9]')
	def remove_braces(match):
		return f"{match.group(0)[0]}{match.group(0)[2]}"
	def remove_spaces(match):
		return match.group(0)[0] + match.group(0)[2]
	pairs = [
		(patt_braces, remove_braces), 
		(patt_spaces, remove_spaces), 
		(patt_spaces2, remove_spaces)
	]
	return reduce(lambda x, y: y[0].sub(y[1], x), pairs, latex_text)

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
