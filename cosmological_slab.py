'''
This script creates a box used to analyze a region within a cosmological simulation to provide depth in plots.
'''

import yt
ds = yt.load('/mnt/research/galaxies-REU/sims/cosmological/set1/halo_004123/RD0034/RD0034')
slab = ds.r[0.44:0.48, 0.43:0.48, 0.44:0.48]
# Center is: ds.quantities.max_location(('gas', 'velocity_magnitude'))
c = [0.4759006500244166, 0.4624843597412059, 0.4742450714111328] 
p = yt.ProjectionPlot(ds, 'z', 'velocity_magnitude', data_source=slab, width=(199, 'kpc'), center=c)
p.set_cmap(field='velocity_magnitude', cmap='Spectral_r')
p.set_figure_size(10)
p.set_font({'size':30})
#p.set_buff_size(3200)
#p.annotate_grids()
p.set_unit('velocity_magnitude', 'km**2/s')
p.save(mpl_kwargs={'bbox_inches':'tight'})