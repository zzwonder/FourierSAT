from FourierCoefficient import *
from util import *
from args import ARGS

def gradient(x,args):
    # compute the gradient of the objective value
    clauses, weight, klist, ctype, FC_table  = args[0],args[1],args[2], args[3], args[4]
    grad = [0 for i in range(len(x))]
    for k in range(len(clauses)):
        clause = clauses[k]
        if ctype[k] == 'c':
            clause_value = 0.5 * (1 + np.dot(cardcons([j/abs(j)*x[abs(j)-1] for j in clause]), CardinalityFC(len(clause),klist[k])))
            temp_grad = grad_BP(clause,x,klist[k],ctype[k],FC_table[k])
        elif ctype[k] == 'x':
            clause_value = 0.5 * (1 + prod(j/abs(j)*x[abs(j)-1] for j in clause))
            temp_grad = grad_BP_XOR(clause,x,klist[k],ctype[k],FC_table[k])
        if ARGS.objectiveType == "abs":
            if clause_value < 0: temp_grad = [ - temp_grad[kk] for kk in range(len(temp_grad))]
        elif ARGS.objectiveType == "square":
            temp_grad = [  2 * temp_grad[kk] * clause_value for kk in range(len(temp_grad))]
        for i in range(len(clause)):
            grad[abs(clause[i])-1] += weight[k] * temp_grad[i]
    if ARGS.beta > 1e-4:
        for i in range(len(x)):
            grad[i] -= (ARGS.beta * 4 * x[i] * (1-x[i] * x[i]))
    return np.array(grad)

# the following two functions efficiently compute the gradient for cardinality and XOR constraints.
def grad_BP_XOR(clause,x,k,ctype,FC_table):
    grad = []
    nv = len(clause)
    forward_message = []
    backward_message = []
    forward_message.append(1)
    backward_message.append(1)
    x_prime = [ x[abs(clause[i])-1] * (clause[i]/abs(clause[i])) for i in range(len(clause))]
    for i in range(1,nv):
        forward_message.append(forward_message[i-1] * x_prime[i-1])
        backward_message.append(backward_message[i-1] * x_prime[nv-i])
    for i in range(1,1+nv):
        grad.append(abs(clause[i-1])/clause[i-1] * forward_message[i-1] * backward_message[nv-i])
    return grad


def grad_BP(clause,x,k,ctype,FC_table):
    grad = []
    nv = len(clause)
    coef = [FC_table[ci] for ci in range(1,len(clause)+1)]
    if nv < 40:
        for i in clause:
            x_rest = [xi/abs(xi)*x[abs(xi)-1] for xi in clause if xi!=i]
            esps = cardcons(x_rest)
            grad.append(np.dot(coef,esps) * (abs(i)/i))
        return grad
    esps= [] # Elementary symetric Polymomials
    x_prime = [ -x[abs(clause[i])-1] * (clause[i]/abs(clause[i])) for i in range(len(clause))]
    forward_message = []
    backward_message = []
    forward_message.append([1])
    backward_message.append([1])
    for i in range(1,nv):
        forward_message.append(np.polymul(forward_message[i-1],poly1d([x_prime[i-1]],True)))
        backward_message.append(np.polymul(backward_message[i-1],poly1d([x_prime[nv-i]],True)))
    for i in range(1,nv+1):
        esps.append(np.polymul(forward_message[i-1],backward_message[nv-i]))
    for i in range(nv):
        grad.append(np.dot(coef,esps[i].c) * (abs(clause[i])/clause[i]))
    return grad

