# CMSC6950_Project
Course project for CMSC6950 Spring 2021

Yashar Tavakoli

## Environment setup

```
bash Miniforge3-Linux-x86_64.sh
conda create -n argopy
```

## Software setup

```
conda install xarray fsspec scikit-learn erddapy gsw aiohttp netCDF4 dask toolz
conda create -n argopy
```
For full argopy functionalities, also:

```
conda install ipython ipywidgets tqdm Matplotlib Cartopy Seaborn
```

## Some basic import/export testing with argopy

```
import matplotlib
matplotlib.use('Agg')
import import matplotlib.pyplot as plt
from argopy import IndexFetcher as ArgoIndexFetcher

idx = ArgoIndexFetcher().float([6902745, 6902746])
idx.to_dataframe()
idx.plot('trajectory')
plt.title('Testing argopy native plotting')
plt.savefig("argo.png")
```