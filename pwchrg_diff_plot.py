#! /usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from pwchrg_read import pwchrg_read
from pwchrg import PWCharge

'''
Sequence of charge density list:
    total, d, free
'''

inpflist = ['chrgsum_60.log','chrgsum_35.log']

# read in total and d charge densities
chrg3dlist = []
for inpfname in inpflist:
    chrg_in, cell = pwchrg_read(inpfname)
    chrg3dlist.append(chrg_in)
# calculate free electron density
chrg_free = chrg3dlist[0] - chrg3dlist[1]
chrg3dlist.append(chrg_free)

# average densities
avgchrglist = []
for chrg in chrg3dlist:
    chrg3d = PWCharge(chrg, cell, 'ang')
    avgchrg = chrg3d.xyavg()
    print('charge integrated, ',chrg3d.intgrl_z())
    avgchrglist.append(avgchrg)
zaxis = chrg3d.zgrid()

print('free charge integrated, ',chrg3d.intgrl_z())

# writing data
alldata = [zaxis] + avgchrglist
alldata = tuple(alldata)
headtag = 'z-axis    full_valence     d-valence     free-valence'
np.savetxt('chrgden.dat', np.column_stack(alldata), header=headtag)

fig = plt.figure()
plt.plot
ax = fig.add_subplot( 1, 1, 1)
ax.plot(zaxis,avgchrglist[2])
plt.show()


