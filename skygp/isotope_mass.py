"""This module interacts with the atomic mass data.

By the time of writing this module, the latest available data is
Atomic Mass Evaluation in 2016 (AME2016). When future evaluation
is released, manual modification needs to be made by updating
`DataManager.AME_URL` as well as `DataManager.read_in_data` if the
format of the table has been changed.
"""

import inspect
import os
import re
import requests
from stat import S_IREAD, S_IRGRP, S_IROTH

from astropy import constants, units
import pandas as pd

# identifies the project directory (`SkyrmeGaussianProcess/`)
# and module directory (`SkyrmeGaussianProcess/skygp/`)
FILE_PATH = os.path.realpath(inspect.getsourcefile(lambda: 0))
MODULE_DIR = os.path.dirname(FILE_PATH)
PROJECT_DIR = os.path.realpath(os.path.join(MODULE_DIR, os.pardir))
del FILE_PATH # to avoid variable name contamination

class DataManager:
    """A class to interacts with the atomic masses.

    Many kinematic calculations require the knowledge of masses of atomic
    isotopes. This class allows user to automatically download the data
    sheet of Atomic Mass Evaluation to local machine, and perform some
    simple query tasks on the table.

    """
    AME_URL = 'https://www-nds.iaea.org/amdc/ame2016/mass16.txt'
    AME_LOCAL_PATH = '%s/database/mass16.txt' % PROJECT_DIR

    def __init__(self, force_download=False):
        """This creates a `DataManager` object.

        A local copy has to be present before any query task can be made.
        Hence this initializer downloads the data if local copy is not
        present yet, or the user has decided to turn on the `force_download`
        option.

        Parameters:
            force_download : bool *optional*
                If `True`, a new local copy will always be downloaded from
                the website (see class variable `AME_URL`). If `False`, the
                program only downloads the data when no local copy is found.
                Default is `False`.

        """
        # download from web if local copy is not found
        file_exists = os.path.isfile(self.AME_LOCAL_PATH)
        if force_download or not file_exists:
            if file_exists: os.remove(self.AME_LOCAL_PATH)
            self.download()
        self.read_in_data()

        # other class attributes to be updated
        self.df = None # a `pandas.DataFrame for storing AME data
        self.units = None # units for every column in self.df
        self.Z_to_symb = None
        self.symb_to_Z = None

    def download(self, filepath=None, url=None):
        """Download AME data from the web.

        Parameters:
            filepath : str *optional*
                The local filepath that store the downloaded data. Default is
                `None`, which will then be set into class variable `AME_LOCAL_PATH`.

            url : str *optional*
                The url to the AME data. Default is `None`, which will then be
                set into class variable `AME_URL`.

        """
        if filepath is None: filepath = self.AME_LOCAL_PATH
        if url is None: url = self.AME_URL

        with open(filepath, 'w') as f:
            # to pretend as a web browser; for some reason, DataManager.AME_URL cannot be accessed otherwise
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36', \
                       'X-Requested-With': 'XMLHttpRequest', \
                      }
            content = requests.get(url, headers=headers).text
            f.write(content)
        
        # set file to be read only for protection
        os.chmod(filepath, S_IREAD | S_IRGRP | S_IROTH)

    def read_in_data(self, filepath=None):
        """Updates class attribute `self.df` into formatted AME data.

        This function only reads from a local copy of AME data. Make sure the data
        has been downloaded from the web. Not all columns from AME data will be kept.
        The columns that will be returned are `Z`, `A`, `symb`, `mass_excess` and
        `mass_excess_err`. Other columns including isospin, binding energy (and its
        error) and mass in a.m.u (and its error) are discarded as they can all be
        calculated directly from mass excess.

        No unit conversion has been made. The AME provides mass excess in $\mathrm{keV/c^2}$.
        Nonetheless, units have been stored as class attribute `self.units` as python
        dictionary using `astropy.units`.

        Parameters:
            filepath : str *optional*
                The local filepath that store the downloaded data. Default is
                `None`, which will then be set into class variable `AME_LOCAL_PATH`.

        """
        if filepath is None: filepath = self.AME_LOCAL_PATH

        # check if file can be opened
        try:
            with open(filepath, 'r') as f:
                content = f.readlines()
        except IOError:
            print('fail to read in %s' % filepath)

        # crop to select only the table data in content
        first_line_of_data = -1
        start_token = '0'
        start_token_count = 0
        for line_i, line in enumerate(content):
            if line[0] == start_token:
                start_token_count += 1
            if start_token_count >= 3:
                first_line_of_data = line_i
                break
        content = content[line_i:]

        content = self.auto_column_splitter(content)
        
        # A lot of HARD-CODED codes from now on. They are written
        # according to the format of the table. The goal is to transform
        # `content` into a `pandas.DataFrame` with appropriate format.

        # construct `pandas.DataFrame` for columns of interest
        column_dict = {3: 'Z', 4: 'A', 5: 'symb',
                       7: 'mass_excess', 8: 'mass_excess_err'}
        content = [[row[i] for i in column_dict.keys()] for row in content]
        df = pd.DataFrame(content, columns=column_dict.values())

        # cast each column into appropriate variable type
        df['Z'] = df['Z'].astype(int)
        df['A'] = df['A'].astype(int)
        df['symb'] = df['symb'].str.extract(r'([A-Za-z]+)')
        df['mass_excess'] = df['mass_excess'].str.extract(r'([0-9.]+)').astype(float)
        df['mass_excess_err'] = df['mass_excess_err'].str.extract(r'([0-9.]+)').astype(float)

        # construct mapping from `Z` to `symb`
        Z_to_symb = dict(zip(df['Z'], df['symb']))

        # IUPAC announces official names for new elements in 2016
        new_symb = {113: 'Nh', 115: 'Mc', 117: 'Ts', 118: 'Og'}
        old_to_new_symb = {Z_to_symb[k]: new_symb[k] for k in new_symb.keys()}
        df.replace({'symb': old_to_new_symb}, inplace=True)
        for k, v in new_symb.items():
            Z_to_symb[k] = v

        # construct mapping from `symb` to `Z`
        symb_to_Z = {v: k for k, v in Z_to_symb.items()}

        # update to class attributes
        df.set_index(['A', 'Z'], drop=False, inplace=True, verify_integrity=True)
        self.df = df
        self.units = {'Z': None, 'A': None, 'symb': None,
                      'mass_excess': units.keV,
                      'mass_excess_err': units.keV}
        self.Z_to_symb = Z_to_symb
        self.symb_to_Z = symb_to_Z

    @staticmethod
    def auto_column_splitter(content):
        """This function automatically separates the columns of `.txt` table.

        This function can separate the columns of `.txt` tables that use space
        characters as their delimiters.

        Parameters:
            content : list of str
                A list of strings that correspond to the content of a `.txt` table.
                Each element in the list, which is a string, corresponds to each row
                of the table. These strings can be either ended with the newline
                character `\n` or not. The row of column names or headers should not
                be included.

        Returns:
            splitted_content : a two-dimensional list of str

        Examples:
        ----------
        >>> from isotope_mass import DataManager
        >>> dm = DataManager()
        >>> content = ["Amy  168.5cm", "Bob  181.9cm", "Cici 157.3cm"]
        >>> dm.auto_column_splitter(content)
        [['Amy  ', '168.5cm'], ['Bob  ', '181.9cm'], ['Cici ', '157.3cm']]

        """
        min_line_length = min([len(line) for line in content])
        split_pos = []
        for c in range(1, min_line_length):
            is_col_splitter = True
            is_all_space = True
            for line in content:
                if line[c] != ' ':
                    is_all_space = False
                if line[c] != ' ' and line[c-1] != ' ':
                    is_col_splitter = False
                if not is_all_space and not is_col_splitter:
                    break
            if is_col_splitter and not is_all_space:
                split_pos.append(c)
        
        splitted_content = []
        split_pos = [0] + split_pos
        for line in content:
            line = line.strip('\n')
            splitted_line = []
            for c0, c1 in zip(split_pos[:-1], split_pos[1:]):
                splitted_line.append(line[c0:c1])
            splitted_line.append(line[c1:])
            splitted_content.append(splitted_line)
        
        return splitted_content

data_manager = DataManager()

def get_A_Z(notation):
    """Converts mass-number annotated isotope expression into A and Z.

    Examples:
    ----------
    >>> import isotope_mass as isom
    >>> isom.get_A_Z('ca40')
    (40, 20)
    """
    global data_manager
    symb_to_Z = data_manager.symb_to_Z

    expected_regex = re.compile(r'([A-Za-z][a-z]?\d{1,3}|\d{1,3}[A-Za-z][a-z]?)')
    matches = expected_regex.findall(notation)
    if (len(matches) != 1):
        raise ValueError('notation "%s" has unexpected format' % notation)
    match = matches[0]
    digit_part = ''.join(filter(str.isdigit, match))
    alpha_part = ''.join(filter(str.isalpha, match))

    A = int(digit_part)
    symb = alpha_part.capitalize()
    if symb not in symb_to_Z.keys():
        raise ValueError('chemical symbol "%s" is unidentified' % symb)
    else:
        Z = symb_to_Z[symb]

    return A, Z

def get_mass(argv, unit=units.MeV):
    """Get mass of isotope.
    """
    global data_manager
    df = data_manager.df
    df_units = data_manager.units

    if isinstance(argv, str):
        A, Z = get_A_Z(argv)
    elif isinstance(argv, tuple) and len(argv) == 2:
        A, Z = tuple

    if (A, Z) not in df.index:
        raise ValueError('"(A, Z) = (%d, %d)" not found' % (A, Z))

    amu = constants.u.to(units.MeV, units.mass_energy())
    mass_excess = units.Quantity(df.loc[(A, Z)]['mass_excess'], df_units['mass_excess'])
    mass = A * amu + mass_excess
    return mass.value

