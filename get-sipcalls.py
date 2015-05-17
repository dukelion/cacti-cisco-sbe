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
	calls = router.get_active_calls(trunkName)
	print calls

def usage():
	print  """Usage:
	%(command)s <hostName> <trunkName>
"""%{'command': sys.argv[0]}
    
if __name__ == '__main__':
  main()
