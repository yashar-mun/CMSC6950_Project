from argopy import DataFetcher as ArgoDataFetcher
argo_loader = ArgoDataFetcher()

#ds_points = argo_loader.profile(2900737, [2]).to_xarray() #Japan
#ds_points = argo_loader.profile(3900267, [2]).to_xarray() #Atlantic, south america
ds_points = argo_loader.profile(5905775, [35]).to_xarray() #indian ocean, off the coast of madagascar


ds = ds_points.argo.point2profile()

df = ds.to_dataframe()
df = df.reset_index(level='N_LEVELS') [['N_LEVELS','PRES','PSAL','TEMP']]

df = df.fillna(method='ffill').fillna(method='bfill')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns

from scipy.stats import pearsonr

def reg_coef(x,y,label=None,color=None,**kwargs):
    ax = plt.gca()
    r,p = pearsonr(x,y)
    ax.annotate('r = {:.2f}'.format(r), xy=(0.5,0.5), xycoords='axes fraction', ha='center', fontsize=25)
    ax.set_axis_off()

import matplotlib as mpl
mpl.rcParams["axes.labelsize"] = 20

g = sns.PairGrid(df)

g.map_diag(sns.histplot)
g.map_lower(sns.scatterplot, alpha=0.5)

g.map_upper(reg_coef)

g.savefig("corr.png")