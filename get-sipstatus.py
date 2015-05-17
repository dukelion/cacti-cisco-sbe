#!/usr/bin/python
import sys
from Cisco import Cisco

def main():
	if len(sys.argv)<3:
		usage()
		exit(-1)

	host = sys.argv[1]
	trunkName = sys.argv[2]

	router = Cisco(host)
	status = router.get_trunk_status(trunkName)
	ping_status = router.get_trunk_ping_status(trunkName)
	print "status:%s pingStatus:%s" % (status, ping_status)

def usage():
	print  """Usage:
	%(command)s <hostName> <trunkName>
"""%{'command': sys.argv[0]}

    
if __name__ == '__main__':
  main()
