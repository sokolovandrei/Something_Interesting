# -*- coding: utf-8 -*-

from pprint import pprint
import ipaddress
import getpass
import re
import sys
import os
import requests
from netmiko import ConnectHandler, NetMikoAuthenticationException
#export NET_TEXTFSM=/home/andrey_s/scripts/Something_Interesting/ntc-templates/templates
# set NET_TEXTFSM=C:\Study\Python_New\ntc-templates-master\templates

user = input('Введите username: ')
password = "1qaz!QAZ"#getpass.getpass('Введите password: ')
ip_addr = input('Введите адреса устройств через запятую: ')

device_params = []
for ip in ip_addr.split(','):
        try:
            if ipaddress.ip_address(ip):
                devices = {
                'device_type': 'cisco_ios',
    		    'ip': ip,
    		    'username': user,
    		    'password': password,
		        }
                device_params.append(devices)
        except ValueError as error:
            print(error)
            sys.exit('ip address введен некорректно!')

def take_device_conf(device_params):
    info_show = []
    host = {}
    for device in device_params:
        with ConnectHandler(**device) as ssh:
            show_hostname = ssh.send_command('sh run  |  i hostname').strip('hostname')
            host = {'hostname': show_hostname}
            command_output = ssh.send_command('sh cdp neighbors',use_textfsm=True)
            command_output.append(host)
            info_show.append(command_output)
            result = info_show
    return result

def topology(list_info=None):
    list_dict = take_device_conf(device_params)
    result = {}
    for dict_first in list_dict:
        data = []
        for i in dict_first:
            if 'hostname' not in i.keys():
                l_intf = i.get('local_interface')
                neighbor = i.get('neighbor').strip('.cisco.com')
                n_intf = i.get('neighbor_interface')
                data.append([l_intf, neighbor, n_intf])
            if 'hostname' in i.keys():
                for intfs in data:
                    info = {}
                    host = i.get('hostname').strip()
                    info[(host, intfs[0])] = (intfs[1], intfs[2])
                    result.update(info)
                    network_map = {}
                    for key, value in result.items():
                            if not network_map.get(value) == key:
                                   network_map[key] = value
    return network_map

try:
    import graphviz as gv
except ImportError:
    print("Module graphviz needs to be installed")
    print("pip install graphviz")
    sys.exit()

styles = {
    'graph': {
        'label': 'Network Map',
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'BT',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'circle',
        'fontcolor': 'white',
        'color': '#006699',
        'style': 'filled',
        'fillcolor': '#006699',
        'margin': '0.4',
    },
    'edges': {
        'style': 'dashed',
        'color': 'green',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '16',
        'fontcolor': 'white',
    }
}


def apply_styles(graph, styles):
    graph.graph_attr.update(('graph' in styles and styles['graph']) or {})
    graph.node_attr.update(('nodes' in styles and styles['nodes']) or {})
    graph.edge_attr.update(('edges' in styles and styles['edges']) or {})
    return graph


def draw_topology(output_filename='img/topology'):

    topology_dict = topology()
    nodes = set([
        item[0]
        for item in list(topology_dict.keys()) + list(topology_dict.values())
    ])

    g1 = gv.Graph(format='svg')

    for node in nodes:
        g1.node(node)

    for key, value in topology_dict.items():
        head, t_label = key
        tail, h_label = value
        g1.edge(
            head, tail, headlabel=h_label, taillabel=t_label, label=" " * 12)

    g1 = apply_styles(g1, styles)
    filename = g1.render(filename=output_filename)
    print("Graph saved in", filename)

if __name__ == '__main__':
	draw_topology(output_filename='img/topology')
