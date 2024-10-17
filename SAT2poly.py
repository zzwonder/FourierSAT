import math
import argparse
from boolean_formula import Formula

# transform a SAT formula into a polynomial for HJProx and Torch
def SAT2PolyStr(args, nv, objectiveType = "square", beta = 0):
    clauses, weight, klist, ctype, FC_table = args[0], args[1], args[2], args[3], args[4]
    terms = []
    polyStr = ""
    for i in range(len(clauses)):
        constraint = clauses[i]
        polyTerm = []
        k = len(constraint)
        for lstr in constraint:
            # check whether the literal is positive or negative
            l = int(lstr)
            if l > 0:
                polyTerm.append( "(1-x[:,%d])" % (l - 1))
            else:
                polyTerm.append( "x[:,%d]" % ( abs(l) - 1))
        tempStr = (" * ".join(polyTerm[i] for i in range(len(polyTerm))))
        if objectiveType == "abs":
            terms.append("torch.abs(%s)" % tempStr)
        elif objectiveType == "square":
            terms.append("torch.square(%s)" % tempStr)
        #if form == "bounded":   # the bounded formulation needs to be optimized on the [0,1]^n cube
        #    terms.append(tempStr)
        else:
            raise ValueError("unrecognized objectiveType: " + objectiveType)
    resStr =  (" + ".join(terms[i] for i in range(len(terms))))
    if beta > 0:
        for i in range(nv):
            resStr += (" + %f torch.square(x[:,%d] - x[:,%d] * x[:,%d]) " % (beta, i, i, i))    
    return resStr

def polyCNFFile(cnffile, form):
    return cnf2poly(form, cnffile, inputFile=True)

