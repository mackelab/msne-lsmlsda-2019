# LSMLSDA exercises and mini-projects
This repository belongs to the Large Scale Modelling and Large Scale Data Analysis course at TUM: [moodle link](https://www.moodle.tum.de/course/view.php?id=48594).

## Usage and contribtion
You find exercises in the `exercises` folder, and mini-projects in the
`mini-projects` folder.

### Contribution workflow
All students can push to this repository. This requires that everyone adapts a certain workflow in order to avoid conflicts. 

When adding code to this repository, create a [local branch first](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging). The name of the branch should be your group name or, if it is for a different assignment, a unique and desciptive name. Push the local branch to the remote and then make a [pull request](https://help.github.com/en/articles/about-pull-requests) to merge it into the master branch. 

Add code exclusively to the `your-code` folder: create a folder with
your group name, e.g., `group1`, in the `your-code` folder and work exclusively in this folder.

## Setup
We recommend to use [conda environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for managing your Python packages. To
create a conda environment named `lsmlsda` execute

`conda create --name lsmlsda python=3.5.6`

Activate your newly create conda env with `source activate lsmlsda`. Then install additional packages with

`conda install -c anaconda notebook numpy scipy matplotlib pandas`. 
