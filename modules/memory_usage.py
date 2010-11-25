import glob
import re
import os

'''
__author__="Matthew Ife,David Busby"
__copyright__="David Busby <d.busby@saiweb.co.uk>, Psycle Interactive Limited <david.busby@psycle.com>"
__license__="GNU v3 + part 5d section 7: Redistribution/Reuse of this code is permitted under the GNU v3 license, as an additional term ALL code must carry the original Author(s) credit in comment form."

This script adapted from the original provided by Matthew Ife, this is inteded to give a more accurate projection of memory usage.

One known issue where this helps is with apache & php APC, where the RSS size per thread is reported incorrectly and the majority of size per thread is infact the apc SHM, this makes it difficult in projecting memory usage
and subsequently tuning apache threads to fit in memory and provide the bext performance
'''

ispid = re.compile("/proc/([0-9]+)")
pssinfo = re.compile("Private.+:\s+([0-9]+)")
files = glob.glob('/proc/*')

for apid in files:
        m = ispid.match(apid)
        if not m:
                continue
        pid = m.group(1)

        try:
                data = open(os.path.join(apid,'smaps')).read(512000)
                stat = open(os.path.join(apid,'stat')).read(512000).split(" ")[1]
        except IOError:
                continue
        m = pssinfo.findall(data)
        m = map(int,m)
        a = 0
        for b in m:
                a += b
        print "%d %s %s" % (a, pid, stat)
