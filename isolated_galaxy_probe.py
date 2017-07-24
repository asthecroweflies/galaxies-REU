'''
Script which conducts timeseries analysis of an isolated galaxy.
'''

import yt
import yt.units as u
import os

yt.enable_parallelism()

lower_limit = 599
upper_limit = 600
dataset_series = []

#d_path = '/mnt/research/galaxies-REU/sims/isolated-galaxies/MW_1638kpcBox_800pcCGM_200pcDisk_lowres/
d_path = '/mnt/c/scratch/sciteam/dsilvia/simulations/galaxy_simulation/reu_sims/MW_1638kpcBox_800pcCGM_200pcDisk/thermalFB/'
for x in range(lower_limit, upper_limit):
    dataset_series.append(d_path + 'DD%04d/DD%04d' % (x, x))
ts = yt.DatasetSeries(dataset_series)

fields = ['baroclinic_vorticity_magnitude']

for ds in ts.piter():
	for field in fields:
		p = yt.ProjectionPlot(ds, 'z', field, width=(100, 'kpc'))
		p.set_cmap(field=field, cmap='RdYlGn_r')
		p.annotate_timestamp(draw_inset_box=True, text_args={'size':30, 'color':'w'})
		#p.annotate_quiver('velocity_x', 'velocity_y', 10)
			# Note: if increasing buffer size, change quiver density accordingly
			# e.g. if buff_size = 3200 => change 10 to 40
		#p.annotate_streamlines('velocity_x', 'velocity_y', factor=8, density=6, field_color='velocity_magnitude')
		p.set_figure_size(10)
		#p.hide_axes()
		#p.set_font({'size':30})
		#p.hide_colorbar()
		p.annotate_scale(corner='upper_left', max_frac=0.4, text_args={'size':30})
		p.set_buff_size(3200)
		#p.set_unit('metallicity', 'Zsun*km')
		#p.set_unit('velocity_magnitude', 'km**2/s')
		p.save('%s' % dd, mpl_kwargs={'bbox_inches':'tight'})
