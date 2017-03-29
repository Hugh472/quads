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

# added for EC528 HIL-QUADS integration project - not a good place for this variable - should be moved eventually
hil_url = 'http://127.0.0.1:5000'

class HilDriver(HardwareService):

    def update_cloud(self, quadsinstance, **kwargs):
        print "updated cloud"

    def update_host(self, quadsinstance, **kwargs):
        print "Updated host"

    def remove_cloud(self, quadsinstance, **kwargs):
        #print "removed cloud"
	targetProject = kwargs['rmcloud']
	quadsinstance.quads_rest_call("DELETE", hil_url, '/project/'+targetProject) 


    def remove_host(self, quadsinstance, **kwargs):
        print "removed host"
	targetHost = kwargs['rmhost']
	quadsinstance.quads_rest_call("DELETE", hil_url, '/node/'+targetHost) 

    def move_hosts(self, quadsinstance, **kwargs):
        print "moved hosts"

    def list_clouds(self, quadsinstance):
	quadsinstance.quads_rest_call("GET", hil_url, '/projects') #Testing 

    def list_hosts(self, quadsinstance):
	quadsinstance.quads_rest_call("GET", hil_url, '/nodes/all') #Testing 

