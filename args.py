
class ARGS:
    clauses = []
    weight = []
    klist = []
    ctype = []
    FC_table = {}
    objectiveType = "square"
    beta = 0
    weight_update_factor = 0
    trial_no = 0
    ismaxsat = 0
    unconstrained = 1
    maxTrial = 10
    mode = 'dev'
    
def setArgs(clauses=[], weight=[], klist=[], ctype=[], FC_table={}, objectiveType = "square", beta = 0, weight_update_factor = 0, optimizer="SLSQP", unconstrained = 0, ismaxsat = 0, maxTrial = 10, mode = 'dev'):
    ARGS.clauses = clauses
    ARGS.weight = weight
    ARGS.klist = klist
    ARGS.ctype = ctype
    ARGS.FC_table = FC_table
    ARGS.objectiveType = objectiveType
    ARGS.beta = beta
    ARGS.weight_update_factor = weight_update_factor
    ARGS.optimizer = optimizer
    ARGS.unconstrained = unconstrained
    ARGS.ismaxsat = ismaxsat
    ARGS.maxTrial = maxTrial
    ARGS.mode = mode
    print("unconstrained = " + repr(unconstrained))
    print("maxsat mode = " + repr(ismaxsat))
    print("objective type = " + objectiveType)
    print("beta = " + repr(beta))
    print("weight update factor = " + repr(weight_update_factor))
    print("optimizer = " + optimizer)
    print("maxTrial = " + repr(maxTrial))
    print("mode = " + repr(mode))

def increase_ARGS_seed():
    ARGS.trial_no += 1

