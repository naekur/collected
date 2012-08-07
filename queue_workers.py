#!/usr/bin/env python
# coding: utf-8

import sys
import simplejson
from twisted.web import client
from twisted.python import log
from twisted.internet import reactor
from pymongo import Connection
class CometClient(object):
    def __init__(self):
	self.connection = Connection()
	self.db = self.connection.collected
    def write(self, content):
	for json in content.splitlines():
        	try:
            		data = simplejson.loads(json)
			data = simplejson.loads(data['value'])
        	except Exception, e:
            		log.err("cannot decode json: %s" % str(e))
			pass
        	else:
			for values in data:
				self.write2mongo(values)
#	    	self.write2comet(value)
    def write2mongo(self,data):
	collection = self.db[data['host']]
        collection.insert(data)
    def write2comet(self,host,data):
	client.getPage('http://localhost/pub?host=%s' % data['host'],postdata=data)
    def close(self):
        pass

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    client.downloadPage("http://localhost/c/collectd_data", CometClient())
    reactor.run()
