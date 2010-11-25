import sys
from ctypes import *
if len(sys.argv) < 1:
	print 'usage:'
	print sys.argv[0],' /path/to/combined.log'
	sys.exit(1)
from apache_combined_parser import *
parse_by_hour(sys.argv[1])