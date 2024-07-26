import random

def randomkConstraints(n, k, alpha, Ctype="CNF"):
    number_of_instances = 10
    for instance in range(number_of_instances):
        num_of_clauses = int(alpha * n)
        filename = Ctype + "_" + repr(n) + "_" + repr(alpha) + "_" + repr(instance) + ".txt"
        with open("randomInstances/2CNF_1000/" + filename, "w+") as f:
            f.write("p cnf " + repr(n) + " " + repr(num_of_clauses) + "\n")
            for clause_num in range(num_of_clauses):
                if Ctype == "XOR": f.write("x ")
                clause = random.sample(range(1,n+1), k)
                for literal in clause:
                    if random.randint(0,1) == 0: 
                        f.write(repr(literal))
                    else: f.write(repr(-literal))
                    f.write(" ")
                f.write("0 \n")


def generateRand(n,k,alphaList, Ctype):
    n = 1000
    k = 3
    for alpha_T10 in alphaList:
        alpha = alpha_T10 * 1.0 / 10
        randomkConstraints(n, k, alpha, Ctype)

#generateRand(1000, 3, range(10,42,2), "CNF")
#generateRand(1000, 3, range(1,10,1), "XOR")
#generateRand(1000, 2, range(1,10,1), "CNF")
generateRand(1000, 2, [9.5], "CNF")
                
            
