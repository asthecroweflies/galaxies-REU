'''
This script is able to produce multi-panel (4) movies of a given dataset using matplotlib.
'''

import yt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

yt.enable_parallelism()
lower_limit = 3
upper_limit = 600
dataset_series = []

d_path = '/mnt/research/galaxies-REU/sims/isolated-galaxies/MW_1638kpcBox_800pcCGM_200pcDisk_lowres/kineticFB/'
for x in range(lower_limit, upper_limit):
    dataset_series.append(d_path + 'DD%04d/DD%04d' % (x, x))
ts = yt.DatasetSeries(dataset_series)
storage = {}

for sto, ds in ts.piter(storage=storage):
    fig = plt.figure()
    grid = AxesGrid(fig, (0.075,0.075,0.85,0.85),
                    nrows_ncols = (2, 2),
                    axes_pad = 1,
                    label_mode = "1",
                    share_all = True,
                    cbar_location="right",
                    cbar_mode="each",
                    cbar_size="3%",
                    cbar_pad="0%")

    fields = ['metallicity', 'density', 'entropy', 'H_p0_number_density']

    p = yt.SlicePlot(ds, 'x', fields, width=(150, 'kpc'))
    p.set_cmap(field="density", cmap='Spectral_r')
    p.set_cmap(field="entropy", cmap='afmhot')
    p.set_cmap(field="metallicity", cmap='GnBu_r')
    p.set_cmap(field="H_p0_number_density", cmap='magma')
    #p.annotate_timestamp(draw_inset_box=True)

    p.zoom(1)

    for i, field in enumerate(fields):
        plot = p.plots[field]
        plot.figure = fig
        plot.axes = grid[i].axes
        plot.cax = grid.cbar_axes[i]
        fig.suptitle(ds, fontsize=14)
    p._setup_plots()
    plt.savefig('images/multiplot_%s.png' % ds)
