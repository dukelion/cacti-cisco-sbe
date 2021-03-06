#!/usr/bin/python
import sys
from Cisco import Cisco

def main():
	if len(sys.argv)<3:
		usage()
		exit(-1)

	host = sys.argv[1]
	cmd = sys.argv[2]

	if cmd == 'index':
		router = Cisco(host)
		trunks = router.get_trunks()
		for trunk in trunks:
			print "%s:" % trunk[0]
	elif cmd == 'num_indexes':
		router = Cisco(host)
		trunks = router.get_trunks()
		print len(trunks)
	elif cmd == 'query':
		router = Cisco(host)
		trunks = router.get_trunks()
		arg1 = sys.argv[3]
		if arg1 == 'trunkName':
			for trunk in trunks:
				print "%s|%s" % (trunk[0],trunk[0])
		elif arg1 == 'sbcTrunkStatus':
			for trunk in trunks:
				print "%s|%s" % (trunk[0],trunk[1])
		elif arg1 == 'sbcTrunkPingStatus':
			for trunk in trunks:
				print "%s|%s" % ( trunk[0], router.get_trunk_ping_status(trunk[0]))
		elif arg1 == 'sbcTrunkActiveCalls':
			for trunk in trunks:
				print "%s|%s" % (trunk[0],router.get_active_calls(trunk[0]))
		elif arg1 == 'sbcPeerInfo':
			for trunk in trunks:
				print "%s|%s" % (trunk[0],router.get_peer_details(trunk[0]))
		else:
			for trunk in trunks:
				print "%s:" % trunk[0]
	elif cmd == 'get':
		if len(sys.argv)<5:
			usage()
			exit(-1)
		trunk = sys.argv[4]
		arg2 = sys.argv[3]
		router = Cisco(host)
		if arg2 == 'trunkName':
			print "%s" % trunk
		elif arg2 == 'sbcTrunkStatus':
#			print "%s:%s" % (trunk,router.get_trunk_status(trunk))
			print "%s" % router.get_trunk_status(trunk)
		elif arg2 == 'sbcTrunkPingStatus':
#			print "%s:%s" % ( trunk, router.get_trunk_ping_status(trunk))
			print "%s" % router.get_trunk_ping_status(trunk)
		elif arg2 == 'sbcTrunkActiveCalls':
#			print "%s:%s" % (trunk,router.get_active_calls(trunk))
			print "%s" % router.get_active_calls(trunk)
		elif arg2 == 'sbcPeerInfo':
			print "%s" % router.get_peer_details(trunk)
		else:
			print trunk
	else:
		usage()
		exit(-1)

def usage():
	print  """Usage:
	%(command)s index
	%(command)s num_indexes
	%(command)s query {trunkName,sbcTrunkStatus,sbcTrunkPingStatus,sbcTrunkActiveCalls,sbcPeerInfo}
	%(command)s get {trunkName,sbcTrunkStatus,sbcTrunkPingStatus,sbcTrunkActiveCalls,sbcPeerInfo} TRUNK
"""%{'command': sys.argv[0]+ ' <hostname> <hostid> <credentials>'}
    
if __name__ == '__main__':
  main()
