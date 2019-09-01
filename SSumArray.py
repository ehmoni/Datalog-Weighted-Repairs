import random
from array import array
import time
from datetime import timedelta


W = [0] + sorted([random.randint(1, 100)for i in range(10)])
start_time = time.time()


n = len(W)
m = sum(W) + 1
ftrue = [-1] * (m - 1)
ftrue = [0] + ftrue
minr = True

table = {(0, 0, 0): array('L', [0])}

print(W)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
start_time = time.time()

for w in range(W[1], m):
    for i in range(1, n):
        up = i - 1
        back = w - W[i]
        k = 0

        if (ftrue[back] == -1):
            continue

        for j in range(up, ftrue[back] - 1, -1):
            t = 0
            while True:
                if (j, back, t) in table:
                    entry = array('L')
                    entry.extend(table[(j, back, t)])
                    entry.append(i)
                    table[(i, w, k)] = entry
                    if (minr):
                        ftrue[w] = i
                        minr = False
                    print(w, "   ", table[(i, w, k)])
                    k = k + 1
                    t = t + 1
                else:
                    break
        k = 0
    minr = True
    #print(w)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(ftrue)

elapsed_time_secs = time.time() - start_time
msg = "Execution took: %s secs" % timedelta(seconds=round(elapsed_time_secs))
print(msg)


