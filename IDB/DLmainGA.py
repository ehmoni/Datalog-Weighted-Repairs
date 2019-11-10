from DLlib import *
import heapq as pq
import multiset as ms
import itertools as itr
import random
import time
file = open("GAiter.txt", "w+")
ii = 0
fit = 0

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
print(len(IDB))
print("==========================================================================")


print("==========================================================================")
print("Negation of the Constraint: ")
print("==========================================================================")
NC = neg_con(IDB)
print(NC)
print("==========================================================================")

print("==========================================================================")
print("Source of Inconsistency: ")
print("==========================================================================")
inconD = incon(NC, IDB)
print(inconD)
print("==========================================================================")


print("==========================================================================")
print("Weight-Ordered Predicates: ")
print("==========================================================================")
inconL = inconlist(inconD)
slwt = genweight(inconL)
random.shuffle(slwt)
inconL, slwt = fixWtorder(inconL, slwt)
print(inconL)
print(slwt)
print("==========================================================================")



print("==========================================================================")
print("==================     Main Program     =================================")
print("==========================================================================")
print("==========================================================================")
print(" < RUNNING >")

def checkmin(Lst):
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
        pAtoms = [('+' + inconL[i][1]) for i in L]
        pd.load(pAtoms)
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

#W = [i[1] for i in slwt]
wts = [i[1] for i in slwt]

#W = [0, 10, 20, 30]

ppln = []
h = []
maxsum = sum(wts)
size = len(wts)
wtdic = {}

print("MAX SUM: ", maxsum)
print("in % : ", 100)
mnwt = min(wts[1:]) 
print("MIN Wt : ", mnwt)
print("in % : ", int(100/maxsum)* mnwt)
# %%

def fitness(lst):
    masked = list(itr.compress(wts, lst))
    msum = sum(masked)
    chk = []

    for i in range(size):
        if lst[i]:
            chk.append(i)

    if checkmin(chk):
        #print(chk)
        return msum

    return (maxsum + 1)


# %%

def addc(c):
    f = fitness(c)
    s = sum(c)
    t = (f, c)
    maxs = h[0][0]

    if (f in wtdic): return

    global fit
    if f < maxs:
        fit = f
        del wtdic[maxs]
        pq._heapreplace_max(h, t)
        wtdic[f] = s


# %%

def population(lst):
    #lst = lst[1:]
    global ii
    n = len(lst)

    for t in range(1, n - 1):
        for _ in range(n):
            crmsm = [0] * (n - t) + [1] * t
            random.shuffle(crmsm)
            #crmsm = [0] + crmsm
            f = fitness(crmsm)
            if (f < maxsum):
                ppln.append((f, crmsm))                
                #s = str(ii) + "\t" + str(min(ppln)[0]) + "\n"                
                s = str(ii) + "\t" + str(f) + "\n"                
                file.write(s)
                ii += 1
    ppln.sort()


# %%

def crossover(heap):
    parents = random.sample(heap, 3)
    parents.sort()
    child = [1 if ((x == 1) and (y == 1)) else 0 for x, y in zip(parents[0][1], parents[1][1])]
    return child


# %%

def mutate(child):
    mch = crossover(ppln[size:])
    i = random.randrange(0, size)
    if child[i] == 1:
        child[i] = mch[i]
    return child


# %%
st0 = time.time()

population(wts)

st1 = time.time() - st0
print(" Population Generated: ", st1)

for i in ppln:
    s = sum(i[1])
    if i[0] in wtdic: continue
    h.append(i)
    wtdic[i[0]] = s
    if len(wtdic) == size:
        break
pq._heapify_max(h)

# %%
print(" < POPULATION DONE >")

st2 = time.time()

iter = 0
if size < 10:
    iter = 100
elif size < 100:
    iter = 1000
elif size < 1000:
    iter = 10000
elif size < 10000:
    iter = 100000
elif size < 100000:
    iter = 1000000
else:
    iter = 10000000

#iter = 100000

for k in range(iter):
    #global ii
    ngen = crossover(h)
    child = mutate(ngen)
    addc(child)
    #s = str(k+ii) + "\t" + str(min(h)[0]) + "\n"
    s = str(k+ii) + "\t" + str(fit) + "\n"
    file.write(s)

ss = str(iter) + "\t" + str(min(h)[0])
file.write(ss)
st3 = time.time() - st2
print(" Interation done in : ", st3)

h.sort()

print(" < DONE >")
tt = []
ss = []
for x in h:
    tt.append(x[0])
    l = []
    for i in range(size):
        if x[1][i]:
            l.append(inconL[i][1])
    ss.append(l)
print(tt[:10])
print(ss[:10])

file.close()
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(h)








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