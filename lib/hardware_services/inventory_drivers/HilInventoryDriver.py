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
import json
import urllib
import time
from subprocess import call
from subprocess import check_call
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from libquads import Quads

from hardware_services.inventory_service import InventoryService


class HilInventoryDriver(InventoryService):


    def update_cloud(self, quadsinstance, **kwargs):
        self.__project_create(quadsinstance.hardware_service_url, kwargs['cloudresource'])
        self.__project_create_network(quadsinstance.hardware_service_url, kwargs['cloudresource'])


    def update_host(self, quadsinstance, **kwargs):
        cloud = kwargs['hostcloud']
        host = kwargs['hostresource']
        hilurl = quadsinstance.hardware_service_url

        self.__project_connect_node(hilurl, cloud, host)
        node_info = self.__show_node(hilurl, host).json()
        for nic in node_info['nics']:        # a node in quads will only have one nic per network
            self.__node_connect_network(hilurl, host, nic['label'], cloud)



    def remove_cloud(self, quadsinstance, **kwargs):
        cloud = kwargs['rmcloud']
        self.__network_delete(quadsinstance.hardware_service_url, cloud)
        self.__project_delete(quadsinstance.hardware_service_url, cloud)


    def remove_host(self,quadsinstance, **kwargs):
        host = kwargs['rmhost']
        hilurl = quadsinstance.hardware_service_url

        # first detach host from network
        node_info = self.__show_node(hilurl, host).json()
        for nic in node_info['nics']:        # a node in quads will only have one nic per network
            self.__node_detach_network(hilurl, host, nic['label'], node_info['project'])


        # then detach host from project
        self.__project_detach_node(hilurl, node_info['project'], host)



    def list_clouds(self, quadsinstance):
        #projects = quadsinstance.quads_rest_call("GET", hil_url, '/projects')
        #print projects.text
        print self.__list_projects(quadsinstance.hardware_service_url).text


    def list_hosts(self, quadsinstance):
        hosts = self.__list_nodes(quadsinstance.hardware_service_url)
        #hosts_yml = yaml.dump(json.loads(hosts.text), default_flow_style=False)
        print hosts.text


    def load_data(self, quads, force):
        """
        """

    def init_data(self, quads, force):
        """
        """

    def sync_state(self, quads):
        """
        """

    def write_data(self, quads, doexit = True):
        """
        """

    ######################################################################################################
    # the following private methods are based on the HIL cli and are wrappers for the hil rest api calls #
    ######################################################################################################

    def __list_projects(self, hil_url):
        """ lists all projects """

        url = Quads.quads_urlify(hil_url, 'projects')
        return Quads.quads_get(url)


    def __project_create_network(self, hil_url, project):
        """ creates network belonging to project of the same name """

        url = Quads.quads_urlify(hil_url, 'network', project)
        Quads.quads_put(url, data={'owner': project,
                              'access': project,
                              'net_id': ""})


    def __project_connect_node(self, hil_url, project, node):
        """ connects node to project """

        url = Quads.quads_urlify(hil_url, 'project', project, 'connect_node')
        Quads.quads_post(url, data={'node': node})


    def __project_detach_node(self, hil_url, project, node):
        """ Detaches node from project. Will fail if node is connected to any project networks """

        url = Quads.quads_urlify(hil_url, 'project', project, 'detach_node')
        Quads.quads_post(url, data={'node': node })


    def __network_delete(self, hil_url, network):
        """ Deletes network. Will fail if network has nodes connected to it """

        url = Quads.quads_urlify(hil_url, 'network', network)
        Quads.quads_delete(url)


    def __project_create(self, hil_url, project):
        """ creates new project """
        url = Quads.quads_urlify(hil_url, 'project', project)
        Quads.quads_put(url)


    def __project_delete(self, hil_url, project):
        """ Deletes project. Will fail if project has any connected nodes or networks """
        url = Quads.quads_urlify(hil_url, 'project', project)
        Quads.quads_delete(url)


    def __list_nodes(self, hil_url, is_free='all'):
        """ lists nodes. If is_free is set to free, only lists unallocated nodes """

        if is_free not in ('all', 'free'):
            sys.exit("error listing hosts. is_free is not set to all or free")
        url = Quads.quads_urlify(hil_url, 'nodes', is_free)
        return Quads.quads_get(url)


    def __show_node(self, hil_url, node):
        """ returns data associated with specified node """

        url = Quads.quads_urlify(hil_url, 'node', node)
        return Quads.quads_get(url)


    def __node_connect_network(self, hil_url, node, nic, network, channel=None):
        """ connects specified node to specified network on the specified nic """

        """ If channel is None, it is set automatically to the default value on the HIL server side, however is kept here as a
        parameter in case it ever needs to be specified. """

        if channel is not None:
            network_data = { 'network': network,
                             'channel': channel }
        else:
            network_data = { 'network': network }

        url = Quads.quads_urlify(hil_url, 'node', node, 'nic', nic, 'connect_network')
        Quads.quads_post(url, data=network_data)

        # Hil network server needs time to process request
        time.sleep(2)


    def __node_detach_network(self, hil_url, node, nic, network):
        """ detaches node from network """

        url = Quads.quads_urlify(hil_url, 'node', node, 'nic', nic, 'detach_network')
        Quads.quads_post(url, data={'network': network})

        # Hil network server needs time to process request
        time.sleep(2)










