import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv
from matplotlib import rc
from matplotlib.ticker import FormatStrFormatter
from pathlib import Path

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

filename = 'Data/cif03.v01.csv'

df = pd.read_csv(filename, sep=",", header=0)

filter_Karmn = df['Karmn'].notnull()

SpTnum = df[filter_Karmn]['SpTnum']

SpTypes = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']

# =============================================================================
# PLOT
# =============================================================================

figsize = (12, 10)
pointsize = 60
linewidth = 2
elinewidth = 2
tickssize = 22
labelsize = 22
legendsize = 18
cblabsize = 18
bins_size = np.arange(70.5, 82.5, 1)
#
fig, ax = plt.subplots(figsize=figsize)
cm = plt.cm.get_cmap('magma_r')

xlabel = f'Spectral type'
ylabel = f'Number of stars'

#
n, bins, patches = plt.hist(SpTnum, bins=bins_size, color='red')
bin_centers = 1 * (bins_size[:-1] + bins_size[1:])

col = bin_centers - min(bin_centers)  # Scale values to interval [0,1]
col = col/max(col)
#
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c+.1)) # The +0.1 avoids light yellow

# =============================================================================
# CUSTOM
# =============================================================================

ax.set_xlabel(xlabel, size=labelsize, font=fpath)
ax.set_ylabel(ylabel, size=labelsize, font=fpath)
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax.set_xticklabels(SpTypes)

ax.tick_params(axis='x', labelsize=tickssize-2, direction='in',
               top=True, labeltop=False, which='both')
ax.tick_params(axis='y', labelsize=tickssize, direction='in',
               right=True, labelright=False, which='both')
ax.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax.minorticks_on()
ax.xaxis.set_tick_params(which='minor', bottom=False, top=False)
plt.xticks(np.arange(70.5, 80.5, 1))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=-45, ha="left")

#
plt.xlim(70.5, 80.5)
plt.ylim(0.5, 1e3)
ax.set_yscale('log')

# =============================================================================
# OUT
# =============================================================================

output_file = 'hist_SpT'
plt.savefig('Output/'+output_file+'.pdf', bbox_inches='tight')
plt.show()
