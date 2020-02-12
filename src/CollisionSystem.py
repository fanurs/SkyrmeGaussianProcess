class CollisionSystem:
    def __init__(self, proj=None, targ=None, skyrme=None, energy=None, imp_param=None):
        """
        Initialize the collision system.

        `proj`: A `str` to describe the projectile nucleus.

        `targ`: A `str` to describe the target nucleus.

        `skyrme`: The Skyrme number. Actual Skyrme parameters have to be known.

        `energy`: Beam energy in $MeV/u$.
        
        `imp_param`: Impact parameter in fm.

        """

        self.proj_symb = (''.join(re.findall('[A-z]+', proj))).lower()
        self.proj_A = int(''.join(re.findall('[0-9]+', proj)))
        self.targ_symb = (''.join(re.findall('[A-z]+', targ))).lower()
        self.targ_A = int(''.join(re.findall('[0-9]+', targ)))
        self.skyrme = skyrme
        self.energy = energy
        self.imp_param = imp_param

        # construct the ImQMD directory name / readable name
        self.name = self.proj_symb + str(self.proj_A)
        self.name += self.targ_symb + str(self.targ_A)
        self.name += '_%03d' % self.skyrme
        self.name += 'e%d' % self.energy
        self.name += 'b%d' + self.imp_param
        self.name += 'x-1' # ImQMD version number (?)

        return

    def __str__(self):
        return '<CollisionSystem> name: ' + self.name

