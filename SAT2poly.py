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
        assert ctype[i] == 'c' or ctype[i] == 'x'
        if ctype[i] == 'c':
            k = len(constraint)
            assert klist[i] == 1 # only cnf and xor constraints are supported
            for lstr in constraint:
                # check whether the literal is positive or negative
                l = int(lstr)
                if l > 0:
                    polyTerm.append( "(0.5 + 0.5 * x[:,%d])" % (l - 1))
                else:
                    polyTerm.append( "(0.5 - 0.5 * x[:,%d])" % ( abs(l) - 1))
            tempStr = (" * ".join(poly for poly in polyTerm))
        elif ctype[i] == 'x':
            k = len(constraint)
            for lstr in constraint:
                l = int(lstr)
                if l < 0:
                    polyTerm.append( "(-x[:,%d])" % ( abs(l) - 1))
                else:
                    polyTerm.append( "x[:,%d]" % ( l - 1))
            tempStr = (" * ".join(poly for poly in polyTerm))
            tempStr = '0.5 * (' + tempStr + ' + 1)'
        if objectiveType == "abs":
            terms.append(repr(weight[i]) + " * torch.abs(%s)" % tempStr)
        elif objectiveType == "square":
            terms.append(repr(weight[i]) + " * torch.square(%s)" % tempStr)
        #if form == "bounded":   # the bounded formulation needs to be optimized on the [0,1]^n cube
        #    terms.append(tempStr)
        else:
            raise ValueError("unrecognized objectiveType: " + objectiveType)
    resStr =  (" + ".join(term for term in terms))
    for i in range(nv):
        if beta > 0:
            resStr += (" + %f * torch.square(x[:,%d] - x[:,%d] * x[:,%d]) " % (beta, i, i, i))    
        if beta < 0:
            resStr += (" %f * torch.square(x[:,%d] - x[:,%d] * x[:,%d]) " % (beta, i, i, i))    
    return resStr
