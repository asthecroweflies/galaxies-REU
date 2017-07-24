'''
This script creates radial profiles of specified fields for cosmological simulations of a given dataset.
'''

import yt

ds = yt.load('/mnt/research/galaxies-REU/sims/cosmological/set1/halo_004123/RD0042/RD0042')
local_path = '/mnt/research/galaxies-REU/dcrowe/testing/view/cosmological/radial_profiles/'

c = [0.4889087677001953, 0.4544239044189428, 0.4741420745849597]
virial_sphere = ds.sphere(center=c, radius=(400, 'kpc'))
fields = ['temperature', 'density', 'entropy']
weight_fields = [None, 'cell_mass']

for field in fields:
	for weight in weight_fields:
		p = yt.ProfilePlot(virial_sphere, "radius", field, weight_field=weight, label=('%s | %s weight:%s' % (ds, field, weight)), x_log=False)
		p.set_unit('radius', 'kpc')
		p.save(local_path + 'profiles/%s_%s-%s' % (ds, field, weight))