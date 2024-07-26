from scipy import poly1d
from FourierCoefficient import *


def norm(x):
    return sum([x[i]*x[i] for i in range(len(x))])

def prod(iterable):
    p= 1
    for n in iterable:
        p *= n
    return p

def truncate(x):
    xnew = [xi for xi in x]
    for i in range(len(xnew)):
        if xnew[i] > 1: xnew[i] = 1
        elif xnew[i] < -1: xnew[i] = -1
    return xnew

def cardcons(x):
    templist = [-x[i] for i in range(len(x))]
    poly = poly1d(templist,True)
    return poly.c

def rounding(x):
    xnew = [xi for xi in x]
    for i in range(len(x)):
        if xnew[i]>0: xnew[i]=1
        else: xnew[i]=-1
    return xnew

def count(x):
    x = rounding(x)
    return (len(x)-sum(x))//2

def modify_weight(weight,formula,x,klist):
    x = rounding(x)
    return weight

def project(x):
    for i in range(len(x)):
        if x[i]>1:
            x[i] = 1
        elif x[i]<-1:
            x[i]=-1
    return x

def compute_FC_table(clauses,klist,ctype,coefs,comparator):
    FC_table = []
    for k in range(len(clauses)):
        if ctype[k]=='c':
            FC_table.append(CardinalityFC(len(clauses[k]),klist[k]))
        elif ctype[k]=='x':
            n = len(clauses[k])
            l = [0 for i in range(n)]
            l.append(1)
            FC_table.append(l) #place holder
        elif ctype[k]=='n':
            FC_table.append(NAEFC(len(clauses[k])))
    return FC_table

def outSideBox(x):
    count = 0
    for xi in x:
        if abs(xi) > 1.01: count+=1


def print_assignment(x):
    roundingx = rounding(x)
    print('v '),
    for i in range(len(bestx)):
        print(repr(int(-1*bestx[i]*(i+1)))+' '),
    print('\n')
