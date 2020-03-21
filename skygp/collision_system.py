"""Collision system is a module to handle the reading and manipulation systems.

Example:
----------
.. block::
    I'm trying a literal block

.. Section breaks are created with two blank lines.

"""
import re

class CollisionSystem:
    """`CollisionSystem`is a class to handle the reading and manipulation systems.
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
