from celery import Celery,Task
from Cisco import Cisco

app = Celery()
app.config_from_object('celeryconfig')

class SshExec(Task):
	abstract = True
	routers = dict()

	def getRouter(self,host):
		if not self.routers.has_key(host):
			self.routers[host] = Cisco(host)
		return self.routers[host]

@app.task(base=SshExec)
def get_trunks(host):
	router = get_trunks.getRouter(host)
	return router.get_trunks()

@app.task(base=SshExec)
def get_trunk_ping_status(host,trunk):
	router = get_trunk_ping_status.getRouter(host)
	return router.get_trunk_ping_status(trunk)

@app.task(base=SshExec)
def get_active_calls(host,trunk):
	router = get_active_calls.getRouter(host)
	return router.get_active_calls(trunk)

@app.task(base=SshExec)
def get_trunk_status(host,trunk):
	router = get_trunk_status.getRouter(host)
	return router.get_trunk_status(trunk)
	
