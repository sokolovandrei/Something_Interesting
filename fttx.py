#!/usr/bin/env python
'''
Скрипт возвращает соответствие ipv4 адреса клиента и MSISDN.
Запускать можно с VM 172.24.223.123 (python/python),
предварительно зайдя в виртуальное окружение pyneng (workon pyneng)
'''
import ipaddress
from tabulate import tabulate
import getpass
import re
import sys
import requests
from netmiko import ConnectHandler, NetMikoAuthenticationException
from pprint import pprint

user = input('Input username: ')
password = getpass.getpass('Input password: ')
ip_addr = input('Input subscriber ip address: ')

try:
    if ipaddress.ip_address(ip_addr):
        pass
except ValueError as error:
    print(error)
    sys.exit('ip address is incorrect!')

device_params = [{
    'device_type': 'cisco_xr',
    'ip': '172.24.250.1',
    'username': user,
    'password': password,
}, {
    'device_type': 'cisco_xr',
    'ip': '172.29.252.1',
    'username': user,
    'password': password,
}, {
    'device_type': 'cisco_xr',
    'ip': '172.28.252.1',
    'username': user,
    'password': password,
}, {
    'device_type': 'cisco_xr',
    'ip': '172.27.252.1',
    'username': user,
    'password': password,
}, {
    'device_type': 'cisco_xr',
    'ip': '172.26.252.1',
    'username': user,
    'password': password,
}, {
    'device_type': 'cisco_xr',
    'ip': '172.25.252.1',
    'username': user,
    'password': password,
}, {
    'device_type': 'cisco_xr',
    'ip': '172.24.250.6',
    'username': user,
    'password': password,
},]

def check_fttx_subscribers(device_params):
    for device in device_params:
        try:
            with ConnectHandler(**device) as ssh:
                info = ssh.send_command('show subscriber session filter ipv4-address {} detail | in Label'.format(ip_addr))
                if 'Subscriber Label' not in info:
                    continue
                else:
                    label = re.findall(r'Subscriber Label: +0x(\S+)', info)
                    for label_line in label:
                        Label = label_line
                    msisdn_info = ssh.send_command('show subscriber manager sadb subscriber-label {} | i class'.format(Label))
                    if 'class' and 'len= 12'  in msisdn_info:
                        msisdn_hex = re.findall(r'len= 12  +((?:\S+ ){11}\S+)', msisdn_info)
                        for msisdn_line in msisdn_hex:
                            MSISDN_HEX = msisdn_line
                            MSISDN = bytearray.fromhex(MSISDN_HEX).decode()
                    else:
                        sys.exit('There is no info for that ip address')
            return MSISDN
        except NetMikoAuthenticationException as error:
             print(error)
             print('Credentials are incorrect!')
             break


if __name__ == '__main__':
    if check_fttx_subscribers(device_params):
        out = [ip_addr+' '+check_fttx_subscribers(device_params)]
        final = []
        for line in out:
            line_new = line.split()
            final.append(line_new)
        print(tabulate(final, headers=['SUBSCRIBER IP','SUBSCRIBER MSISDN'], tablefmt="github"))
    else:
        try:
            if not check_fttx_subscribers(device_params):
                print('ip address {}  does not exist or session is inactive'.format(ip_addr))
        except EOFError:
            print('Try again')

