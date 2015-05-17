#!/usr/bin/python
import paramiko
import time
import re
import socket
import ConfigParser
import sys

#logfile = '/tmp/siptrunks.log'
#paramiko.util.log_to_file(logfile,level=10)


class Cisco:
	"""Cisco SSH helper"""
	timeout = 5
	def get_trunks(self):
		output = self.run_cmd("show sbc 1 sbe adjacencies")
		out_lines = output.splitlines()
		
		del out_lines[0:4] #Remove header lines
		del out_lines[-2:] # Remove trailing prompt

		regex = re.compile(r'\s+(?P<name>\S+)\s+SIP\s+(?P<status>\S+)\s+(?P<description>.*)$')
		
		result = []
		for line in out_lines:
			if not line:
				continue
			match = regex.match(line)
			if match: 
				result.append(match.groups())
		return result
	
	def get_trunk_ping_status(self,trunk_name):
		output = self.run_cmd("show sbc 1 sbe adjacencies %s det | in [Ss]tatus"%trunk_name)
		out_lines  = output.splitlines()

		regex = re.compile(r'\s+Ping Peer Status:\s+(\S+\s*\S*)',re.I)

		status = 'Unknown'
		for line in out_lines:
			if not line:
				continue
			match = regex.match(line)
			if match:
				status = match.group(1)

		if status[0:2] == 'On':
			return 1
		if status[0:2] == 'Of':
			return 0
		return -1

	def get_trunk_status(self,trunk_name):
		output = self.run_cmd("show sbc 1 sbe adjacencies %s det | in [Ss]tatus"%trunk_name)
		out_lines  = output.splitlines()

		regex = re.compile(r'\s+Signaling-peer status:\s+(\S+\s*\S*)',re.I)


		status = 'Unknown'
		for line in out_lines:
			if not line:
				continue
			match = regex.match(line)
			if match:
				status = match.group(1)
		if status[0:2] == 'Up':
			return 1
		if status[0:2] == 'Do':
			return 0
		if status[0:2] == 'Wa':
			return -2
		if status[0:2] == 'No':
			return -1
		return -1

	def get_active_calls(self,trunk_name):
		output = self.run_cmd("show sbc 1 sbe call-stats adjacency %s emergence"%trunk_name)
		out_lines  = output.splitlines()

		regex = re.compile(r'\s+Total active calls = (\d+)',re.I)

		calls = 0
		for line in out_lines:
			if not line:
				continue
			match = regex.match(line)
			if match:
				calls = int(match.group(1))
				return calls
		return calls
		

	def __init__(self,hostname):
		
		config = ConfigParser.ConfigParser()
		try:
			config.read(['./ciscologin.cfg',"/etc/ciscologin.cfg"])
		except ConfigParser.ParsingError as e:
			print "Config format incorrect\n" + e.message
			exit(1)

		username = config.get('ciscossh','username')
		password = config.get('ciscossh','password')

		# Create instance of SSHClient object
		self.remote_conn_pre = paramiko.SSHClient()

		# Automatically add untrusted hosts (make sure okay for security policy in your environment)
		self.remote_conn_pre.set_missing_host_key_policy(
		paramiko.AutoAddPolicy())

		try:
			self.remote_conn_pre.connect(hostname, username=username, password=password, allow_agent=False, look_for_keys=False, timeout=self.timeout)
		except socket.error, (value,message):
			print >> sys.stderr, "Unable to connect to %s@%s: (%d) %s\n" % (username,hostname,value,message)
			exit(-1)
		except Exception, e:
			print >> sys.stderr, "Unable to connect to %s@%s (%s)" % (username,hostname,e)
			exit(-1)
#		print "SSH connection established to %s" % ip

		# Use invoke_shell to establish an 'interactive session'
		self.shell = self.remote_conn_pre.invoke_shell()
#		print "Interactive SSH session established"

		# Strip the initial router prompt
		output = self.shell.recv(1000)

		# See what we have
#		print "Connected: "+output

		self.run_cmd('')

		# Turn off paging
		self.run_cmd("terminal length 0")

	def run_cmd(self,cmd):
		'''Run command and wait for prompt ending in #'''
		self.shell.send(cmd+'\n')
		rbuf = ''
		start = time.time()
		
		while (not "#" in rbuf) or(time.time()-start>self.timeout):
			rbuf +=self.shell.recv(1024)

		return rbuf
