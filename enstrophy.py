'''
Enstrophy is the integral of the curl of the velocity field, or vorticity.
This in-progress script endeavors to calculate this field for use in radial profling.
'''

import yt
from yt import derived_field

yt.enable_parallelism()

d_path = '/mnt/research/galaxies-REU/sims/isolated-galaxies/MW_1638kpcBox_800pcCGM_200pcDisk_lowres/'
d_list = []
lower_limit = 400
upper_limit = 405
dataset_series = []

for x in range(lower_limit, upper_limit):
    dataset_series.append(d_path + 'DD%04d/DD%04d' % (x, x))
ts = yt.DatasetSeries(dataset_series)

d_series = yt.load(d_list)
storage = {}

def _enstrophy(field, data):
    dV = data.sum("cell_volume")
    return ((data[field]**2) * dV)

yt.add_field(('gas', 'enstrophy'), function=_enstrophy)

for ds in ts.piter():
	ad = ds.all_data()
	radial_profile = yt.create_profile(
		data_source=ad,
		bin_fields=["radius"],
		fields=_enstrophy(('gas', 'vorticity_magnitude'), ad),
		n_bins=256,
		units=dict(radius="kpc"),
		logs=dict(radius=False),
		weight_field='cell_mass',
		extrema={'radius': (0, 300)},
		)
	p = yt.ProfilePlot.from_profiles(radial_profile)
	p.save('%s' % ds)
	#vorticity = ad.quantities.vorticity_magnitude()
	#print('enstrophy: %s' % _enstrophy(('gas', 'vorticity_magnitude'), ds))