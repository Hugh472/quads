# inherits from hardware_service.py and overwrites methods. This is a mock driver for testing purposes and will not be attached to any specific hardware
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

from hardware_services.inventory_service import InventoryService

class MockInventoryDriver(InventoryService):

    def update_cloud(self, quadsinstance, **kwargs):
        description = kwargs['description']
        cloudresource = kwargs['cloudresource']
        forceupdate = kwargs['forceupdate']
        cloudowner = kwargs['cloudowner']
        cloudticket = kwargs['cloudticket']
        qinq = kwargs['qinq']
        ccusers = kwargs['ccusers']

        if description is None:
            quadsinstance.logger.error("--description is required when using --define-cloud")
            exit(1)
        else:
            if cloudresource in quadsinstance.quads.clouds.data and not forceupdate:
                quadsinstance.logger.error("Cloud \"%s\" already defined. Use --force to replace" % cloudresource)
                exit(1)
            if not cloudowner:
                cloudowner = "nobody"
            if not cloudticket:
                cloudticket = "00000"
            if not qinq:
                qinq = "0"
            if not ccusers:
                ccusers = []
            else:
                ccusers = ccusers.split()
            if cloudresource in quadsinstance.quads.clouds.data:
                if 'ccusers' in quadsinstance.quads.clouds.data[cloudresource]:
                    savecc = []
                    for cc in quadsinstance.quads.clouds.data[cloudresource]['ccusers']:
                        savecc.append(cc)
                else:
                    savecc = []
                if 'description' in quadsinstance.quads.clouds.data[cloudresource]:
                    save_description = quadsinstance.quads.clouds.data[cloudresource]['description']
                else:
                    save_description = ""
                if 'owner' in quadsinstance.quads.clouds.data[cloudresource]:
                    save_owner = quadsinstance.quads.clouds.data[cloudresource]['owner']
                else:
                    save_owner = "nobody"
                if 'qinq' in quadsinstance.quads.clouds.data[cloudresource]:
                    save_qinq = quadsinstance.quads.clouds.data[cloudresource]['qinq']
                else:
                    save_qinq = '0'
                if 'ticket' in quadsinstance.quads.clouds.data[cloudresource]:
                    save_ticket = quadsinstance.quads.clouds.data[cloudresource]['ticket']
                else:
                    save_ticket = '000000'
                quadsinstance.quads.cloud_history.data[cloudresource][int(time.time())] = {'ccusers':savecc,
                                                       'description':save_description,
                                                       'owner':save_owner,
                                                       'qinq':save_qinq,
                                                       'ticket':save_ticket}

            quadsinstance.quads.clouds.data[cloudresource] = { "description": description, "networks": {}, "owner": cloudowner, "ccusers": ccusers, "ticket": cloudticket, "qinq": qinq }
            quadsinstance.quads_write_data()

        return

    def update_host(self, quadsinstance, **kwargs):
        if kwargs['hostcloud'] is None:
            quadsinstance.logger.error("--default-cloud is required when using --define-host")
            exit(1)
        else:
            if kwargs['hostcloud'] not in quadsinstance.quads.clouds.data:
                print "Unknown cloud : %s" % kwargs['hostcloud']
                print "Define it first using:  --define-cloud"
                exit(1)
            if kwargs['hostresource'] in quadsinstance.quads.hosts.data and not kwargs['forceupdate']:
                quadsinstance.logger.error("Host \"%s\" already defined. Use --force to replace" % kwargs['hostresource'])
                exit(1)

            if kwargs['hostresource'] in quadsinstance.quads.hosts.data:
                quadsinstance.quads.hosts.data[kwargs['hostresource']] = { "cloud": kwargs['hostcloud'], "interfaces": self.quads.hosts.data[kwargs['hostresource']]["interfaces"],
                    "schedule": quadsinstance.quads.hosts.data[kwargs['hostresource']]["schedule"] }
                quadsinstance.quads.history.data[kwargs['hostresource']][int(time.time())] = kwargs['hostcloud']
            else:
                quadsinstance.quads.hosts.data[kwargs['hostresource']] = { "cloud": kwargs['hostcloud'], "interfaces": {}, "schedule": {}}
                quadsinstance.quads.history.data[kwargs['hostresource']] = {}
                quadsinstance.quads.history.data[kwargs['hostresource']][0] = kwargs['hostcloud']
            quadsinstance.quads_write_data()

            return


    def remove_cloud(self, quadsinstance, **kwargs):
        # remove a cloud (only if no hosts use it)
        if kwargs['rmcloud'] not in quadsinstance.quads.clouds.data:
            print kwargs['rmcloud'] + " not found"
            return
        for h in quadsinstance.quads.hosts.data:
            if quadsinstance.quads.hosts.data[h]["cloud"] == kwargs['rmcloud']:
                print kwargs['rmcloud'] + " is default for " + h
                print "Change the default before deleting this cloud"
                return
            for s in quadsinstance.quads.hosts.data[h]["schedule"]:
                if quadsinstance.quads.hosts.data[h]["schedule"][s]["cloud"] == kwargs['rmcloud']:
                    print kwargs['rmcloud'] + " is used in a schedule for "  + h
                    print "Delete schedule before deleting this cloud"
                    return
        del(quadsinstance.quads.clouds.data[kwargs['rmcloud']])
        quadsinstance.quads_write_data()

        return

    def remove_host(self, quadsinstance, **kwargs):
        # remove a specific host
        print(quadsinstance)
        #print(kwargs)
        if kwargs['rmhost'] not in quadsinstance.quads.hosts.data:
            print kwargs['rmhost'] + " not found"
            return
        del(quadsinstance.quads.hosts.data[kwargs['rmhost']])
        quadsinstance.quads_write_data()

        return


    def list_clouds(self,quadsinstance):
        quadsinstance.quads.clouds.cloud_list()

    def list_hosts(self,quadsinstance):
        quadsinstance.quads.hosts.host_list()

    def load_data(self, quadsinstance, force):
        if initialize:
            quadsinstance.quads_init_data(force)
        try:
            stream = open(quadsinstance.config, 'r')
            quadsinstance.data = yaml.load(stream)
            stream.close()
        except Exception, ex:
            quadsinstance.logger.error(ex)
            exit(1)

    def write_data(self, quadsinstance, doexit = True):
        quadsinstance.quads_write_data_(doexit)

    def sync_state(self, quadsinstance):
        quadsinstance.quads_sync_state_()

    def init_data(self, quadsinstance, force):
        quadsinstance.quads_init_data_(force)



