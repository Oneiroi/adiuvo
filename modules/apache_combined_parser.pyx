import re,sys,os,mmap,time,MySQLdb

cdef char* ip,rtime,method,uri,referer,user_agent,line
cdef int http_code,bytes


cdef void parse_by_hour( char* logPath ):
    if not os.path.isfile( logPath ):
        print 'Could not find',logPath
        sys.exit(1)
    else:
         r = re.compile('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)[^[]+\[([0-9]+\/[a-z]+\/[0-9]+:[0-9]+:[0-9]+:[0-9]+)\s[0-9\+|-]+\]\s"([a-z]+)\s([^\s]+)\s[^"]+"\s([0-9]{3})\s([0-9]+)\s"([^"]+)"\s"([^"]+)"',re.IGNORECASE)
         res = {}

    for line in open( logPath, 'r' ):
        for m in r.finditer(line):
            ip 		= m.group(1)
            rtime 	= time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(m.group(2),'%d/%b/%Y:%H:%M:%S')) #convert to mySQL time
            method 	= m.group(3)
            uri 	= m.group(4)	#Whilst rare, this could contain injection code, let's escape it
            http_code 	= int(m.group(5))
            bytes 	= int(m.group(6))
            referer	= m.group(7)	#Whilst rare, this could contain injection code, let's escape it
            user_agent	= m.group(8) #Whilst rare, this could contain injection code, let's escape it
            try:
                res[re.split(':',rtime)[0]]['bytes']+=bytes
                res[re.split(':',rtime)[0]]['rcount']+=1
            except:
                res.update({re.split(':',rtime)[0]:{'bytes':bytes,'rcount':1}})

        print 'hour,bytes,requests'
        for hour in res:
            print '%s,%s,%s' % (hour,res[hour]['bytes'],res[hour]['rcount'])