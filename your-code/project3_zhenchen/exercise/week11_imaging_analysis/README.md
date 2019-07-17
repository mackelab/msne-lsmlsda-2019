# Calcium imaging analysis exercises

## Requirements

With conda:
```
conda install numpy scipy pandas matplotlib ipywidgets scikit-image scikit-learn numba pytables
```

Optinal, recommended, for interactive plots in the notebook:

```bash
conda install -c conda-forge ipympl

# If using the Notebook
conda install -c conda-forge widgetsnbextension

# If using JupyterLab
conda install nodejs
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-matplotlib
```

And with pip:

```bash
pip install deepdish # for serializing Python, Numpy and Pandas structures in HDF5
```