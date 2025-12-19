import cvc5
from cvc5 import Kind
#from cvc5.pythonic import *

#   # Create solver
#   solver = cvc5.Solver()
#   solver.setOption("tlimit", "5000")
#   solver.setOption("rlimit", "5000000")
#   solver.setOption("sygus", "true")
#   solver.setLogic("LRA")  # Linear Real Arithmetic
#   # Define sorts
#   real_sort = solver.getRealSort()
#   bool_sort = solver.getBooleanSort()
#   # Define variables
#   x = solver.mkVar(real_sort, "x")
#   y = solver.mkVar(real_sort, "y")
#   z = solver.mkVar(real_sort, "z")
#   # Define grammar
#   bool_term = solver.mkVar(bool_sort, "BoolTerm")
#   real_term = solver.mkVar(real_sort, "RealTerm")
#   thresh_term = solver.mkVar(real_sort, "ThreshTerm")
#   bool_productions = [
#       solver.mkTerm(Kind.LEQ, real_term, thresh_term),
#       solver.mkTerm(Kind.GEQ, real_term, thresh_term),
#       solver.mkTerm(Kind.AND, bool_term, bool_term),
#       solver.mkTerm(Kind.NOT, bool_term),
#       solver.mkTerm(Kind.OR, bool_term, bool_term),
#   ]
#   thresh_productions = [
#       solver.mkReal(-1),
#       solver.mkReal(0),
#       solver.mkReal(0.5),
#       solver.mkReal(1),
#       solver.mkReal(2),
#       solver.mkTerm(Kind.ADD, thresh_term, thresh_term),
#       solver.mkTerm(Kind.MULT, thresh_term, thresh_term)
#   ]
#   real_productions = [
#       x, y, z,
#       #solver.mkTerm(Kind.ADD, real_term, real_term),
#       #solver.mkTerm(Kind.SUB, real_term, real_term),
#   ]
#solver = None

def real_val(solver, v):
        return solver.mkReal(str(round(v, 4)))
    
def turntoValues(solver, values):
    return [real_val(solver, val) for val in values]

# examples := [[True, w1, w2, d1,d2,d3], [True, w1, w2, d1,d2,d3], [...]]
def turnexampleValues(solver, examples):
    examplevalues = []
    for ex in examples:
        b = solver.mkBoolean(bool(ex[0]))
        examplevalues.append([*turntoValues(solver, ex[3:]), b])
    return examplevalues





# exList:= [[]]
# cmprfct:= [[function1, threshhold1], [function2, threshhold2]]

#Synth(Ggbf(Na,Nd), Esyn, F)
def synth(exList:list, cmprfct:list = []):
    
    
    
    
    #create solver
    solver = cvc5.Solver()
    #solver.setOption("tlimit", "5000")
    solver.setOption("rlimit", "500000")

    solver.setOption("sygus", "true")
    solver.setLogic("LRA")  # Linear Real Arithmetic

    # Define sorts
    real_sort = solver.getRealSort()
    bool_sort = solver.getBooleanSort()

    # Define variables
    var = []
    ch = ord('a')
    for i in range(0, len(exList[0])-3):
        var.append(solver.mkVar(real_sort, chr(ch + i)))
        
        

    # Define grammar
    bool_term = solver.mkVar(bool_sort, "BoolTerm")
    real_term = solver.mkVar(real_sort, "RealTerm")
    thresh_term = solver.mkVar(real_sort, "ThreshTerm")

    bool_productions = [
        #option 1; valueas comparable
        solver.mkTerm(Kind.LEQ, real_term, thresh_term),
        solver.mkTerm(Kind.GEQ, real_term, thresh_term),
        solver.mkTerm(Kind.AND, bool_term, bool_term),
        solver.mkTerm(Kind.NOT, bool_term),
        
        #option 2; values only comparable with self
        #solver.mkTerm(Kind.LEQ, real_term, thresh_term),
        #solver.mkTerm(Kind.GEQ, real_term, thresh_term),
        #solver.mkTerm(Kind.AND, thresh_term, thresh_term),
        #solver.mkTerm(Kind.AND, bool_term, thresh_term),
        
        
        ##solver.mkTerm(Kind.OR, bool_term, bool_term),
    ]

    thresh_productions = [
        solver.mkReal(-1),
        solver.mkReal(0),
        solver.mkReal(0.5),
        solver.mkReal(1),
        solver.mkReal(3),
        solver.mkReal(10),
        solver.mkReal(100),
        solver.mkTerm(Kind.ADD, thresh_term, thresh_term),
        solver.mkTerm(Kind.MULT, thresh_term, thresh_term)
    ]

    #for ex in exList:
    #    for e in ex[3:]:
    #        thresh_productions.append(real_val(solver, e))
    
    real_productions = [
        *var,
        #solver.mkTerm(Kind.ADD, real_term, real_term),
        #solver.mkTerm(Kind.SUB, real_term, real_term),
        #solver.mkTerm(Kind.MULT, real_term, thresh_term),
    ]

    grammar = solver.mkGrammar(var, [bool_term, real_term, thresh_term])
    
    grammar.addRules(bool_term, bool_productions)
    grammar.addRules(real_term, real_productions)
    grammar.addRules(thresh_term, thresh_productions)

    # Function to synthesize
    f = solver.synthFun("f", var, bool_sort, grammar)
    
    
    
    # load examples
    examples = turnexampleValues(solver, exList)
    
    # TESTING
    examples2 = [
        #[real_val(solver, 1.5), solver.mkBoolean(True)],
        #[real_val(solver, 1.5), solver.mkBoolean(False)],
        #[real_val(solver, 1.5), solver.mkBoolean(True)],
        [real_val(solver, 1.0), solver.mkBoolean(True)],
        #[real_val(solver, 1.0), solver.mkBoolean(True)],
        #[real_val(solver, 2.0), solver.mkBoolean(True)],
        [real_val(solver, 2.0), solver.mkBoolean(False)],
        #[real_val(solver, -5.0), solver.mkBoolean(True)],
        #[real_val(solver, -5.0), solver.mkBoolean(True)],
    ]
    
    #print(examples)
    for values in examples:
        app = solver.mkTerm(Kind.APPLY_UF, f, *values[:-1])
        solver.addSygusConstraint(solver.mkTerm(Kind.EQUAL, app, values[-1]))
    
    # Solve
    #print("Starting synthesis...")
    res = solver.checkSynth()

    if res.hasSolution():
        solver.checkSat()
        
        #print("Synthesized function:")

        fun = solver.getSynthSolution(f)
        #print(fun)
        return [solver, fun]

        app = solver.mkTerm(Kind.APPLY_UF, fun, real_val(1.0), real_val(2.0), real_val(1.5))
        print(solver.getValue(app))
        app2 = solver.mkTerm(Kind.APPLY_UF, fun, real_val(3.0), real_val(1.0), real_val(1.5))
        print(solver.getValue(app2))
    else:
        return None
        print("No solution found.")


# check if values are valid under solver
# vars := [x, y, z, [...]] unmodified number
# return True/False if yes/no
def verify(solver, fun, vars):
    app = solver.mkTerm(Kind.APPLY_UF, fun, *turntoValues(solver, vars))
    #tmp = solver.getValue(app)
    #print(tmp)
    #tmp2 =  str(solver.getValue(app)) == 'true' 
    return str(solver.getValue(app)) == 'true'


# check all entries of posEx and negEx in solver
# return all non-fitting examples
def VerifyExamples(solver, fun, posEx, negEx):
    inval = []
    
    for ex in posEx:
        if not verify(solver, fun, ex[2:]):
            inval.append([True, *ex])
            
    for ex in negEx:
        if verify(solver, fun, ex[2:]):
            inval.append([False, *ex])
    
    return inval





lsit = [
    [True, 'w', 'v', 1.0, 2.0],
    [True, 'w', 'v', 4.0, 2.9],
    [False, 'ww', 'vv', 2.0, 1.0],
    [False, 'ww', 'vv', 2.0, 4.0],
]
#print(synth(lsit))
