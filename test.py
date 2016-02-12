if __name__ == '__main__':
    import complib
    import itertools
    

    # f(0) = 1 in 3 steps
    # f(1) = 7 in 1 steps
    # f(n>1) = undefined
    f = complib.Function.from_graph(
        name="f",
        graph=set([
            (0,1,3),
            (1,7,1)
        ])
    )

    # g(0) = 5 in 1 steps
    # g(n>0) = undefined
    g = complib.Function.from_graph(
        name="g",
        graph=set([
            (0,5,1)
        ])
    )

    # Print the graphs of all functions in the range [0,10).
    print "Graph of function f:"; f.pp_graph()
    print "Graph of function g:"; g.pp_graph()
    print "Graph of function K0:"; complib.K0.pp_graph()
    print "Graph of function ident:"; complib.ident.pp_graph()
    print "Graph of function undef:"; complib.undef.pp_graph()
    
    print "Function f(0) halts in 1 step:", complib.T3(f,0,1)
    print "Function g(0) halts in 1 step:", complib.T3(g,0,1)
    print "Function K0(0) halts in 1 step:", complib.T3(complib.K0,0,1)
    print "Function ident(0) halts in 1 step:", complib.T3(complib.ident,0,1)
    print "Function undef(0) halts in 1 step:", complib.T3(complib.undef,0,1)

    # Extract the graphs of all functions in the range [0,3).
    print "Graph of function f:", f.graph(0,3)
    print "Graph of function g:", g.graph(0,3)
    print "Graph of function K0:", complib.K0.graph(0,3)
    print "Graph of function ident:", complib.ident.graph(0,3)
    print "Graph of function undef:", complib.undef.graph(0,3)
    
    # Print the output value of all functions on input 0.
    print "f(0) =", f(0)
    print "g(0) =", g(0)
    print "K0(0) =", complib.K0(0)
    print "ident(0) =", complib.ident(0)
    
    # This would run forever, setting on_undef to "continue" does not terminate
    # the program but is not a realistic behaviour. It is impossibile in general
    # to understand whether a program will terminate on a given input or not.
    print "undef(0) =",
    complib.undef(0, on_undef="continue")
    
    # A bunch of semi-deciders for sets of programs.
    
    # Semi-deciders for the set { i | 7 in cod(phi_i) }.
    def sd1_1(f):
        for t in itertools.count(1):
            for k in range(0, t):
                print "Running function {} on input {} for {} steps.".format(f, k, t)
                output = f(k, steps=t)
                if output is not None and output == 7:
                    print "On this input it returns 7!"
                    return True
    
    def sd1_2(f):
        return complib.dovetailing(f, lambda i,o,t: o == 7)

    # Semi-deciders for the set { (i,y) | exists a,b. a != b, phi_i(a) halts and phi_i(a) = phi_i(b) }.
    def sd2_1(f):
        s = set()
        for t in itertools.count(1):
            for k in range(0, t):
                print "Running function {} on input {} for {} steps.".format(f, k, t)
                output = f(k, steps=t)
                if output is not None:
                    # If this output was produced in the past by running `f` on
                    # a different input, output `True` and stop.
                    for inv, outv in s:
                        if inv != k and outv == output:
                            print "This function returns {} on inputs {} and {}!".format(output, inv, k)
                            return True
                    # Otherwise, record that `f` outputs `output` when ran on input k.
                    print "Recording that {}({}) = {}.".format(f, k, output)
                    s.add((k, output))
                else:
                    print "{}({}) did not terminate in {} steps.".format(f, k, t)

    def sd2_2(f):
        return complib.dovetailing_on_pairs(f, lambda i,oi,j,oj,t: i != j and oi == oj)
    
    # Apply the semi-deciders to some functions.
    sd1_1(f)
    sd1_2(f)
    sd1_1(complib.ident)
    sd1_2(complib.ident)
    
    # k12_3_steps(i) = 12 in 3 steps.
    k12_3_steps = complib.K(12, 3)

    sd2_1(k12_3_steps)
    sd2_2(k12_3_steps)

    # Test encodings of the pairs.
    print "Encoding and decoding of pairs as natural numbers:"
    for i in xrange(10):
        p = complib.number2pair(i)
        n = complib.pair2number(*p)
        print i, "->", p, "->", n