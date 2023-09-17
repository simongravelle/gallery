import os
import numpy as np
import MDAnalysis as mda
from MDAnalysis import transformations

from utilities import extract_monomer_list

u = mda.Universe("AA.data", "AA.xtc")
u.transfer_to_memory()
monomer_list = extract_monomer_list(u)
number_PEG = len(np.unique(u.select_atoms("resid 1").atoms.resids))
monomer_per_molecule = u.select_atoms("resid 1 and type 4 6").atoms.n_atoms

# unwrap the AA universe
ag = u.atoms
transform = mda.transformations.unwrap(ag)
u.trajectory.add_transformations(transform)
oxygens = u.select_atoms("type 4 6")
with mda.Writer("_oxygens.xtc", oxygens.n_atoms) as W:
    for ts in u.trajectory:
        W.write(oxygens)
oxygens.write("_oxygens.gro")

# calculate CoM positions
center_of_mass = np.zeros((u.trajectory.n_frames, len(monomer_list), 3))
for ts in u.trajectory:
    for cpt, monomer in enumerate(monomer_list): 
        x2 = np.diff(monomer.positions, axis=0).T[0]**2
        y2 = np.diff(monomer.positions, axis=0).T[1]**2
        z2 = np.diff(monomer.positions, axis=0).T[2]**2
        if np.max(np.sqrt(x2 + y2 + z2)) > 3.0:
            print("too much distance between 2 atoms, is the universe unwrapped?")
            print("the distance bewteen the CoM and oxygen is "+str(np.max(np.sqrt(x2 + y2 + z2))))
        center_of_mass[ts.frame][cpt] = monomer.center_of_mass()
        #print(center_of_mass[ts.frame][cpt])

# replace oxygen positions by CoM positions
v = mda.Universe("_oxygens.gro", "_oxygens.xtc")
with mda.Writer("_temp.xtc", "w") as W:
    for ts in v.trajectory:
        ts.positions = center_of_mass[ts.frame]
        W.write(v)
v.atoms.write("_temp.gro")

# wrap universe (optional here)
w = mda.Universe("_temp.gro", "_temp.xtc")
ag = w.atoms
transform = mda.transformations.wrap(ag)
w.trajectory.add_transformations(transform)

# write CoM trajectory
with mda.Writer("CG.xtc", len(monomer_list)) as W:
    for ts in w.trajectory:
        W.write(w)
w.select_atoms("all").write("CG.gro")

os.remove("_temp.gro")
os.remove("_temp.xtc")
os.remove("_oxygens.xtc")
os.remove("_oxygens.gro")
