#!/usr/bin/env python

import os
import numpy as np
import MDAnalysis as mda
from MDAnalysis import transformations

u = mda.Universe("AA.gro", "AA.xtc")
u.transfer_to_memory()
ua = u.atoms
masses = np.zeros(u.atoms.n_atoms)
masses[u.atoms.types == '3'] = 12.011
masses[u.atoms.types == '4'] = 15.9994
masses[u.atoms.types == '5'] = 1.008
masses[u.atoms.types == '6'] = 15.9994
masses[u.atoms.types == '7'] = 1.008

for ts in u.trajectory:
    center = np.sum(ua.positions.T[0]*masses)/np.sum(masses), np.sum(ua.positions.T[1]*masses)/np.sum(masses), np.sum(ua.positions.T[2]*masses)/np.sum(masses)
    positions = ua.positions + u.dimensions[:3]/2 - center
    ua.positions = positions

with mda.Writer("AA.xtc", "w") as W:
    for ts in u.trajectory:
        W.write(ua)
ua.write("AA.gro")

# v = mda.Universe("CG.gro", "CG.xtc")
# v.transfer_to_memory()
#va = v.atoms

#masses = np.zeros(v.atoms.n_atoms)*1

#for ts in v.trajectory:
#    center = np.sum(va.positions.T[0]*masses)/np.sum(masses), np.sum(va.positions.T[1]*masses)/np.sum(masses), np.sum(va.positions.T[2]*masses)/np.sum(masses)
#    positions = va.positions + v.dimensions[:3]/2 - center
#    va.positions = positions

#with mda.Writer("CG.xtc", "w") as W:
#    for ts in v.trajectory:
#        W.write(va)
#va.write("CG.gro")
