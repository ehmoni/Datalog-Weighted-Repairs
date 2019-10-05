import heapq as pq
import multiset as ms
import itertools as itr
import random

wts = [10, 81, 50, 51, 49, 21, 53, 36, 12, 10, 13, 66, 27, 11, 85, 8, 49, 97, 93, 21, 40, 2, 10, 58, 48, 35, 1, 10, 39,
       53, 30, 68, 53, 2, 88, 96, 61, 56, 52, 55, 81, 71, 20, 5, 19, 66, 4, 90, 49, 33, 2, 18, 97, 71, 80, 23, 42, 96,
       96, 55, 67, 7, 21, 29, 59, 95, 78, 86, 55, 26, 33, 54, 46, 93, 13, 74, 83, 41, 91, 13, 61, 100, 89, 41, 53, 35,
       21, 39, 61, 45, 28, 45, 28, 52, 31, 64, 99, 61, 87, 30]

AS1 = [5, 7, 11, 12, 83, 96, 96, 100]
AS2 = [2, 2, 2]
AS3 = [99, 2]
AS4 = [1, 50, 100]
AS5 = [40, 41, 41, 42, 45, 45, 46, 48, 49, 49, 49]
AS6 = [5, 2, 2]

ans = []

ans.append(ms.Multiset(AS1))
ans.append(ms.Multiset(AS2))
ans.append(ms.Multiset(AS3))
ans.append(ms.Multiset(AS4))
ans.append(ms.Multiset(AS5))
ans.append(ms.Multiset(AS6))

# %%

ppln = []
h = []
maxsum = sum(wts)
size = len(wts)
wtdic = {}


# %%

def fitness(lst):
    masked = list(itr.compress(wts, lst))
    msum = sum(masked)

    lstms = ms.Multiset(masked)

    for m in ans:
        if m.issubset(lstms):
            return msum

    return (maxsum + 1)


# %%

def addc(c):

    f = fitness(c)
    s = sum(c)
    t = (f, c)
    maxs = h[0][0]

    if (f in wtdic): return

    if f < maxs:
        del wtdic[maxs]
        pq._heapreplace_max(h, t)
        wtdic[f] = s

# %%    

def population(lst):

    n = len(lst)

    for t in range(1, n - 1):
        for _ in range(n):
            crmsm = [0] * (n - t) + [1] * t
            random.shuffle(crmsm)
            f = fitness(crmsm)
            if (f < maxsum):
                ppln.append((f, crmsm))
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

population(wts)

for i in ppln:
    s = sum(i[1])
    if i[0] in wtdic: continue
    h.append(i)
    wtdic[i[0]] = s
    if len(wtdic) == size:
        break
pq._heapify_max(h)

# %%

for k in range(10000):
    ngen = crossover(h)
    child = mutate(ngen)
    addc(child)
 

h.sort()

tt = []
for x in h:
    tt.append(x[0])
print(tt[:10])
