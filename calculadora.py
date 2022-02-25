from lark import Lark, Transformer, v_args
import operator

@v_args(inline=True)
class CalcTranformer(Transformer):
    from operator import add, mul, sub, truediv as div, pow

    def INT(self, tk):
        return int(tk)

    def FLOAT(self, tk):
        return float(tk)

    def start(self, elem):
        return elem

GRAMMAR = r"""
start : expr

?expr : expr "+" term   -> add
      | expr "-" term   -> sub
      | term
      
?term : term "*" elem   -> mul
      | term "/" elem   -> div
      | elem
      
?elem : atom  "^" elem   -> pow
      | atom
      
?atom : INT
      | FLOAT
      | "(" expr ")"
      
INT   : ("0" .. "9")+
FLOAT : INT "." INT
NAME  : ("a" .. "z")+

%ignore " "
"""

lark = Lark(GRAMMAR, transformer=CalcTranformer(), parser="lalr")

def eval(st: str):
    return lark.parse(st)

for ex in [
    "40 + 2",
    "40 * 2",
    "42",
    "1 + 2 + 3",
    "5 + 2 * 3",
    "10 ^ 3 ^ 2",
    "2 ^ 3 * 3 ^ 2"
]:
    print(ex + " =", eval(ex))