# this is a library to conveniently do REST calls to HIL server

import requests
import sys
import yaml
import os

def error_check(response):
    if response.status_code < 200 or response.status_code >= 300:
        sys.exit(response.text)
    else:
        print(response.text)
    return response.json()

def make_url(*args):
    filename = os.path.join(os.path.dirname(__file__), "..", "..", "..", "conf", "quads.yml")
    with open(filename, 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError:
            sys.exit("Can't parse quads.yml file.")
    url = data.get('hardware_service_url')
    if url is None:
        sys.exit("Hil url is not specified in quads.yml.")
    for arg in args:
        url += '/' + arg
    return url

def do_put(url, data={}):
    error_check(requests.put(url, data=json.dumps(data)))

def do_post(url, data={}):
    error_check(requests.post(url, data=json.dumps(data)))

def do_get(url, params=None):
    return error_check(requests.get(url, params=params))

def do_delete(url):
    error_check(requests.delete(url))

def network_create_simple(network, project):
    if project is None:
        project = network
    url = make_url('network', network)
    do_put(url, data={'owner': project,
                      'access': project,
                      'net_id': ""})

def network_delete(network):
    url = make_url('network', network)
    do_delete(url)

def list_projects():
    url = make_url('projects')
    return do_get(url)

def project_create(project):
    url = make_url('project', project)
    do_put(url)

def project_delete(project):
    url = make_url('project', project)
    do_delete(url)

def project_connect_node(project, node):
    url = make_url('project', project, 'connect_node')
    do_post(url, data={'node': node})

def project_detach_node(project, node):
    url = make_url('project', project, 'detach_node')
    do_post(url, data={'node': node})

def node_connect_network(node, nic, network, channel='null'):
    # use default value nic='nic'
    url = make_url('node', node, 'nic', nic, 'connect_network')
    do_post(url, data={'network': network,
                       'channel': channel})

def node_detach_network(node, nic, network):
    # use default value nic='nic'
    url = make_url('node', node, 'nic', nic, 'detach_network')
    do_post(url, data={'network': network})

def list_nodes(is_free='all'):
    if is_free not in ('all', 'free'):
        sys.exit("list_nodes should have 'all' or 'free'")
    url = make_url('nodes', is_free)
    return do_get(url)

def list_project_nodes(project):
    url = make_url('project', project, 'nodes')
    return do_get(url)

def list_project_networks(project):
    url = make_url('project', project, 'networks')
    return do_get(url)

def list_networks():
    url = make_url('networks')
    return do_get(url)

def show_network(network):
    url = make_url('network', network)
    return do_get(url)

def show_node(node):
    url = make_url('node', node)
    return do_get(url)

