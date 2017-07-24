'''
Script to iterate through datasets to create captivating plots of with annotated velocity magnitude streamlines.
'''

import yt

yt.enable_parallelism()
lower = 3
upper = 10
make_dir = False
#d_path = '/mnt/research/galaxies-REU/sims/isolated-galaxies/MW_1638kpcBox_800pcCGM_200pcDisk_lowres/'

d_path = '/mnt/c/scratch/sciteam/dsilvia/simulations/galaxy_simulation/reu_sims/MW_1638kpcBox_800pcCGM_200pcDisk/thermalFB/'
d_list = []

for i in range(lower, upper):
    path = "DD%04d" %i
    path = d_path + path + "/" + path
    d_list.append(path)
d_series = yt.load(d_list)

for ds in d_series.piter():
	p = yt.ProjectionPlot(ds, 'z', 'velocity_magnitude', width=(100, 'kpc'))
	p.set_cmap(field='velocity_magnitude', cmap='magma')
	p.annotate_timestamp(draw_inset_box=True, text_args={'size':20, 'color':'w'})
	#p.annotate_quiver('velocity_x', 'velocity_y', 10)
	p.annotate_streamlines('velocity_x', 'velocity_y', factor=12, density=6, field_color='velocity_magnitude')
	p.set_figure_size(12)
	p.hide_axes()
	#p.set_font({'size':30})
	p.hide_colorbar()
	#p.annotate_scale(corner='upper_left', max_frac=0.4, text_args={'size':30})
	#p.annotate_mesh_lines(plot_args={'color':'black'})
	#p.set_buff_size(3200)
	#p.set_unit('metallicity', 'Zsun*km')
	#p.set_unit('velocity_magnitude', 'km**2/s')
	#p.save('stream/z/' % ds, mpl_kwargs={'bbox_inches':'tight'})
	p.save()