'''
This code uses yt's clump finding feature to detect regions of high density of a particualr field. The bounds provided are the default as seen within the documentation, consider tweaking these as desired for better results.
'''

import yt
from yt.analysis_modules.level_sets.api import *
import numpy as np
import os

yt.enable_parallelism()

d_path = '/mnt/research/galaxies-REU/sims/isolated-galaxies/MW_1638kpcBox_800pcCGM_200pcDisk_lowres/DD????/DD????'
d_list = []

lower = 3
upper = 1776
make_dir = False

fields = ['H_p0_number_density']

for i in range(lower, upper):
    path = "DD%04d" %i
    path = d_path + path + "/" + path
    d_list.append(path)

d_series = yt.load(d_path)

axes = ['x', 'z']
storage = {}
if make_dir:
    for axis in axes:
        for field in fields:
            path = '%s_clumps2/%s' % (axis, field) 
            os.makedirs(path)

# Iterates through each timestep, axis, and field to produce plots with annotated clump regions.

for sto, ds in d_series.piter(storage=storage):
    for axis in axes:
        for field in fields:
            data_source = ds.disk([0.5, 0.5, 0.5], [0., 0., 1.], (20, 'kpc'), 
                (4, 'kpc')) # region of interest

            c_min = 10**np.floor(np.log10(data_source[field]).min()  )
            c_max = 10**np.floor(np.log10(data_source[field]).max()+1)
            step = 2.0

            master_clump = Clump(data_source, field)
            #master_clump.add_validator("min_cells", 20)
            #master_clump.add_validator("gravitationally_bound", use_particles=False)
            find_clumps(master_clump, c_min, c_max, step)
            leaf_clumps = get_lowest_clumps(master_clump)

            p = yt.ProjectionPlot(ds, axis, field, center='c', width=(90, 'kpc'))
            p.annotate_clumps(leaf_clumps)
            p.annotate_timestamp(draw_inset_box=True)
            p.set_cmap('H_p0_number_density', "kamae")
            #p.set_zlim('H_p0_number_density', 10e14, 10e23)
            p.save('%s_clumps2/%s/clump_%s_%s.png' % (axis, field, axis, ds))