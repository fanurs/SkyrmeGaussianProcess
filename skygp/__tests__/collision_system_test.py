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

# import the to-be-tested module
from collision_system import CollisionSystem

# create object from the module
coll_sys = CollisionSystem('Ca48', 'Sn124')

##--------------------------------------------------------------------##
class Test___init__:
    def test_TypeError(self):
        """`proj` and `targ` must be strings.
        `skyrme` must be an integer.
        `energy` must be a float.
        `imp_param` must be a float.
        """
        bad_args = [\
                (1, 2),\
                (1.0, 2.0),\
                (True, False),\
                ([1, 2], [3, 4]),\
                (1j, -1j),\
                ('Ca48', 'Sn124', 1.0),\
                ('Ca48', 'Sn124', [1]),\
                ('Ca48', 'Sn124', None, 1),\
                ('Ca48', 'Sn124', None, [1.0]),\
                ('Ca48', 'Sn124', None, None, 1),\
                ('Ca48', 'Sn124', None, None, [1.0]),\
                ]
        for arg in bad_args:
            with pytest.raises(TypeError):
                CollisionSystem(*arg)

##--------------------------------------------------------------------##
class Test_get_name:
    func = coll_sys.get_name # alias for function to be tested

    def test_TypeError(self):
        """`imqmd` must be boolean.
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
