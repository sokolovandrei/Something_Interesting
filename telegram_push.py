#!/usr/bin/env python3.7

#import getpass
#import re
import sys
import requests
#from netmiko import ConnectHandler

#user = 'andrey_s'
#password = 'StanazololZx948d4'
#device_ip = '10.1.8.249'
api_token = '644688660:AAEmglihHrHQfM-opFGOkKHlh97CmGy_2V8'
#device_params = {
#        'device_type': 'cisco_xe',
#        'ip': device_ip,
#        'username': user,
#        'password': password,
#        }


def telegram_push(device_params=None):
    while 1 > 0:
    #with ConnectHandler(**device_params) as ssh:
        #result = ssh.send_command('show ip interface brief')
        requests.post('https://api.telegram.org/bot{}/sendMessage'.format(api_token), params=dict(
            chat_id='@new_test_group',
            text="text"
        ))

if __name__ == '__main__':
	telegram_push(device_params=None)

