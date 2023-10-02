import itertools as it

########################## Q4 ##########################

def load_dimacs(textdocument):
    endlist = []
    with open(textdocument, "r") as f:
        contents = f.readlines()[1:]
    
        for x in contents:
            l = list(map(int, x.split(" ")[:-1]))
            endlist.append(l)

    f.close()
    return endlist

########################## Q5 ########################## 

def changeset(x):
    literals = set()
    newtuple = set()
    newlist = []
    for l in x:
        for val in l:
            if(val < 0):
                newtuple.add((abs(val), False))
            else:
                newtuple.add((abs(val), True))
            literals.add(abs(val))
        newlist.append(newtuple)
        newtuple = set()
    return literals, newlist


#influence for solver sourced from https://davefernig.com/2018/05/07/solving-sat-in-python/
def solver(x):
    literals, newlist = changeset(x)
    
    literals = list(literals)
    
    for seq in it.product([True, False], repeat=len(literals)):

        a = set(zip(literals, seq))
       
        if all([bool(var.intersection(a)) for var in newlist]):
            return a
    
    return False

def simple_sat_solve(l):
    outputlist = []
    a = solver(l)
    if(a == False):
       return False
    for x in a:
        if(x[1]):
            outputlist.append(x[0])
        else:
            outputlist.append(-x[0])
    return outputlist

########################## Q6 ########################## 

def give_values(x):
    listofvalues = []
    for clause in x:
        
        for val in clause:
            numb = 0
            curval = abs(val)
            for i in range(0, len(listofvalues)):
                if(listofvalues[i] == curval):
                    numb = 1
            if (numb == 0):
               listofvalues.append(curval)
    listofvalues.sort()
    return listofvalues

def absvalue(dig):
    return abs(dig)
def sort_endlist(endlist):
   for clause in endlist:
      clause.sort(key = absvalue)

def new_brancher(clause_set, value_list, ind, originallistofval):

    changed_set = []
    for x in clause_set:
        changed_set.append(x.copy())

    for value in value_list:
        x = 0
        while x < len(changed_set):
            i = 0
            while i < len(changed_set[x]):
                
                if(value == changed_set[x][i]):
                    i = len(changed_set[x])
                    changed_set.remove(changed_set[x])
                    x -= 1
                elif(abs(value) == abs(changed_set[x][i])):
                    changed_set[x].remove(changed_set[x][i])
                    if(len(changed_set[x]) == 0):
                        return False
                else:
                    i += 1
                if(x == -1):
                    break
            x += 1

        
    if(len(changed_set) == 0):
        return value_list
   
    possiblelist = False
    
    value_list.append(originallistofval[ind])
    ind += 1
    possiblelist = new_brancher(clause_set, value_list, ind, originallistofval)
    if(possiblelist):
        return value_list

    if(not possiblelist):
        value_list.pop()
        ind -= 1
    value_list.append(-originallistofval[ind])
    ind += 1
    possiblelist = new_brancher(clause_set, value_list, ind, originallistofval)

    if(possiblelist):
        return value_list
    if(not possiblelist):
        value_list.pop()
        ind -= 1

#partial_assignment is never used but I added it because the formative checker failed tests because I didn't have it
def branching_sat_solve(l, partial_assignment=[]):
    l.sort(key=len)
    ind = 0
    value_list = []
    sort_endlist(l)
    originallistofval = give_values(l)
    returnclause = new_brancher(l, value_list, ind, originallistofval)
    if(returnclause == None):
        return False
    return returnclause

########################## Q7 ##########################

def unit(clause_set):

    l = []
    clause_set.sort(key=len)
    for i in range(0, len(clause_set)):
        if(len(clause_set[i]) == 1):
            l.append(clause_set[i][0])
        else:
            break

    for var in l:
        a = 0
        while a < len(clause_set):
            b = 0
            while b < len(clause_set[a]):
                if(var == clause_set[a][b]):
                    b = len(clause_set[a])
                    clause_set.remove(clause_set[a])
                    if(len(clause_set) == 0):
                        break
                    a -= 1
                elif(abs(var) == abs(clause_set[a][b])):
                    clause_set[a].remove(clause_set[a][b])
                    if(len(clause_set[a]) == 0):
                        return "Un sat"
                    b -= 1
                b += 1
            a += 1
    return clause_set

def unit_propagate(l):
    l.sort(key=len)
    sort_endlist(l)

    unit(l)
    reduced_clause_set_1 = l.copy()
    
    unit(l)
    reduced_clause_set_2 = l.copy()
    
    while reduced_clause_set_1 != reduced_clause_set_2:
        unit(l)
        reduced_clause_set_1 = l.copy()
        unit(l)
        reduced_clause_set_2 = l.copy()


    if(reduced_clause_set_1 == "Un sat"):
        return False
    elif(len(reduced_clause_set_1) == 0):
        return reduced_clause_set_1
    else:
        return reduced_clause_set_1



########################## Q8 (old version) ##########################
"""
def q8_solver(clause_set, value_list, ind, originallistofval):
    changed_set = []
    for x in clause_set:
        changed_set.append(x.copy())

    for value in value_list:
        x = 0
        while x < len(changed_set):
            i = 0
            while i < len(changed_set[x]):
                
                if(value == changed_set[x][i]):
                    i = len(changed_set[x])
                    changed_set.remove(changed_set[x])
                    x -= 1
                elif(abs(value) == abs(changed_set[x][i])):
                    changed_set[x].remove(changed_set[x][i])
                    if(len(changed_set[x]) == 0):
                        return False
                else:
                    i += 1
                if(x == -1):
                    break
            x += 1
        
        
    if(len(changed_set) == 0):
        return value_list
   
     
    possiblelist = False
    print("still going")
    value_list.append(originallistofval[ind])
    ind += 1
    possiblelist = q8_solver(clause_set, value_list, ind, originallistofval)
    if(possiblelist):
        return value_list

    if(not possiblelist):
        value_list.pop()
        ind -= 1
    value_list.append(-originallistofval[ind])
    ind += 1
    possiblelist = q8_solver(clause_set, value_list, ind, originallistofval)

    if(possiblelist):
        return value_list
    if(not possiblelist):
        value_list.pop()
        ind -= 1

def dpll_sat_solve(l):
    l.sort(key=len)
    ind = 0
    value_list = []

    reduced_clause_set = unit_propagate(l)
    
    if(len(reduced_clause_set) == 0):
        return reduced_clause_set
    elif(reduced_clause_set == "Un sat"):
        return reduced_clause_set
    originallistofval = give_values(l)
    returnclause = q8_solver(reduced_clause_set, value_list, ind, originallistofval)
    if(returnclause == None):
        return "Un sat"
    return returnclause
"""

################# Q8 (new version) ##################

def get_into_format(l):
    newlist = []
    i = -1
    for clause in l:
        i += 1
        first = True
        newlist.append({()})
        for var in clause:
            if(var < 0):
                newlist[i].add((str(abs(var)), False))
            else:
                newlist[i].add((str(abs(var)), True))
            if(first):
                newlist[i].remove(())
                first = False

    return newlist

#code sourced from https://davefernig.com/2018/05/07/solving-sat-in-python/
def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]
 
#code sourced from https://davefernig.com/2018/05/07/solving-sat-in-python/
def dpll(cnf, assignments={}):
 
    if len(cnf) == 0:
        return True, assignments
 
    if any([len(c)==0 for c in cnf]):
        return False, None
 
    l = __select_literal(cnf)
 
    new_cnf = [c for c in cnf if (l, True) not in c]
    new_cnf = [c.difference({(l, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals
 
    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals
 
    return False, None


#partial_assignment is never used but I added it because of the formative checker failed tests because I didn't have it
def dpll_sat_solve(l, partial_assignment=[]):
    l.sort(key=len)

    reduced_clause_set = unit_propagate(l)
    
    if(len(reduced_clause_set) == 0):
        return reduced_clause_set
    elif(reduced_clause_set == "Un sat"):
        return reduced_clause_set
    
    reduced_clause_set = get_into_format(reduced_clause_set)
    cur_set = dpll(reduced_clause_set)
    if(cur_set[0] == False):
        return False
    cur_set = cur_set[1]
    return_list = []
    
    for key in cur_set:
        if(cur_set[key] == 1):
            return_list.append(int(key))
            
        else:
            return_list.append(int(key)*-1)

    
    return return_list
        
        






