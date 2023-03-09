import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib import rc
from pathlib import Path

fpath = Path(matplotlib.get_data_path(), "/Users/ccifuentesr/Library/Fonts/MinionPro-MediumCapt.otf")
plt.rcParams["font.family"] = "Georgia"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v01'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

filter_single = df['Component'] == '-'
filter_multiple = df['Component'] != '-'

G_mag_single = df[filter_single]['G_mag']
G_mag_multiple = df[filter_multiple]['G_mag']
ruwe_single = df[filter_single]['ruwe']
ruwe_multiple = df[filter_multiple]['ruwe']

x_single = G_mag_single
y_single = ruwe_single
x_multiple = G_mag_multiple
y_multiple = ruwe_multiple


# =============================================================================
# AXES
# =============================================================================

left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.005

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom + height + spacing, width, 0.2]
rect_histy = [left + width + spacing, bottom, 0.2, height]

# =============================================================================
# PLOT
# =============================================================================

figsize = (12, 10)
pointsize = 60
linewidth = 2
elinewidth = 2
tickssize = 16
labelsize = 18

xlabel = f'$G$ [mag]'
ylabel = f'ruwe'

plt.close('all')
plt.figure(figsize=(8, 8))

#
ax_histx = plt.axes(rect_histx)
ax_histy = plt.axes(rect_histy)

ax_histx.tick_params(axis='y', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax_histy.tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax_histx.tick_params('both', direction = 'in', length = 5, width = 1.5, which = 'major')
ax_histx.tick_params('both', direction = 'in', length = 2.5, width = 0.5, which = 'minor')
ax_histy.tick_params('both', direction = 'in', length = 5, width = 1.5, which = 'major')
ax_histy.tick_params('both', direction = 'in', length = 2.5, width = 0.5, which = 'minor')
ax_histx.axes.xaxis.set_ticklabels([])
#
ax = plt.axes(rect_scatter)

ax.scatter(x_single, y_single, facecolors='none', edgecolors='lightsteelblue')
ax.scatter(x_multiple, y_multiple, facecolors='none', edgecolors='blue')
ax.axhline(2, color='red', linestyle='dashed', linewidth=linewidth)

#
ax_histx.hist(x_single, bins=np.logspace(np.log10(min(y_single)), np.log10(max(y_single)), 80),\
density=False, alpha=1, histtype='step', color='blue', linewidth=linewidth)
ax_histx.hist(x_multiple, bins=np.logspace(np.log10(min(y_multiple)), np.log10(max(y_multiple)), 80),\
 density=False, alpha=1, histtype='step', color='lightsteelblue', linewidth=linewidth, zorder=0)
ax_histy.hist(y_single, bins=np.logspace(np.log10(min(y_single)), np.log10(max(y_single)), 80),\
orientation='horizontal', density=False, alpha=1, histtype='step', color='blue', linewidth=linewidth)
ax_histy.hist(y_multiple, bins=np.logspace(np.log10(min(y_multiple)), np.log10(max(y_multiple)), 80),\
orientation='horizontal', density=False, alpha=1, histtype='step', color='lightsteelblue', linewidth=linewidth, zorder=0)
ax_histy.axhline(2, color='red', linestyle='dashed', linewidth=linewidth)

# =============================================================================
# CUSTOM
# =============================================================================

ax.tick_params(axis='x', labelsize=tickssize, direction='in',
                  top=True, labeltop=False, which='both', labelbottom=True)
ax.tick_params(axis='y', labelsize=tickssize, direction='in',
                  right=True, labelright=False, which='both')
ax.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major')
ax.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)
ax.minorticks_on()
ax.set_xlabel(xlabel, size=labelsize, font=fpath)
ax.set_ylabel(ylabel, size=labelsize, font=fpath)
# ax.set_title(f'This is a special font', font=fpath)

ax_histx.set_xlim(ax.get_xlim())
# ax_histy.set_ylim(ax.get_ylim())
ax.set_yscale('log')
ax_histy.set_yscale('log')


# =============================================================================
# SAVE
# =============================================================================

plt.savefig('Output/'+'plot_G_ruwe.pdf', dpi=900, bbox_inches='tight')
plt.show()
