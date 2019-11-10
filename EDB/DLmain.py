from DLlib import *

print("==========================================================================")
print("Loading FACTS and DIMENSION: ")
print("==========================================================================")
load_facts()
load_dim()
print("==========================================================================")

print("==========================================================================")
print("Item created by the RULE: ")
print("==========================================================================")
IDB = run_rule()
print(IDB)
print("==========================================================================")


print("==========================================================================")
print("Negation of the Constraint: ")
print("==========================================================================")
NC = neg_con()
print(NC)
print("==========================================================================")

print("==========================================================================")
print("Source of Inconsistency: ")
print("==========================================================================")
inconD = incon(NC)
print(inconD)
print("==========================================================================")


print("==========================================================================")
print("Weight-Ordered Predicates: ")
print("==========================================================================")
inconL = inconlist(inconD)
slwt = genweight(inconL)
inconL, slwt = fixWtorder(inconL, slwt)
print(inconL)
print(slwt)
print("==========================================================================")



print("==========================================================================")
print("==================     Main Program     =================================")
print("==========================================================================")
print("==========================================================================")


def checkmin(Lst):
    L = Lst[1:]
    nAtoms = [('-' + inconL[i][1]) for i in L]
    #print(nAtoms)
    pd.load(nAtoms)
    nc = neg_con()
    #print(nc)
    size = 0
    for n in nc:
        size += len(n)
    if not size:
        return 1
    icd = incon(nc)
    for v in icd.values():
        if v:
            #print(v)
            pAtoms = [('+' + inconL[i][1]) for i in L]
            pd.load(pAtoms)
            return 0
    return 1



print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

W = [i[1] for i in slwt]

n = len(W)
m = sum(W) + 1
ftrue = [0]*m
minr = True

table = {(0, 0, 0): [0]}

print(W)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
sat = 0

for w in range(W[1], m):
    for i in range(1, n):
        up = i-1
        back = w-W[i]
        k = 0

        for j in range(up, ftrue[back]-1, -1):
            t = 0
            while True:
                if(j, back, t) in table:
                    table[(i, w, k)] = table[(j, back, t)] + [i]
                    if(minr):
                        ftrue[w] = i
                        minr = False
                    #print(w, "   ", table[(i, w, k)])
                    sat = checkmin(table[(i, w, k)])
                    #print(sat)
                    if sat:
                        L = table[(i, w, k)][1:]
                        nAtoms = [('-' + inconL[i][1]) for i in L]
                        print(nAtoms)
                        break
                    k = k + 1
                    t = t + 1
                else:
                    break
            if sat: break
        k = 0
    if sat: break
    minr = True

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
