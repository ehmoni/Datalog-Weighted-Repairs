from DLlib import *
import time

st0 = time.time()

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
#print(IDB)
print("==========================================================================")

st1 = time.time() - st0
print("Rule Generated time: ", st1)
st1 = time.time()

print("==========================================================================")
print("Negation of the Constraint: ")
print("==========================================================================")
NC = neg_con(IDB)
#print(NC)
print("==========================================================================")

print("==========================================================================")
print("Source of Inconsistency: ")
print("==========================================================================")
inconD = incon(NC, IDB)
print(inconD)
print("==========================================================================")

st2 = time.time() - st1
print("Source of Inconsistency found in: ", st2)

print("==========================================================================")
print("Weight-Ordered Predicates: ")
print("==========================================================================")
inconL = inconlist(inconD)
slwt = genweight(inconL)
inconL, slwt = fixWtorder(inconL, slwt)
print(inconL)
print(slwt)
print("==========================================================================")


st3 = time.time()

print("==========================================================================")
print("==================     Main Program     =================================")
print("==========================================================================")
print("==========================================================================")
print(" < RUNNING >")

count = 0

def checkmin(Lst):
    global count
    count+=1
    global IDB
    L = Lst[1:]
    nAtoms = [('-' + inconL[i][1]) for i in L]
    #print(nAtoms)
    pd.load(nAtoms)
    nc = neg_con(IDB)
    #print(nc)
    size = 0
    for n in nc:
        size += len(n)
    if not size:
        return 1

    IDB = run_rule()
    icd = incon(nc, IDB)
    for v in icd.values():
        if v:
            #print(v)
            pAtoms = [('+' + inconL[i][1]) for i in L]
            pd.load(pAtoms)
            return 0
    return 1



#slwt = namedtuple('slwt', "sl, wt")
#slwts = [slwt(1, 1), slwt(2, 2), slwt(3, 3)]
#W = [0] + [i.wt for i in slwts]

W = [i[1] for i in slwt]


#W = [0, 10, 20, 30]

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
                    if sat: break
                    k = k + 1
                    t = t + 1
                else:
                    break
            if sat: break
        k = 0
    if sat: break
    minr = True

st4 = time.time() - st3
print("Min Weight found in: ", st4)
print("Out of: ", 2**(len(W)-1), " Result Found: ", count)
print("~~~~~~~~~~~~~ DONE ~~~~~~~~~~~~~~~~~~~")








#nAtoms = [('-' + inconL[i][1]) for i in L]
#pAtoms = [('+' + inconL[i][1]) for i in L]

#print(checkmin(L, inconL))

#str = ["""+aBC('Clinical', 'Nurse')""", """+bCD('Tom', 'Pediatrician')"""]

# str = ["+aBC('Clinical', 'Nurse')", "+bCD('Tom', 'Pediatrician')"]
# print(str)
#
#
# pd.create_terms("aBC, bCD, A, B, C, D")
# pd.load(str)
#
# print(aBC(A, B))
# print(bCD(C, D))