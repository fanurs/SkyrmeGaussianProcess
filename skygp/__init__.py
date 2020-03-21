"""
# `skygp` - Skyrme Gaussian Process

Source code: https://github.com/Fanurs/SkyrmeGaussianProcess/

Documentation: https://fanurs.github.io/SkyrmeGaussianProcess/


Developed by Chi-En Teh (Fanurs) for the class CMSE-802.

<p align="center">
  This repository is under development. The expected date of completion: April 2020.
</p>

## What do these directories contain?
- `skygp/`: Source codes of this sofware.
- `WeeklyReports/`: Weekly assignments that are due on every Friday.
- `docs/`: Documentation of this software.
- `tutorials/`: A collection of `.ipynb` and `.py` that demonstrate the usage of this program.

## Tutorials
- [Gaussian emulator basics](https://github.com/Fanurs/SkyrmeGaussianProcess/blob/master/tutorials/TUT-emulating_a_toy_model.ipynb) or [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Fanurs/SkyrmeGaussianProcess/blob/master/tutorials/TUT-emulating_a_toy_model.ipynb)

## Physics objective
Project title: Constraining Skyrme with Bayesian inference on heavy-ion collisions and Gaussian-emulated ImQMD

### Overview
<p align="justify">
The studies of nuclear physics are typically categorized into two approaches. The first approach is the so-called "ab initio methods" that seeks for a bottom-up model to describe nuclei. But just like any many-body problems, nuclear dynamics involves interactions among multiple neutrons and protons, making it very difficult to be solved even with the help of modern computers. This motivates physicists to come up with a second approach that describes atomic nuclei phenomenologically.
</p>

## Requirements (to do: write a script to check and install automatically for users)
### Operating system
- Linux: Ok. All developments are made here so far.
- OS X: Never tested. Maybe ok.
- Windows: Not available yet. E.g. path names will be incompatible.

### Python modules
- numpy (version?)
- matplotlib (version?)
- sklearn (version >= 0.22.1): for sklearn.gaussian_process.GaussianProcessRegressor
- pytest (version?)

"""
from .collision_system import *
from .gaussian_emulator import *
