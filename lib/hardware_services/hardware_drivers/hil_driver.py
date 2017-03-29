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
	if not kwargs['cloudowner']:
                cloudOwner = "nobody"
	else:
		cloudOwner = kwargs['cloudowner']
	print "cloudOwer is "+cloudOwner
	#Add conditional to see if user alredy exists
	quadsinstance.quads_rest_call("PUT", hil_url, '/auth/basic/user/'+cloudOwner+'{\npassword: password\nisadmin: True\n}') #add the user
	quadsinstance.quads_rest_call("POST", hil_url, '/auth/basic/user/'+cloudOwner+'/add_project {"project": '+cloudResource) #Is cloudResource = cloud name? I don't see any other option

	#cloudTicket = kwargs['cloudticket] No analog in HIL
	

    def update_host(self, quadsinstance, **kwargs):
	print "updated host"
	#if kwargs['hostcloud'] is None:
         #   parent.logger.error("--default-cloud is required when using --define-host")
          #  exit(1)
        #else:
	#    hostCloud = kwargs['hostcloud']
	#    quadsinstance.quads_rest_call("PUT", hil_url, '/node/'+hostCloud)#fix
	#hostResource = kwargs['hostresource']
	#quadsinstance.quads_rest_call("PUT", hil_url, '/node/'+hostResource)#fix
	#schedule =  kwargs['schedule']

    def remove_cloud(self, quadsinstance, **kwargs):
        #print "removed cloud"
	targetProject = kwargs['rmcloud']
	quadsinstance.quads_rest_call("DELETE", hil_url, '/project/'+targetProject) 

    def remove_host(self, quadsinstance, **kwargs):
        print "removed host"
	targetHost = kwargs['rmhost']
	quadsinstance.quads_rest_call("DELETE", hil_url, '/node/'+targetHost) 

    def move_hosts(self, quadsinstance, **kwargs):
	print "moved host"

    def list_clouds(self, quadsinstance):
	quadsinstance.quads_rest_call("GET", hil_url, '/projects') #Testing 

    def list_hosts(self, quadsinstance):
	quadsinstance.quads_rest_call("GET", hil_url, '/nodes/all') #Testing 

