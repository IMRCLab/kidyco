# See https://stackoverflow.com/questions/49145059/how-to-change-printed-representation-of-functions-derivative-in-sympy
from sympy.printing.latex import LatexPrinter
from sympy.core.function import UndefinedFunction
from sympy import Symbol, Function, Eq, latex, cse

from sympy.printing.rust import rust_code
from sympy.printing.pycode import pycode
from sympy import ccode
from sympy.codegen.ast import Assignment

class MyLatexPrinter(LatexPrinter):
    """Print derivatives in shorter format.

    * Derivatives dependent on variable `t` are printed with a dot.
    * More complicated derivatives revert to the default SymPy behaviour.

    """
    def __init__(self, t, latex_symbol_names=dict()):
        super().__init__({"symbol_names": latex_symbol_names})
        self.t = t

    def _print_Function(self, expr: Function, exp=None) -> str:
        if len(expr.args) == 1 and expr.args[0] == self.t:
            return super()._print_Function(expr, exp).replace(r"{\left(t \right)}","")
        else:
            return super()._print_Function(expr, exp)

    def _print_Derivative(self, expr):
        f, *vars = expr.args
        if (not (vars[0][0] == self.t)
                or not isinstance(type(f), UndefinedFunction)
                or not (isinstance(f.args[0], Symbol)
                        or isinstance(type(f.args[0]), UndefinedFunction))
                or not len(vars)==1):
            # If `expr` is anything other than a simple UndefinedFunction or
            # Symbol, dependent on a single variable `t` or `x`, then revert
            # to the standard SymPy behaviour:
            return super()._print_Derivative(expr)

        order = vars[0][1]  # Which order derivative? 1st, 2nd, 3rd, etc.
        f = self._print(Symbol(f.func.__name__))  # Function being derived.
        v = self._print(vars[0][0])  # Independent variable.
        if vars[0][0] == self.t:
            # Print derivatives w.r.t. `t` as dots:
            return f"\\{order * 'd'}ot{{{f}}}" #({v})"
        else:
            raise Exception("Unexpected error...")
        
    def show(self, expr):
        print('$$\n%s\n$$\n' % self.doprint(expr))

    def showEq(self, var, expr):
        print('$$\n{} = {}\n$$\n'.format(var, self.doprint(expr)))

    def showEqArray(self, l):
        print("\\begin{aligned}\n")
        for var, expr in l:
            print("{} &= {}\\\\\n".format(var, self.doprint(expr)))
        print("\\end{aligned}\n")

    def showSubs(self, l):
        print("\\begin{aligned}\n")
        for var, expr in l:
            print("{} &= {}\\\\\n".format(self.doprint(var), self.doprint(expr)))
        print("\\end{aligned}\n")

    def showAllSubs(self, l):
        print("\n\n")
        print("::: {.panel-tabset group='language'}\n")
        print("## Math\n")
        self.showSubs(l)
        print("## C\n")
        print("``` {.c}")
        for var, expr in l:
            assign_stmt = Assignment(var, expr)
            print(ccode(assign_stmt))
        print("```\n")
        print("## Rust\n")
        print("``` {.rust}")
        for var, expr in l:
            assign_stmt = Assignment(var, expr)
            print(rust_code(assign_stmt))
        print("```\n")
        print("## Python\n")
        print("``` {.python}")
        for var, expr in l:
            assign_stmt = Assignment(var, expr)
            print(pycode(assign_stmt))
        print("```\n")
        print(":::\n\n")

    def showAllCode(self, expr):
        print("\n\n")
        print("::: {.panel-tabset group='language'}\n")
        print("## Math\n")
        self.show(expr)
        print("## C\n")
        print("``` {.c}")
        print(ccode(expr))
        print("```\n")
        print("## Rust\n")
        print("``` {.rust}")
        print(rust_code(expr))
        print("```\n")
        print("## Python\n")
        print("``` {.python}")
        print(pycode(expr))
        print("```\n")
        print(":::\n\n")
   
        

