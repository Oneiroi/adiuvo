import sys
from ctypes import *
if len(sys.argv) < 1:
	print 'usage:'
	print sys.argv[0],' /path/to/combined.log'
	sys.exit(1)
cdll.LoadLibrary('build/lib.macosx-10.6-universal-2.6/apache_combined_parser.so')
from build/lib.macosx-10.6-universal-2.6/apache_combined_parser import *
#acp.parse_by_hour(sys.argv[1])
print dir(acp)
