'''
This script identifies regions of inflow, outflow, and remaining circumgalactic medium using boolean masks and cut regions.

Yt's documentation may be found here: 
http://yt-project.org/doc/analyzing/filtering.html
'''

import yt
import yt.units as u
import os

# Range of timesteps to plot.
lower_limit = 1400
upper_limit = 1410

dataset_series = []
scale = (150, 'kpc')

d_path = '/mnt/research/galaxies-REU/sims/isolated-galaxies/MW_1638kpcBox_800pcCGM_200pcDisk_lowres/'

for x in range(lower_limit, upper_limit):
    dataset_series.append(d_path + 'DD%04d/DD%04d' % (x, x))  
ts = yt.DatasetSeries(dataset_series)

makedir = True # Set to false after initial execution.
field_list = ['entropy'] # List of fields used to probe regions.

# Domain criteria
hot_domain = '(obj["temperature"].in_units("K") > 1e6)'
warm_domain = '((obj["temperature"].in_units("K") > 1e5) & (obj["temperature"].in_units("K") < 1e6))'
cold_domain = '(obj["temperature"].in_units("K") < 1e5)'

pos_Vr = '(obj["radial_velocity"].in_units("km/s") > 30)'
neg_Vr = '(obj["radial_velocity"].in_units("km/s") < -30)'

high_Z = '(obj["metallicity"].in_units("Zsun") > 0.6)'
low_Z = '(obj["metallicity"].in_units("Zsun") < 0.4)'
a = ' & '

domain_names = ['outflow', 'inflow', 'cgm']

# Creates directories wherein to store plots.
if makedir:
	for domain in domain_names:
		path = 'phases/%s/' % domain
		os.makedirs(path)

# Iterates through each timestep and produces plot based on prior criteria for each field.
for ds in ts.piter():
	ad = ds.all_data()

	outflow_criteria = hot_domain + a + high_Z + a + pos_Vr
	inflow_criteria = low_Z + a + cold_domain + a + neg_Vr

	outflow_region = ad.cut_region([outflow_criteria])
	inflow_region = ad.cut_region([inflow_criteria])
	cgm_region = ad - outflow_region - inflow_region

	domains = {'outflow': outflow_region, 'inflow': inflow_region, 'cgm': cgm_region}

	for domain in domains:
	    for field in field_list:
	        p = yt.SlicePlot(ds, 'x', field, data_source=domains[domain], width=scale)
	        p.annotate_title(domain)

	        if (domain == 'outflow'):
	        	p.set_cmap(field=field, cmap='Spectral_r')
	        elif (domain == 'inflow'):
	        	p.set_cmap(field=field, cmap='YlGnBu_r')
	        elif (domain == 'cgm'):
	        	p.set_cmap(field=field, cmap='kamae')

	        p.save('/phases/%s/' % domain)