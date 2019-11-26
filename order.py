#!/usr/bin/python

qs = []
ks = []

for i in range(0,13):
    for j in range(0,13):
        ans = i*j
        qs.append(["%d x %d =" % (i,j), ans])
        if ans not in ks:
            ks.append(ans)

for k in sorted(ks):
    for q in qs:
        if q[1] == k:
            print("%12s %d" % (q[0], k))


