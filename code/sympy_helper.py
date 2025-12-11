# See https://stackoverflow.com/questions/49145059/how-to-change-printed-representation-of-functions-derivative-in-sympy
from sympy.printing.latex import LatexPrinter
from sympy.core.function import UndefinedFunction
from sympy import Symbol, Function, latex

class MyLatexPrinter(LatexPrinter):
    """Print derivatives in shorter format.

    * Derivatives dependent on variable `t` are printed with a dot.
    * More complicated derivatives revert to the default SymPy behaviour.

    """
    def __init__(self, t):
        super().__init__()
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

