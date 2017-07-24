'''
This script generates radial angular momentum profiles for x, y, and z axes as well as the magnitude as defined by a yt disk.
'''

import yt
import yt.units as u
import os

yt.enable_parallelism()

lower_limit = 1100
upper_limit = 1800

# Defines the disk used for calculation
c = [0.5, 0.5, 0.5]
normal = [0, 0, 1]
radius = 40 * u.kpc
height = 100 * u.kpc

dataset_series = []
make_dir = False
# Used to generate plots for skipped timesteps.
fill_missing = True

d_path = '/mnt/research/galaxies-REU/sims/isolated-galaxies/MW_1638kpcBox_800pcCGM_200pcDisk_lowres/'

for x in range(lower_limit, upper_limit):
    dataset_series.append(d_path + 'DD%04d/DD%04d' % (x, x))
ts = yt.DatasetSeries(dataset_series)

field_list = ['angular_momentum_x', 'angular_momentum_y', 'angular_momentum_z', 'angular_momentum_magnitude']

if make_dir:
	for field in field_list:
		os.makedirs('radius_300/cell_mass/' + field)

# Creates plots given a particular dataset and field; useful for iteration.
def _plot_ds_field(ds, field):
			disk = ds.disk(c, normal, radius, height)
			radial_profile = yt.create_profile(
				data_source=disk,
				bin_fields=["radius"],
				fields=field,
				n_bins=256,
				units=dict(radius="kpc"),
				logs=dict(radius=False),
				weight_field='cell_mass',
				extrema={'radius': (0, 300)},
				)
			p = yt.ProfilePlot.from_profiles(radial_profile)
			if (field != 'angular_momentum_magnitude'):
				p.set_ylim(field, -2e70, 2e70)
			else:
				p.set_ylim(field, 0, 1e70)
			p.set_log('%s' % field, False)
			p.save('radius_300/cell_mass/%s/%s' % (field, ds))

# This function iterates through a particular directory and locates any skipped timesteps and automatically generates them. 
missing_dd = []
def _file_checker():
    for dd in range(lower_limit, upper_limit):
        for field in field_list:
            cwd = os.getcwd()
            path = cwd + '/radius_300/cell_mass/%s/DD%04d_1d-Profile_radius_%s.png' % (field, dd, field)
            if (os.path.isfile(path) == False):
                print('File: %s' % path + ' does not exist! Generating now..')
                missing_dd.append(dd)
                ds = yt.load(d_path + 'DD%04d/DD%04d' % (dd, dd))
               _plot_ds_field(ds, field)
    print('Jeepers, we missed %i files between timesteps %i and %i' % (len(missing_dd), lower_limit, upper_limit))

# Simply iterates through the dataset without parameters.
if(fill_missing == False):
	for ds in ts.piter():
		for i, field in enumerate(field_list):
				disk = ds.disk(c, normal, radius, height)
				radial_profile = yt.create_profile(
					data_source=disk,
					bin_fields=["radius"],
					fields=field,
					n_bins=256,
					units=dict(radius="kpc"),
					logs=dict(radius=False),
					weight_field='cell_mass',
					extrema={'radius': (0, 300)},
					)
				p = yt.ProfilePlot.from_profiles(radial_profile)
				if (field != 'angular_momentum_magnitude'):
					p.set_ylim(field, -2e70, 2e70)
				else:
					p.set_ylim(field, 0, 1e70)
				p.set_log('%s' % field, False)
				p.save('radius_300/cell_mass/%s/%s' % (field, ds))

elif(fill_missing):
    _file_checker()
