import sys
sys.path.append('../') # append repository's home directory to identify module
import skygp.isotope_mass as isom

print(isom.get_mass('Ca40'))
