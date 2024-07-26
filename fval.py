# efficiently evaluate the function value
from args import ARGS
import numpy as np
from util import *

def fun(x, args):
    # compute the objective value
    clauses, weight, klist, ctype, FC_table = args[0], args[1], args[2], args[3], args[4]
    if ARGS.objectiveType == "abs":
        cardtotal = sum(weight[k]* np.abs( 0.5 * (1 + np.dot(cardcons([j/abs(j)*x[abs(j)-1] for j in clauses[k]]),CardinalityFC(len(clauses[k]),klist[k])))) for k in range(len(clauses)) if (ctype[k]=='c'))
        xortotal = sum(weight[k] * np.abs( 0.5 * (1 + prod(j/abs(j)*x[abs(j)-1] for j in clauses[k]))) for k in range(len(clauses)) if (ctype[k]=='x'))
    elif ARGS.objectiveType == "square":
        cardtotal = sum(weight[k] * np.square( 0.5 * (1 + np.dot(cardcons([j/abs(j)*x[abs(j)-1] for j in clauses[k]]),CardinalityFC(len(clauses[k]),klist[k])))) for k in range(len(clauses)) if (ctype[k]=='c'))
        xortotal = sum(weight[k] * np.square( 0.5 * (1 + prod(j/abs(j)*x[abs(j)-1] for j in clauses[k]))) for k in range(len(clauses)) if (ctype[k]=='x'))
    elif ARGS.objectiveType == "linear":
        cardtotal = sum(weight[k] * ( 0.5 * (1 + np.dot(cardcons([j/abs(j)*x[abs(j)-1] for j in clauses[k]]),CardinalityFC(len(clauses[k]),klist[k])))) for k in range(len(clauses)) if (ctype[k]=='c'))
        xortotal = sum(weight[k] * 0.5 * (1 + prod(j/abs(j)*x[abs(j)-1] for j in clauses[k])) for k in range(len(clauses)) if (ctype[k]=='x'))

    #naetotal = sum(weight[k] * np.dot(cardcons([j / abs(j) * x[abs(j) - 1] for j in clauses[k]]),
                                     #NAEFC(len(clauses[k]))) for k in range(len(clauses)) if (ctype[k] == 'n'))
    # CNFs are viewed as special cardinality constraints

    # add the barrier objective forcing x^2=1 for all variable x
    fval = cardtotal + xortotal
    for i in range(len(x)):
        fval += (ARGS.beta * np.square(1-x[i]*x[i]))
    return fval

