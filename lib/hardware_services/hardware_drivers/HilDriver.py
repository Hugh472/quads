# this class will inherit from hardware_service.py and overwrite all of its methods
# with hil-specific behaviors - mostly through api calls to the HIL server

from datetime import datetime
import calendar
import time
import yaml
import argparse
import os
import sys
import requests
import logging
from subprocess import call
from subprocess import check_call

from hardware_services.hardware_service import HardwareService

# Hardcoded to the default
hil_url = 'http://127.0.0.1:5000'

class HilDriver(HardwareService):

    def update_cloud(self, quadsinstance, **kwargs):
	#No REST API Call to update Project Label
	#if kwargs['description'] is None:
        #   parent.logger.error("--description is required when using --define-cloud")
        #    exit(1)
        #else:
	    #description = kwargs['description']
	    #quadsinstance.quards_rest_call("POST", hil_url, '/project/'+description)#fix
	cloudResource = kwargs['cloudresource'] #What is this? The cloud name?
	if cloudResource:
        	print "creating project in HIL named " + cloudResource
       		quadsinstance.quads_rest_call('PUT', hil_url, '/project/' + cloudResource)     #EC528 addition
        	print "adding network to HIL and attaching it to " + cloudResource
        	quadsinstance.quads_rest_call('PUT', hil_url, '/network/' + cloudResource, {"owner": cloudResource, "access": cloudResource, "net_id": ""})  #EC528 addition
	

    def update_host(self, quadsinstance, **kwargs):
    	hostCloud = kwargs['hostcloud']
	if kwargs['hostcloud'] is None:
            quadsinstance.logger.error("--default-cloud is required when using --define-host")
            exit(1)
        else:
	    	#quadsinstance.quads_rest_call("PUT", hil_url, '/node/'+hostCloud)#fix
		hostResource = kwargs['hostresource']
		#quadsinstance.quads_rest_call("PUT", hil_url, '/node/'+hostResource)#fix
		forceUpdate = kwargs['forceupdate']

		print "attaching HIL node " + hostResource + " to project " + hostCloud
       		quadsinstance.quads_rest_call('POST', hil_url, '/project/' + hostCloud + '/connect_node', {'node': hostResource}) 
      	  	#print "defining QUADS host " + hostResource + " and adding it to " + hostCloud + " in QUADS data"
        	quadsinstance.quads_update_host(hostResource, hostCloud, forceUpdate)
        	#exit(0)

    def remove_cloud(self, quadsinstance, **kwargs):
        #print "removed cloud"
	targetCloud = kwargs['rmcloud']
	quadsinstance.quads_rest_call("DELETE", hil_url, '/project/'+targetCloud)
	quadsinstance.quads_rest_call("DELETE", hil_url, '/network/'+targetCloud) 

    def remove_host(self, quadsinstance, **kwargs):
	targetHost = kwargs['rmhost']
	quadsinstance.quads_rest_call("DELETE", hil_url, '/node/'+targetHost)
	print "removed host "+targetHost 

    def move_hosts(self, quadsinstance, **kwargs):
	print "moved host"

    def list_clouds(self, quadsinstance):
	quadsinstance.quads_rest_call("GET", hil_url, '/projects') #Testing 

    def list_hosts(self, quadsinstance):
	quadsinstance.quads_rest_call("GET", hil_url, '/nodes/all') #Testing 

