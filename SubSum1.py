from collections import namedtuple

slwt = namedtuple('slwt', "sl, wt")
slwts = [slwt(1, 1), slwt(2, 2), slwt(3, 3)]
W = [0] + [i.wt for i in slwts]

W = [0, 10, 20, 30]

n = len(W)
m = sum(W) + 1
ftrue = [0]*m
minr = True

table = {(0, 0, 0): [0]}

print(W)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

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
                    print(w, "   ", table[(i, w, k)])
                    k = k + 1
                    t = t + 1
                else:
                    break
        k = 0
    minr = True

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# for keys,values in table.items():
#     print(keys)
#    # print(values)