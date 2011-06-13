import sys
from ctypes import *
if len(sys.argv) < 1:
	print 'usage:'
	print sys.argv[0],' /path/to/combined.log'
	sys.exit(1)
import apache_combined_parser
apache_combined_parser.parse_by_hour(sys.argv[1])
