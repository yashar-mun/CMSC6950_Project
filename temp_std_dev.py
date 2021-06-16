from argopy import DataFetcher as ArgoDataFetcher
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

import numpy as np


argo_loader = ArgoDataFetcher()

ds_points = argo_loader.float(3900267).to_xarray()
 
ds = ds_points.argo.point2profile()
df = ds.to_dataframe()
df = df.reset_index(level='N_LEVELS') [['N_LEVELS','PSAL','TEMP','TIME']]

#print(df.head())
#print(ds_points.keys)

df['TEMP'] = df['TEMP'] /df['TEMP'].abs().max()
df['PSAL'] = df['PSAL'] /df['PSAL'].abs().max()


TEMP = pd.Series(df['TEMP'])
TEMP = pd.concat([pd.Series([0]), TEMP]).reset_index()
TEMP = TEMP[:-1]

PSAL = pd.Series(df['PSAL'])
PSAL = pd.concat([pd.Series([0]), PSAL]).reset_index()
PSAL = PSAL[:-1]

df = df.reset_index()

df['TEMP'] = abs(df['TEMP'] - TEMP)
df['PSAL'] = abs(df['PSAL'] - PSAL)

df['DIFF'] = df['TEMP'] - df['PSAL']

print(df['DIFF'])

z_min, z_max = -np.abs(df['DIFF']).max(), np.abs(df['DIFF']).max()
c = plt.pcolormesh(df['TIME'], df['N_LEVELS'], df['DIFF'], cmap ='Greens', vmin = z_min, vmax = z_max)
#plt.colorbar(c)

plt.savefig("diff.png")
