"""`data_manager` is a module to handle the reading and manipulation simulation data.

Example:
----------
.. block::
    I'm trying a literal block

.. Section breaks are created with two blank lines.

"""
import re
import numpy as np
import pandas as pd
import itertools as itr

class CollisionSystem:
    """`CollisionSystem` is a class to handle the reading and manipulation systems.
    """

    def __init__(self, proj, targ, skyrme=None, energy=None, imp_param=None):
        """Initialize the collision system.

        Parameters:
            proj : str
                To describe the projectile nucleus with a string containing the
                element symbol and mass number.

            targ : str
                To describe the target nucleus with a string containing the
                element symbol and mass number.

            skyrme : int *optional*
                The Skyrme number that represents a set of Skyrme parameters.

            energy : float *optional*
                Beam energy in MeV/u.

            imp_param : float *optional*
                Impact parameter in femtometer.

        Examples:
        ----------
        Consider a beam particle of calcium-48 hitting on target nickel-64
        with a beam energy of 140 MeV/u. This can be created by

        >>> coll_sys = CollisionSystem('ca48', 'ni64', energy=140.0)
        >>> print(coll_sys)
        <CollisionSystem> name: ca48ni64_e140

        """

        self.proj_symb = (''.join(re.findall('[A-z]+', proj))).lower()
        self.proj_A = int(''.join(re.findall('[0-9]+', proj)))
        self.targ_symb = (''.join(re.findall('[A-z]+', targ))).lower()
        self.targ_A = int(''.join(re.findall('[0-9]+', targ)))

        if skyrme is not None and not isinstance(skyrme, int):
            raise TypeError('skyrme must be an integer.')
        self.skyrme = skyrme

        if energy is not None and not isinstance(energy, float):
            raise TypeError('energy must be an integer.')
        self.energy = energy

        if imp_param is not None and not isinstance(imp_param, float):
            raise TypeError('imp_param must be an integer.')
        self.imp_param = imp_param

        self.name = self.get_name(imqmd=False)

    def get_name(self, imqmd=False):
        """Construct the ImQMD directory name.

        This also provides a string of readable name to inspect the collision
        system.

        Parameters:
            imqmd : bool *optional*
                If `True`, the system name will be formatted like
                `'ca48ni64_001e140b2x-1'`. If `False`, an ordinary readable name
                will be coined. Default is `False`.

        Returns:
            name : str
                A readable name or a name formatted for ImQMD program.

        """
        if imqmd is not None and not isinstance(imqmd, bool):
            raise TypeError('imqmd must be a boolean.')

        name = self.proj_symb + str(self.proj_A)
        name += self.targ_symb + str(self.targ_A)

        # decide to add underscore or not
        name_items = [self.skyrme, self.energy, self.imp_param]
        add_underscore = not all(ele is None for ele in name_items)
        name += '_' if add_underscore else ''

        name += '%03d' % self.skyrme if self.skyrme is not None else ''
        name += 'e%d' % self.energy if self.energy is not None else ''
        name += 'b%d' + self.imp_param if self.imp_param is not None else ''
        name += 'x-1' if imqmd else '' # ImQMD version number (?)
        return name

    def __str__(self):
        return '<CollisionSystem> name: ' + self.name

class SimulationReader:
    """`SimulationReader` process simulation outputs.
    """

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.filename = 'NP-EK-A16Z6.DAT'
        self.file_header = ['beam_E', 'imp_param', 'ene_cm', \
                            'yield_p', 'yield_p_err', 'yield_n', 'yield_n_err', \
                            'single_ratio', 'single_ratio_err' \
                           ]
        self.param_filename = 'param.dat'

    def get_data(self, subdir_fmt_numer, subdir_fmt_denom, param_codes, energy_range):
        # check subdir_fmt
        for string in [subdir_fmt_numer, subdir_fmt_denom]:
            if not (string.count('%') and string.count('%03d')):
                raise ValueError('"%s" should contain exactly one placeholder "%%03d".' % string)

        # read in the `x_train`
        path = '%s/%s' % (self.data_dir, self.param_filename)
        x_train = pd.read_csv(path, delim_whitespace=True)

        # read in the `y_train`
        y_train = []
        header_train = []
        for code in param_codes:
            df_sr = dict()
            numer = subdir_fmt_numer % code
            denom = subdir_fmt_denom % code
            for subdir in [numer, denom]:
                path = '%s/%s/%s' % (self.data_dir, subdir, self.filename)
                df = pd.read_csv(path, names=self.file_header, delim_whitespace=True)
                df = df[['ene_cm', 'single_ratio']]
                df = df[(df['ene_cm'] >= energy_range[0])]
                df = df[(df['ene_cm'] <= energy_range[1])]
                df = df.astype(float)
                df_sr[subdir] = df

            # check if ene_cm column is identical in both systems
            ene_cm = list(df_sr[numer]['ene_cm'])
            if ene_cm != list(df_sr[denom]['ene_cm']):
                raise ValueError('Systems for calculating double ratio have inconsistent ene_cm')

            # check if ene_cm identical to previous ene_cm
            if header_train == []:
                header_train = ene_cm
            else:
                if header_train != ene_cm:
                    raise ValueError('Mismatch ene_cm for parameter code %03d' % skyrme)

            # calculate the double ratio
            df_dr = df_sr[numer].copy()
            df_dr.rename(columns={'single_ratio': 'double_ratio'}, inplace=True)
            df_dr['double_ratio'] /= df_sr[denom]['single_ratio']

            # append to training data
            y_train.append(list(df_dr['double_ratio']))

        # finalize the formats of x_train and y_train
        x_train.set_index('code', inplace=True)
        x_train = x_train.reindex(param_codes)
        header_train = ['ene_cm_%03d' % ele for ele in header_train]
        y_train = pd.DataFrame(y_train, columns=header_train)
        y_train['code'] = param_codes
        y_train.set_index('code', inplace=True)

        return x_train, y_train
