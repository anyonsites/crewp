#! /usr/bin/python3

import sys
from qescripts.vasp.outcar import Outcar

if len(sys.argv) < 2:
    inpfname = 'OUTCAR'
else:
    inpfname = sys.argv[1]

print('Reading VASP OUTCAR filetype, ', inpfname)

outcar_obj = Outcar(inpfname)
print('Elements: ', outcar_obj.elements)
print('N_ions of each element: ', outcar_obj.n_ions)

