# yt Analysis Scripts
This repo contains scripts created during the Summer of 2017 as part of the iCER-ACRES REU which provide varying analysis tools for astrophysical simulations.


### [clump_finder.py](https://github.com/dac183/galaxies-REU/blob/master/clump_finder.py)
Using [yt's clump finding feature](http://yt-project.org/doc/analyzing/analysis_modules/clump_finding.html), this script highlights regions of a defined density.


### [cosmological_probe.py](https://github.com/dac183/galaxies-REU/blob/master/cosmological_probe.py)
This script iterates through cosmological simulations and has the capability to create desired plots for specified fields at any scale. This script also features derivied fields which subtracts the bulk velocity of the large-scale gas en masse to accurately calculate various velocity profiles such as radial velocity.


### [cosmological_radial_profiles.py](https://github.com/dac183/galaxies-REU/blob/master/cosmological_radial_profiles.py)
Centered at a point with the highest velocity magnitude of a particular simulation, this script generates radial profiles of cosmological simulations.


### [cosmological_slab.py](https://github.com/dac183/galaxies-REU/blob/master/cosmological_slab.py)
This script creates a rectangular box which enables projections to be conducted on cosmological simulations.


### [enstrophy.py](https://github.com/dac183/galaxies-REU/blob/master/enstrophy.py)
While the accuracy of this script has not been verified, it attempts to calculate the enstrophy of an idealized simulation and generate the accompanying radial profile.


### [ion_density_field.py](https://github.com/dac183/galaxies-REU/blob/master/ion_density_field.py)
This script allows for the probing of a myriad of ions within idealized simulations using [Trident](http://trident-project.org/) over a defined time interval.


### [isolated_galaxy_probe.py](https://github.com/dac183/galaxies-REU/blob/master/isolated_galaxy_probe.py)
Probing isolated galaxies is an imperitive part of astrophysical simulation analysis. This script has the capability to probe an array of fields over a given time interval and also has a variety of plot-modifications available to produce high-quality plots.


### [make_me_movie.py](https://github.com/dac183/galaxies-REU/blob/master/make_me_movie.py)
Using ffmpeg, this highly contrived script can be used to generate movies on a windows machine for any series images with proper alterationos.

### [multipanel.py](https://github.com/dac183/galaxies-REU/blob/master/multi_panel.py)
Using matplotlib as the backbone, this script creates multi-panel plots of different fields over a defined timestep.

### [phase_filter.py](https://github.com/dac183/galaxies-REU/blob/master/phase_filter.py)
This script locates regions defined with yt's boolean masks and uses these filters to create plots of particular regions of interest i.e. outflow, inflow, CGM.


### [phase_plotter.py](https://github.com/dac183/galaxies-REU/blob/master/phase_plottter.py)
Deriving functionality from code within phase_filter.py, this script creates phase plots of different phases within idealized simulations.


### [radial_angular_momentum.py](https://github.com/dac183/galaxies-REU/blob/master/radial_angular_momentum.py)
To gain insight into the dynamical activity of isolated galaxies, this script creates a profile of angular momentum for each axis and accompanying magnitude with respect to radius.


### [run.sh](https://github.com/dac183/galaxies-REU/blob/master/run.sh)
This is a sample job script for MSU's HPCC.


### [stream_time.py](https://github.com/dac183/galaxies-REU/blob/master/stream_time.py)
This fun, though expensive, script supports various plot modifications at high resolution.
