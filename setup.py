from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("apache_combined_parser",['modules/apache_combined_parser.py'])]
setup(
    Name = 'Adiuvo',
    cmdclass = {'build_ext':build_ext},
    ext_modules = ext_modules
)
