## Getting started with BRIAN

To work with the newest version of Brian you need to install `brian2`. For most of
the mini-projects you additionally need a python package developed in Wulfram
Gerstners group at EPFL, called `neurodynex`.

You want to install these packages inside of your `lsmlsda` conda environment so
that they do not interfere with other packages or python versions on your system
(neurodynex needs python=3.5.6).

## Installation
1) activate the conda environment. Depending on your system this is
  - `conda activate lsmlsda` (linux)
  - `source activate lsmlsda` (mac os)
  - `activate lsmlsda`(windows)
2) install Brian 2:
  - `conda install -c brian-team brian2`
  - the `-c` selects the channel from which you want to obtain your package
3) install neurodynex
  - `conda install -c epfl-lcn neurodynex`

## Tutorials
There are very well designed tutorials for getting started with Brian on the brian
website.

I downloaded the corresponding jupyter notebooks from the [website](https://brian2.readthedocs.io/en/stable/resources/tutorials/index.html) and put them in this folder. You
can therefore just pull the latest version of this repository and then start working
on the notebooks locally.

1) [intro-to-brian neurons](1-intro-to-brian-neurons.ipynb)
2) [intro-to-brian synapses](2-intro-to-brian-synapses.ipynb)
3) [intro-to-brian simulations](3-intro-to-brian-simulations.ipynb)
