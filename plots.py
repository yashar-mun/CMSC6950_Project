from argopy import DataFetcher as ArgoDataFetcher
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np
import seaborn as sns

from scipy.stats import pearsonr

matplotlib.use('Agg')



def reg_coef(x,y,label=None,color=None,**kwargs):
    ax = plt.gca()
    r,p = pearsonr(x,y)
    ax.annotate('r = {:.2f}'.format(r), xy=(0.5,0.5), xycoords='axes fraction', ha='center', fontsize=25)
    ax.set_axis_off()

mpl.rcParams["axes.labelsize"] = 20

argo_loader = ArgoDataFetcher()

# A loop for image generation causes some errors in argo_loader.
# Time permitting, I'll look more into it.

ds_points1 = argo_loader.profile(5905775, [1]).to_xarray() #indian ocean, off the coast of madagascar
ds_points2 = argo_loader.profile(2900737, [3]).to_xarray() #Japan
ds_points3 = argo_loader.profile(3900267, [3]).to_xarray() #Atlantic, south america

ds1 = ds_points1.argo.point2profile()
ds2 = ds_points2.argo.point2profile()
ds3 = ds_points3.argo.point2profile()

df1 = ds1.to_dataframe()
df2 = ds2.to_dataframe()
df3 = ds3.to_dataframe()

df1 = df1.reset_index(level='N_LEVELS') [['N_LEVELS','PRES','PSAL','TEMP']]
df2 = df2.reset_index(level='N_LEVELS') [['N_LEVELS','PRES','PSAL','TEMP']]
df3 = df3.reset_index(level='N_LEVELS') [['N_LEVELS','PRES','PSAL','TEMP']]
    
df1 = df1.fillna(method='ffill').fillna(method='bfill')
df2 = df2.fillna(method='ffill').fillna(method='bfill')
df3 = df3.fillna(method='ffill').fillna(method='bfill')

g = sns.PairGrid(df1)
g.map_diag(sns.histplot)
g.map_lower(sns.scatterplot, alpha=0.5)
g.map_upper(reg_coef)
g.savefig("corr1.png")

g = sns.PairGrid(df2)
g.map_diag(sns.histplot, color = 'red')
g.map_lower(sns.scatterplot, alpha=0.5, color = 'red')
g.map_upper(reg_coef,color = 'red')
g.savefig("corr2.png")

g = sns.PairGrid(df3)
g.map_diag(sns.histplot, color = 'green')
g.map_lower(sns.scatterplot, alpha=0.5, color = 'green')
g.map_upper(reg_coef, color = 'green')
g.savefig("corr3.png")


