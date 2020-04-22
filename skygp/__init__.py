"""
# `skygp` - Skyrme Gaussian Process

Developed by Chi-En Teh (Fanurs) for the class CMSE-802.

Source code: https://github.com/Fanurs/SkyrmeGaussianProcess/

Documentation: https://fanurs.github.io/SkyrmeGaussianProcess/

Documentation is automatically generated with `pdoc3`. By running `$ ./run_doc.sh skygp/`, the `./docs/*.html` files will be updated accordingly.

## What do these directories contain?
- `skygp/`: Source codes of this sofware.
- `WeeklyReports/`: Weekly assignments that are due on every Friday.
- `docs/`: Documentation of this software.
- `tutorials/`: A collection of `.ipynb` and `.py` that demonstrate the usage of this program.

## Tutorials
- [Gaussian emulator basics](https://github.com/Fanurs/SkyrmeGaussianProcess/blob/master/tutorials/TUT-emulating_a_toy_model.ipynb) or [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Fanurs/SkyrmeGaussianProcess/blob/master/tutorials/TUT-emulating_a_toy_model.ipynb)
- [Emulating ImQMD data](https://github.com/Fanurs/SkyrmeGaussianProcess/blob/master/tutorials/TUT-demonstrating_gaussian_emulation.ipynb) or [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Fanurs/SkyrmeGaussianProcess/blob/master/tutorials/TUT-demonstrating_gaussian_emulation.ipynb)
- [A very short example](https://github.com/Fanurs/SkyrmeGaussianProcess/blob/master/tutorials/TUT-a_very_short_example.py)

## Physics objective
Project title: Constraining Skyrme with Bayesian inference on heavy-ion collisions and Gaussian-emulated ImQMD

### Overview
<p align="justify">
The studies of nuclear physics are typically categorized into two approaches. The first approach is the so-called "ab initio methods" that seeks for a bottom-up model to describe nuclei. But just like any many-body problems, nuclear dynamics involves interactions among multiple neutrons and protons, making it very difficult to be solved even with the help of modern computers. This motivates physicists to come up with a second approach that describes atomic nuclei phenomenologically.
</p>

## Requirements
- See `./environment.yml`.

### Operating system
- Linux: Ok. All developments are made here so far.
- OS X: Never tested. Maybe ok.
- Windows: Not available yet. E.g. path names will be incompatible.

"""
from .data_manager import *
from .gaussian_emulator import *
from .isotope_mass import *
