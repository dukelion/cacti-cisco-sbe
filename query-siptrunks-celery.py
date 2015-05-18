#!/usr/bin/python
import sys
import tasks as celery

def main():
	if len(sys.argv)<3:
		usage()
		exit(-1)

	host = sys.argv[1]
	cmd = sys.argv[2]

	timeout = 5

	if cmd == 'index':
		task = celery.get_trunks.delay(host)
		trunks = task.get(timeout=timeout)
		for trunk in trunks:
			print "%s:" % trunk[0]
	elif cmd == 'num_indexes':
		task = celery.get_trunks.delay(host)
		trunks = task.get(timeout=timeout)
		print len(trunks)
	elif cmd == 'query':
		task = celery.get_trunks.delay(host)
		trunks = task.get(timeout=timeout)
		arg1 = sys.argv[3]
		if arg1 == 'trunkName':
			for trunk in trunks:
				print "%s|%s" % (trunk[0],trunk[0])
		elif arg1 == 'sbcTrunkStatus':
			for trunk in trunks:
				print "%s|%s" % (trunk[0],trunk[1])
		elif arg1 == 'sbcTrunkPingStatus':
			for trunk in trunks:
				task = celery.get_trunk_ping_status.delay(host,trunk[0])
				ping_status = task.get(timeout=timeout)
				print "%s|%s" % ( trunk[0], ping_status)
		elif arg1 == 'sbcTrunkActiveCalls':
			for trunk in trunks:
				task = celery.get_active_calls.delay(host,trunk[0])
				active_calls = task.get(timeout=timeout)
				print "%s|%s" % (trunk[0],active_calls)
		else:
			for trunk in trunks:
				print "%s:" % trunk[0]
	elif cmd == 'get':
		if len(sys.argv)<5:
			usage()
			exit(-1)
		trunk = sys.argv[4]
		arg2 = sys.argv[3]
		if arg2 == 'trunkName':
			print "%s" % trunk
		elif arg2 == 'sbcTrunkStatus':
			task = celery.get_trunk_status.delay(host,trunk[0])
			status = task.get(timeout=timeout)
			print "%s" % status
		elif arg2 == 'sbcTrunkPingStatus':
			task = celery.get_trunk_ping_status.delay(host,trunk[0])
			ping_status = task.get(timeout=timeout)
			print "%s" % ping_status
		elif arg2 == 'sbcTrunkActiveCalls':
			task = celery.get_active_calls.delay(host,trunk[0])
			active_calls = task.get(timeout=timeout)
			print "%s" % active_calls
		else:
			print trunk
	else:
		usage()
		exit(-1)

def usage():
	print  """Usage:
	%(command)s index
	%(command)s num_indexes
	%(command)s query {trunkName,status,ping_status,active_calls}
	%(command)s get {trunkName,status,ping_status,active_calls} TRUNK
"""%{'command': sys.argv[0]+ ' <hostname> <hostid> <credentials>'}
    
if __name__ == '__main__':
  main()
