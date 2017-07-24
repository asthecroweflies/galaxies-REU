'''
This script analyzes properties of our cosmological simulations by defining a scale at which to view and by defining from which set and halo to pull the data.
'''

import yt
from yt import derived_field
import os
import numpy as np 

cosmo_path = '/mnt/research/galaxies-REU/sims/cosmological/' # Data path
local_path = '/mnt/research/galaxies-REU/dcrowe/testing/view/cosmological'

#halos = [8506, 5036, 5016, 4123, 2878, 2392]
halos = [4123]
#RDs = [8, 13, 16, 20, 27, 29, 31, 32, 34, 36, 38, 40, 42]
sets = ['set1']
dataset_series = []
directories = []
makedir = False
scale = (200, 'kpc')

field_list = ['corrected_radial_velocity']
c = [0.4889087677001953, 0.4544239044189428, 0.4741420745849597] # set1-halo4123 center of highest density 

# Loads data and creates a sphere to use for removing of bulk velocity.
ds = yt.load(cosmo_path + sets[0] + '/' + 'halo_%06d' % halos[0] + '/RD0042/RD0042')
virial_sphere = ds.sphere(center=c, radius=scale)

# Creates new fields to account for the large-scale motion of the gas within the simulation by subtracting the bulk velocity of each component. This allows for probing of the velocity components of our cosmological simulations.
@derived_field(name="corrected_velocity_x", units="cm/s", force_override=True)
@derived_field(name="corrected_velocity_y", units="cm/s", force_override=True)
@derived_field(name="corrected_velocity_z", units="cm/s", force_override=True)

def _correct_velocity_x(field, data):
	return data["gas", "corrected_velocity_x"] - virial_sphere.quantities.bulk_velocity()[0]
def _correct_velocity_y(field, data):
	return data["gas", "corrected_velocity_y"] - virial_sphere.quantities.bulk_velocity()[1]
def _correct_velocity_z(field, data):
	return data["gas", "corrected_velocity_z"] - virial_sphere.quantities.bulk_velocity()[2]
def _corrected_radial_velocity(field, data):
    if data.has_field_parameter("bulk_velocity"):
        bv = data.get_field_parameter("bulk_velocity").in_units("cm/s")
    else:
        bv = data.ds.arr(np.zeros(3), "cm/s")
    xv = data["gas","velocity_x"] - virial_sphere.quantities.bulk_velocity()[0]
    yv = data["gas","velocity_y"] - virial_sphere.quantities.bulk_velocity()[1]
    zv = data["gas","velocity_z"] - virial_sphere.quantities.bulk_velocity()[2]
    center = data.get_field_parameter('center')
    x_hat = data["x"] - center[0]
    y_hat = data["y"] - center[1]
    z_hat = data["z"] - center[2]
    r = np.sqrt(x_hat*x_hat+y_hat*y_hat+z_hat*z_hat)
    x_hat /= r
    y_hat /= r
    z_hat /= r
    return xv*x_hat + yv*y_hat + zv*z_hat
ds.add_field(("gas","corrected_radial_velocity"),
             function=_corrected_radial_velocity,
             units="cm/s",
             take_log=False)
ds.add_field(("gas", "corrected_velocity_x"), function=_correct_velocity_x, units="cm/s", force_override=True)
ds.add_field(("gas", "corrected_velocity_y"), function=_correct_velocity_y, units="cm/s", force_override=True)
ds.add_field(("gas", "corrected_velocity_z"), function=_correct_velocity_z, units="cm/s", force_override=True)

# Iterates through directory to find the furthest redshift dump and returns the redshift.
def findHighest(directories):
	numericals = []
	for dir in directories:
		n = int(dir[-2:])
		numericals.append(n)

	highestRD = numericals[0]
	for x in numericals:
		if (x > highestRD):
			highestRD = x
	return highestRD

''' 
# Makes use of the findHighest function however has since been deprecated.
for set in sets:
	for halo in halos:
		directories = []
		os.chdir(cosmo_path + set + '/halo_%06d' % halo)
		directories = [x for x in os.listdir('.') if os.path.isdir(x)]
		highestRD = findHighest(directories)
		rd = 42
		dataset_series.append(cosmo_path + '/' + set + '/' + 'halo_%06d/RD%04d/RD%04d' % (halo, rd, rd))
ts = yt.DatasetSeries(dataset_series)
'''

# Creates directories wherein to save plots.
if makedir:
	for set in sets:
		for halo in halos:
			os.chdir(local_path)
			path = os.getcwd() + '/probe/halo_%06d' % (halo)
			os.makedirs(path)


# Creates a sphere of a given size and center, iterates through the data and creates yt Plots with desired criteria.
sp = ds.sphere(radius=scale, center=c)
for set in sets:
	for halo in halos:
		p = yt.SlicePlot(ds, 'x', ("gas","corrected_radial_velocity"), center=c, width=scale, data_source=sp)
		p.annotate_title('Halo %06d, %s Radial Velocity' % (halo, ds))
		p.set_cmap(field=("gas","corrected_radial_velocity"), cmap='Spectral')
		path = local_path + '/probe/corrected/halo_%06d' % (halo)
		os.chdir(path)
		p.save('halo_%06d-%s' % (halo, ds))