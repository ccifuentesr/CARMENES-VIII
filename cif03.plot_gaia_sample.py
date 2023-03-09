import numpy as np
import pandas as pd
#import uncertainties
#from uncertainties.umath import *
import matplotlib.pyplot as plt
import astroquery
from astroquery.gaia import Gaia
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
#from PyAstronomy import pyasl
import re
import matplotlib
from scipy.stats import gaussian_kde
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable


astroquery.simbad.conf.server

plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

Gaia.login(user = 'ccifuent', password = 'Cwasdqwe!23')
job = Gaia.launch_job(
    "SELECT TOP 1000000000 l, b FROM gaiadr3.gaia_source WHERE l<=3 AND b>=-2 AND b<=1")
r = job.get_results()

x = r['l'] #[r[i]['l'] for i in range(len(r))]
y = r['b'] #[r[i]['b'] for i in range(len(r))]
# xy = np.vstack([np.round(x,2), np.round(y,2)])
# z = gaussian_kde(xy)(xy) # Calculate the point density

# =============================================================================
# PLOT
# =============================================================================

figsize = (12, 10)
pointsize = 0.2
linewidth = 2
elinewidth = 2
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18

xlabel = r'$l$ [deg]'
ylabel = r'$b$ [deg]'
cbarlabel = 'Density of stars'

fig, ax = plt.subplots(figsize=figsize)
cmap_col = plt.get_cmap('magma_r')

sc = ax.scatter(x, y, c = 'white', s = pointsize, alpha = 0.08)   #, c = z, cmap=cmap, s = pointsize)

# =============================================================================
# CUSTOM
# =============================================================================

ax.tick_params(axis='x', labelsize=tickssize, direction='out',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax.tick_params(axis='y', labelsize=tickssize, direction='out',
                  right=True, labelright=False, which='both')
ax.tick_params('both', direction = 'out', length = 10, width = 1.5, which = 'major')
ax.tick_params('both', direction = 'out', length = 5, width = 0.5, which = 'minor')
ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax.minorticks_on()
ax.set_xlabel(xlabel, size=labelsize)
ax.set_ylabel(ylabel, size=labelsize)
#plt.gca().invert_yaxis()
ax.set_xlim([0, 3])
ax.set_ylim([-2, 1])
ax.set_facecolor('black')

# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("right", "2%", pad="1%")
# cbar = plt.colorbar(sc, cax=cax)  # Colorbar
# cbar.set_label(cbarlabel, rotation=270, fontsize=labelsize, labelpad=30)
#sc.set_clim(vmin=min(x), vmax=max(x))
# cbar.ax.tick_params(labelsize=cblabsize)
# cbar.outline.set_visible(False)

# =============================================================================
# OUTPUT
# =============================================================================

plt.savefig('plot_Gaia_sample.pdf', dpi=900, bbox_inches='tight')
plt.show()
