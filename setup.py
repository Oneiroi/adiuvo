from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

'''
__author__="David Busby"
__copyright__="David Busby <d.busby@saiweb.co.uk>, Psycle Interactive Limited <david.busby@psycle.com>"
__license__="GNU v3 + part 5d section 7: Redistribution/Reuse of this code is permitted under the GNU v3 license, as an additional term ALL code must carry the original Author(s) credit in comment form."
'''

ext_modules = [Extension("apache_combined_parser",['modules/apache_combined_parser.pyx'])]
setup(
    Name = 'Adiuvo',
    cmdclass = {'build_ext':build_ext},
    ext_modules = ext_modules
)
