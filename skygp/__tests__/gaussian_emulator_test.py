# identify the directory that contains skygp modules to be tested
import sys
import os
import inspect
import pytest
FILE_PATH = os.path.realpath(inspect.getsourcefile(lambda: 0))
FILE_DIR = os.path.dirname(FILE_PATH)
SKYGP_DIR = os.path.realpath(os.path.join(FILE_DIR, os.pardir))
sys.path.append(SKYGP_DIR)

# modules that facilitate the writing of test functions
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# import the to-be-tested module
from gaussian_emulator import GaussianEmulator

# create object from the module
gmu = GaussianEmulator()

##--------------------------------------------------------------------##
class Test_set_niterations:
    func = gmu.set_niterations # alias for function to be tested

    def test_TypeError(self):
        """`n_itr` must be integer.
        """
        bad_args = [\
                [1, 2],\
                1.0,\
                1j,\
                'str',\
                ]
        for arg in bad_args:
            with pytest.raises(TypeError):
                self.func(arg)

##--------------------------------------------------------------------##
class Test_fit:
    func = gmu.fit # alias for function to be tested
    good_arg = (np.array([[0.0, 0.0], [0.1, 0.1], [0.2, 0.2]]),
                np.array([[1.0, 1.0], [2.1, 2.1], [3.2, 3.2]]))

    def test_TypeError(self):
        """`x` and `y` must be numpy array.
        """
        bad_args = [\
                (1, 2),\
                ([[0.0, 0.1], [0.2, 0.3]], [[1.0, 1.1], [1.2, 1.3]]),\
                ('x', 'y'),\
                ]
        for arg in bad_args:
            with pytest.raises(TypeError): self.func(*arg)

    def test_ValueError(self):
        """`x` and `y` must be two-dimensional
        """
        bad_args = [\
                (np.array([1, 2]), np.array([3, 4])),\
                ]
        for arg in bad_args:
            with pytest.raises(ValueError):
                self.func(*arg)

##--------------------------------------------------------------------##
class Test_predict:
    func = gmu.predict # alias for function to be tested
    good_arg = np.array([[0.0, 0.0], [0.1, 0.1], [0.2, 0.2]])

    def test_TypeError(self):
        """`x` must be a numpy array.
        """
        bad_args = [\
                1,\
                1.0,\
                True,\
                'str',\
                [1, 2, 3],\
                [[1, 2], [3, 4]],\
                ]
        for arg in bad_args:
            with pytest.raises(TypeError):
                self.func(arg)

##--------------------------------------------------------------------##
class Test_inspect_training_xslice:
    func = gmu.predict # alias for function to be tested

    def test_TypeError(self):
        """`ix` must be an integer.
        `ax` must be matplotlib.axes.Axes if not `None`.
        """
        _, ax = plt.subplots()
        bad_args = [\
                (1.0, None),\
                (1j, None),\
                (True, None),\
                ('str', None),\
                ([1, 2], None),\
                (0, 1),\
                ]
        for arg in bad_args:
            with pytest.raises(TypeError):
                self.func(*arg)
