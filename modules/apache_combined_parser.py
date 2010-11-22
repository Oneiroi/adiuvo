#!/usr/bin/env python
import re,sys,os,mmap,time,MySQLdb

'''
__author__="David Busby"
__copyright__="David Busby <d.busby@saiweb.co.uk>, Psycle Interactive Limited <david.busby@psycle.com>"
__license__="GNU v3 + part 5d section 7: Redistribution/Reuse of this code is permitted under the GNU v3 license, as an additional term ALL code must carry the original Author(s) credit in comment form."
'''

 #this was not fun to type!
'''
Not needed at this time
http_code = {
                     100:{'desc':'continue'},
                     101:{'desc':'switching protocol'},
                     200:{'desc':'OK'},
                     201:{'desc':'created'},
                     202:{'desc':'accepted'},
                     203:{'desc':'Non-Authoritative Information'},
                     204:{'desc':'No content'},
                     205:{'desc':'Reset content'},
                     206:{'desc':'Partial content'},
                     300:{'desc':'Multiple choices'},
                     301:{'desc':'Moved permanently'},
                     302:{'desc':'Found'},
                     303:{'desc':'See other'},
                     304:{'desc':'Not modified'},
                     305:{'desc':'Use proxy'},
                     #306 deprecated
                     307:{'desc':'Temporary redirect'},
                     400:{'desc':'Bad request'},
                     401:{'desc':'Unauthorised'},
                     402:{'desc':'Payment required'},
                     403:{'desc':'Forbidden'},
                     404:{'desc':'Not found'},
                     405:{'desc':'Method not allowed'},
                     406:{'desc':'Not acceptable'},
                     407:{'desc':'Proxy Auth Required'},
                     408:{'desc':'Request timeout'},
                     409:{'desc':'Conflict'},
                     410:{'desc':'Gone'},
                     411:{'desc':'Length required'},
                     412:{'desc':'Precondition Failed'},
                     413:{'desc':'Request Entity Too Large'},
                     414:{'desc':'Request-URI Too Long'},
                     415:{'desc':'Unsupported Media Type'},
                     416:{'desc':'Requested Range Not Satisfiable'},
                     417:{'desc':'Expectation Failed'},
                     500:{'desc':'Internal Server Error'},
                     501:{'desc':'Not Implemented'},
                     502:{'desc':'Bad Gateway'},
                     503:{'desc':'Service Unavailable'},
                     504:{'desc':'Gateway Timeout'},
                     505:{'desc':'HTTP Version Not Supported'}
                 }
'''
'''
This function will assume the DB details you pass have a mySQL table named

apache_data

CREATE TABLE apache_data (
	id INT AUTO_INCREMENT PRIMARY_KEY,
	ip VARCHAR(255),
	request_time INT(11),
	method VARCHAR(6),
	uri VARCHAR(255),
	http_code TINYINT(3),
	bytes INT,
	referer VARCHAR(255),
	user_agent VARCHAR(255)
)

'''

def parse_by_hour(logPath):
    '''Abort if logpath does not exits'''
    if not os.path.isfile(logPath):
        print 'Could not find',logPath
        sys.exit(1)
    r = re.compile('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)[^[]+\[([0-9]+\/[a-z]+\/[0-9]+:[0-9]+:[0-9]+:[0-9]+)\s[0-9\+|-]+\]\s"([a-z]+)\s([^\s]+)\s[^"]+"\s([0-9]{3})\s([0-9]+)\s"([^"]+)"\s"([^"]+)"',re.IGNORECASE)
    '''
		1 - ip
		2 - time
		3 - method
		4 - uri
		5 - http_code
		6 - bytes
		7 - referer
		8 - user agent
    '''
    res = {}
    for line in open(logPath,'r'):
        for m in r.finditer(line):
                ip 		= m.group(1)
                rtime 		= time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(m.group(2),'%d/%b/%Y:%H:%M:%S')) #convert to mySQL time
                method 		= m.group(3)
                uri 		= m.group(4)	#Whilst rare, this could contain injection code, let's escape it
                http_code 	= int(m.group(5))
                bytes 		= int(m.group(6))
                referer		= m.group(7)	#Whilst rare, this could contain injection code, let's escape it
                user_agent	= m.group(8) #Whilst rare, this could contain injection code, let's escape it
                try:
                    res[re.split(':',rtime)[0]]['bytes']+=bytes
                    res[re.split(':',rtime)[0]]['rcount']+=1
                except:
                    res.update({re.split(':',rtime)[0]:{'bytes':bytes,'rcount':1}})

    print 'hour,bytes,requests'
    for hour in res:
        print '%s,%s,%s' % (hour,res[hour]['bytes'],res[hour]['rcount'])
                    
                
def parse_to_mysql(logPath,mysql_host,mysql_user,mysql_pass,mysql_db):
	'''Abort if logpath does not exits'''
        if not os.path.isfile(logPath):
		print 'Could not find',logPath
		sys.exit(1)
	'''@todo: A multiline expr, and processing in say 1000 line chunks may be more efficent, esp as this means you could mmap said chunk
	I could not get this to work at the time of writing though'''
	#r = re.compile('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s-\s[^\]]+\]\s"(.*)"\s([0-9]+)\s(-|[0-9]+)')
	'''@todo: add support for UTC offsets, not presently working, having to skip in regex capture'''
	r = re.compile('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)[^[]+\[([0-9]+\/[a-z]+\/[0-9]+:[0-9]+:[0-9]+:[0-9]+)\s[0-9\+|-]+\]\s"([a-z]+)\s([^\s]+)\s[^"]+"\s([0-9]{3})\s([0-9]+)\s"([^"]+)"\s"([^"]+)"',re.IGNORECASE)
	'''
		1 - ip
		2 - time
		3 - method
		4 - uri
		5 - http_code
		6 - bytes
		7 - referer
		8 - user agent
	'''
	db=MySQLdb.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,db=mysql_db)
	c = db.cursor()
	c.execute('SET NAMES utf8;')
	for line in open(logPath,'r'):
		for m in r.finditer(line):
			ip 		= m.group(1)
			rtime 		= time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(m.group(2),'%d/%b/%Y:%H:%M:%S')) #convert to mySQL time	
			method 		= m.group(3)		
			uri 		= db.literal(m.group(4))	#Whilst rare, this could contain injection code, let's escape it
			http_code 	= int(m.group(5))		
			bytes 		= int(m.group(6))		
			referer		= db.literal(m.group(7))	#Whilst rare, this could contain injection code, let's escape it
			user_agent	= db.literal(m.group(8)) #Whilst rare, this could contain injection code, let's escape it
			
			''' @todo: Sanity check for allready processed entry '''
			''' @todo: add checking here to ensure data has been entered correctly '''
			c.execute('''   INSERT INTO apache_data (ip,request_time,method,uri,http_code,bytes,referer,user_agent)
                                        VALUES ("%s","%s","%s","%s",%d,%d,"%s","%s") ''' % (ip,rtime,method,uri,http_code,bytes,referer,user_agent))


if __name__ == '__main__':
	parse_by_hour('./test.log')
