'''
The function of this code is to probe over many different ions for common elements found in galactic environments.
'''

import yt
import os
import trident

yt.enable_parallelism()

d_path = '/mnt/research/galaxies-REU/sims/isolated-galaxies/MW_1638kpcBox_800pcCGM_200pcDisk_lowres/'
d_list = []

lower = 800
upper = 1200

make_dir = False

for i in range(lower, upper):
    path = "DD%04d" %i
    path = d_path + path + "/" + path
    d_list.append(path)

d_series = yt.load(d_list)

#Pertinent ions
#OV, OVI, OVII, OVIII
#CII, IV
#NV
#MgII, MgX
#SiIII, SiIV, SiV, SiVI
#NeII, NeIV, NeV, NeVIII
O_ions = [5, 6, 7, 8]
C_ions = [2, 4]
N_ions = [5]
Mg_ions = [2, 10]
Si_ions = [3, 4, 5, 6]
Ne_ions = [2, 4, 5, 8]
H_ions = [1]
Na_ions = [1]
Ca_ions = [2]

ions = {'O': O_ions, 'C': C_ions, 'N': N_ions, 'Mg': Mg_ions, 'Si': Si_ions, 'Ne': Ne_ions, 'H': H_ions}
#ions = {'H': H_ions, 'Na': Na_ions, 'Ca': Ca_ions}
axes = ['x', 'z']

def field_namer(atom, ion):
    field_name = atom + "_p%d_density" % (ion - 1)
    return field_name

if yt.is_root():
   if make_dir:
      for axis in axes:
          for atom in ions.keys():
                for ion in ions.get(atom):
                    path = atom + '/' + axis + '/' + atom + '_density/' + atom + '_' + str(ion)
                    os.makedirs(path)

storage = {}
for sto, ds in d_series.piter(storage=storage):
    for axis in axes:
        for atom in ions.keys():
            for ion in ions.get(atom):
                try:
                    trident.add_ion_density_field(atom, ion, ds)
                except:
                    pass
                p = yt.ProjectionPlot(ds, axis, field_namer(atom, ion), width=(150, "kpc"))
                p.annotate_timestamp(draw_inset_box=True)
                path = atom + '/' + axis + '/' + atom + '_density/' + atom + '_' + str(ion)
                p.set_cmap(field='density', cmap='kamae')
                p.save(path)
