'''
This script creates phase plots for inflow, outflow, and CGM regions and has the capability to also create projection plots of the same regions for a given field.
'''

import yt
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

yt.enable_parallelism()

xy_fields = [('density', 'temperature'), ('radius', 'radial_velocity')]
#xy_fields = [('density', 'temperature')]
z_fields = ['metallicity', 'cell_mass', 'entropy']
#z_fields = ['cell_mass']
axes = ['x', 'z']
a = ' & '

Z_thresh = 0.6
T_thresh = 10e6
V_thresh = 40 #km/s
lower_limit = 3
upper_limit = 1800
make_dir = False
dataset_series = []

d_path = '/mnt/research/galaxies-REU/sims/isolated-galaxies/MW_1638kpcBox_800pcCGM_200pcDisk_lowres/'

for x in range(lower_limit, upper_limit):
    dataset_series.append(d_path + 'DD%04d/DD%04d' % (x, x))
ts = yt.DatasetSeries(dataset_series)

# Domain Criteria
hot_domain = '(obj["temperature"].in_units("K") > 1e6)'
warm_domain = '((obj["temperature"].in_units("K") > 1e5) & (obj["temperature"].in_units("K") < 1e6))'
cold_domain = '(obj["temperature"].in_units("K") < 1e5)'

pos_Vr = '(obj["radial_velocity"].in_units("km/s") > 30)'
neg_Vr = '(obj["radial_velocity"].in_units("km/s") < -30)'

high_Z = '(obj["metallicity"].in_units("Zsun") > 0.6)'
low_Z = '(obj["metallicity"].in_units("Zsun") < 0.4)'
a = ' & '

outflow = fast_domain + a + hot_domain + a + high_Z
inflow = low_Z + a + cold_domain
CGM = slow_domain + a + low_Z
region_names = ['outflow_domain', 'inflow_domain', 'CGM_domain']

# Creates directories wherein to save plots.
if yt.is_root():
    if make_dir:
        for region_name in region_names:
            for z in z_fields:
                for xy in xy_fields:
                    x_and_y_fields = xy[0] + '_vs_' + xy[1]
                    path = "%s/%s/%s" % (region_name, z, x_and_y_fields)
                    os.makedirs(path)

# Iterates through timesteps to create phase plots.
storage = {}
def plot_series(ts):
    for sto, ds in ts.piter(storage=storage):
        for z in z_fields:
            for xy in xy_fields:
                ad = ds.all_data()

                outflow_criteria = hot_domain + a + high_Z + a + pos_Vr
                inflow_criteria = low_Z + a + cold_domain + a + neg_Vr

                outflow_region = ad.cut_region([outflow_criteria])
                inflow_region = ad.cut_region([inflow_criteria])
                cgm_region = ad - outflow_region - inflow_region

                for region in regions.keys():
                    if (xy[0] == 'radius'):
                        pp = yt.PhasePlot(regions.get(region), xy[0], xy[1], 'entropy', weight_field=None)
                    else:
                        pp = yt.PhasePlot(regions.get(region), xy[0], xy[1], z, weight_field=None)

                    x_and_y_fields = xy[0] + '_vs_' + xy[1]
                    path = "%s/%s/%s" % (region, z, x_and_y_fields)
                    #pp.set_zlim(z, 1e-1, 1e5)
                    #pp.set_log(z, False)
                    pp.annotate_title(region)
                    pp.set_cmap(z, "kamae")
                    #print('dataset: %s' % ds)
                    pp.save(path + "_%s" % ds)
    # Run backup after 20% of initial run has completed
    #if (iter > int((upper_limit - lower_limit) * 0.2)):
        #_file_checker()

# Plot a single timestep
def plot_timestep(ds):
    for z in z_fields:
        for xy in xy_fields:
            ad = ds.all_data()
            center = [0.5, 0.5, 0.5]
            inner_sp = ds.sphere(center, (50, 'Mpc'))
            outer_sp = ds.sphere(center, (300, 'Mpc'))

            outer_shell = outer_sp - inner_sp
            outer_shell_domain = ad.cut_region([outer_shell])

            outflow_domain = ad.cut_region([outflow])
            inflow_domain = ad.cut_region([inflow])
            cgm_domain = ad.cut_region([CGM])
            regions = {'outflow_domain': outflow_domain, 'inflow_domain': inflow_domain, 'cgm_domain': cgm_domain}
            #regions = {'inflow_domain': inflow_domain}

            for region in regions.keys():
                if (xy[0] == 'radius'):
                    pp = yt.PhasePlot(regions.get(region), xy[0], xy[1], 'entropy', weight_field=None)
                else:
                    pp = yt.PhasePlot(regions.get(region), xy[0], xy[1], z, weight_field=None)

                x_and_y_fields = xy[0] + '_vs_' + xy[1]
                path = "%s/%s/%s" % (region, z, x_and_y_fields)
                #pp.set_zlim(z, 1e-1, 1e5)
                pp.annotate_title(region)
                pp.set_cmap(z, "kamae")
                pp.save(path + "_%s" % ds)

plot_series(ts)
'''
#Projection Plots

p_CGM = yt.ProjectionPlot(ds, 'z', "radial_velocity", weight_field="density", data_source=outer_shell_domain, width=(150, 'kpc'))
p_CGM.annotate_title('Outer Shell Radial Velocity')
p_CGM.annotate_timestamp(draw_inset_box=True)
#p_CGM.set_zlim('density', 1e-28, 6e-28)
p_CGM.set_cmap(field="radial_velocity", cmap='BuPu')
p_CGM.save("CGM_Vr/CGM_%s" % ds)


p_inflow = yt.ProjectionPlot(ds, 'x', "temperature", weight_field="temperature", data_source = inflow_domain, width=(120, 'kpc'))
p_inflow.annotate_title('Low Temperature & Metallicity (Inflow)')
p_inflow.annotate_timestamp()
p_inflow.set_cmap(field="temperature", cmap='BuPu')
#p_inflow.set_zlim('temperature', 1e-1, 1.0)
p_inflow.save("Inflow/Inflow_%s" % ds)

p_outflow = yt.ProjectionPlot(ds, 'x', "entropy", weight_field="entropy", data_source = outflow_domain, width=(120, 'kpc'))
p_outflow.annotate_title('High Temperature, Metallicity, & Net Velocity (Outflow)')
p_outflow.annotate_timestamp()
p_outflow.set_cmap(field="entropy", cmap='BuPu')
p_outflow.save("Outflow/Outflow_%s" % ds)
'''
