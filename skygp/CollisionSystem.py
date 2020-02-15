"""Collision system is a class to handle the reading and manipulation systems.  

Example:
----------
.. Let's try to use a literal block::
    $ from skygp import CollisionSystem


.. Section breaks are created with two blank lines.

"""
class CollisionSystem:
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

        >>> sys = CollisionSystem('ca48', 'ni64')
        <CollisionSystem> name: ca48ni64 

        """

        self.proj_symb = (''.join(re.findall('[A-z]+', proj))).lower()
        self.proj_A = int(''.join(re.findall('[0-9]+', proj)))
        self.targ_symb = (''.join(re.findall('[A-z]+', targ))).lower()
        self.targ_A = int(''.join(re.findall('[0-9]+', targ)))
        self.skyrme = skyrme
        self.energy = energy
        self.imp_param = imp_param

        return

    def get_name(self, imqmd=False):
        """Construct the ImQMD directory name.

        This also provides a string of readable name to inspect the collision
        system.

        Parameters:
            imqmd : bool *optional*
                If `True`, the system name will be formatted like
                `'ca48ni64_001e%140b2x-1'`. If `False`, an ordinary readable name
                will be coined. Default is `False`.

        Returns:
            name : str
                A readable name or a name formatted for ImQMD program.

        """
        self.name = self.proj_symb + str(self.proj_A)
        self.name += self.targ_symb + str(self.targ_A)
        self.name += '_%03d' % self.skyrme if self.skyrme is not None else ''
        self.name += 'e%d' % self.energy if self.energy is not None else ''
        self.name += 'b%d' + self.imp_param if self.imp_param is not None else ''
        self.name += 'x-1' if imqmd else '' # ImQMD version number (?)
        return self.name

    def __str__(self):
        return '<CollisionSystem> name: ' + self.name

