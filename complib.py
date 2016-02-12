import itertools
import random
from collections import namedtuple


UNDEF = None
Output = namedtuple('Output', ['value', 'steps'])


class Function():
    def __init__(self, name, f):
        self.name = name
        self.f = f
        
    @classmethod
    def from_graph(cls, name, graph):
        """
            Returns a function by its finite graph.
            
            The graph is represented as a set of triples of the form <i,o,t> 
            meaning that the function on input `i` returns `o` in `t` steps.
        """
        m = {}
        for i,o,t in graph:
            assert(i >= 0 and o >= 0 and t >= 1)
            m[i] = Output(o, t)
        def inner(n):
            try:
                result = m[n]
            except KeyError:
                result = UNDEF
            return result
        return Function(name, inner)

    def graph(self, start, offset):
        """
            Returns the graph of this function only considering inputs in the 
            range [`start`, `start`+`offset`).
        """
        g = set()
        for i in xrange(start, start+offset):
            output = self.f(i)
            if output is not UNDEF:
                g.add((i, output.value, output.steps))
        return g

    def domain(self, start=0, offset=10):
        """
            Returns the domain of this function only considering inputs in the
            range [`start`, `start`+`offset`).
        """
        g = self.graph(start, offset)
        return set([i for i,_,_ in g])

    def range(self, start=0, offset=10):
        """
            Returns the range of this function only considering inputs in the
            range [`start`, `start`+`offset`).
        """
        g = self.graph(start, offset)
        return set([o for _,o,_ in g])

    def pp_graph(self, start=0, offset=10):
        """
            Prints the graph of this function only considering inputs in the
            range [`start`, `start`+`offset`).
        """
        for i in xrange(start, start+offset):
            output = self.f(i)
            print "{}({}) =".format(self, i),
            if output is not UNDEF:
                print "{} in {} steps".format(output.value, output.steps)
            else:
                print "undefined"

    def __call__(self, i, steps=None, on_undef="abort"):
        """
            Returns the output of running this function on input `i` for `steps` steps.
            
            If the behaviour of this function is undefined for input `i`, then 
            if `on_undef` is set to "abort" the program is terminated, otherwise
            None is returned.
        """
        assert(i >= 0)
        assert(steps is None or steps >= 1)
        
        output = self.f(i)
        if output is UNDEF: # If the function would not terminate on this input.
            if steps is None:
                # If no steps have been specified, loop forever.
                print "{}({}) runs forever!".format(self, i)
                if on_undef == "abort":
                    exit(1)
            # Otherwise, return None.
            return None
        elif steps is None or output.steps <= steps:
            # If the function would terminate on this input and no steps or
            # enough steps have been provided, return its output.
            return output.value
        
        # In all other cases return None.
        return None
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def T3(f, i, t):
    """
        Kleene's predicate of arity three.
        Returns `True` iff f(i) terminates in at most `t` steps.
    """
    return f(i, steps=t) is not None


def T4(f, i, o, t):
    """
        Kleene's predicate of arity four.
        Returns `True` iff `f(i) outputs `o` in at most `t` steps.
    """
    output = f(i, steps=t)
    return (output is not None and output == o)


def dovetailing(f, stop_predicate):
    """
        Runs function f on all inputs for any number of steps.
        Whenever the function terminates on input i producing o within t steps 
        the predicate stop_predicate(i,o,t) is executed. If it returns `True`
        this function stops and returns `True`, otherwise this function keeps 
        running potentially forever.
    """
    for t in itertools.count(1):
        for i in xrange(t):
            print "Running function {} on input {} for {} steps.".format(f, i, t),
            o = f(i, steps=t)
            if o is not None:
                print "It halts returning {}.".format(o)
                if stop_predicate(i,o,t):
                    print "Stop predicate returned `True`, thus dovetailing ends."
                    return True
            else:
                print "It does not halt."


def dovetailing_on_pairs(f, stop_predicate):
    """
        Runs function f on all possible pairs of inputs for any number of steps.
        Whenever the function terminates on inputs i and j producing outputs oi 
        and oj within t steps the predicate stop_predicate(i,oi,j,oj,t) is executed. 
        If it returns `True` this function stops and returns `True`, otherwise 
        this function keeps running potentially forever.
    """
    for t in itertools.count(1):
        for i in xrange(t):
            for j in xrange(t):
                print "Running function {} on inputs {} and {} for {} steps.".format(f, i, j, t),
                oi = f(i, steps=t)
                oj = f(j, steps=t)
                if oi is None and oj is None:
                    print "It does not halt on either input."
                elif oi is None:
                    print "It does not halt on input {}.".format(i)
                elif oj is None:
                    print "It does not halt on input {}.".format(j)
                elif stop_predicate(i, oi, j, oj, t):
                    print "Halts on both."
                    print "Stop predicate returned `True`, thus dovetailing ends."
                    return True
                else:
                    print "Halts on both, but stop predicate returned `False`."


# =============
# | Encodings |
# =============

def pair2number(a,b):
    d = a+b
    return (d*(d+1))/2 + a

def number2pair(n):
    if n == 0:
        return (0,0)
    a,b = number2pair(n-1)
    if b == 0:
        return (0, a+1)
    return (a+1, b-1)

def pair2first(n):
    return number2pair(n)[0]

def pair2second(n):
    return number2pair(n)[1]


# =======================
# | Function generators |
# =======================

# Generator of constant functions.
def K(k, steps=1, name=None):
    """
        Returns the constant `k` function, that is, a function 
        that returns `k` on each input in `steps` steps.
    """
    assert(steps >= 1)
    if name is None:
        name = "K{}_{}_steps".format(k, steps)
    return Function(name, lambda n: Output(k, steps))


# =====================
# | Utility functions |
# =====================

# Always undefined function.
undef = Function("undef", lambda n: UNDEF)

# Identity function.
ident = Function("ident", lambda n: Output(n,1))

# Successor function.
succ = Function("succ", lambda n: Output(n+1, 1))

# Constant functions.
K0 = K(0, name="K0")
K1 = K(1, name="K1")