#!/opt/homebrew/anaconda3/bin/python

import subprocess
import argparse
import os
import shutil

import config_parser

def get_service_pids(service_csv):
    service_pids = {}
    with open(service_csv, 'r') as file:
        for line in file:
            service, pid = line.strip().split(',')
            service_pids[service] = pid
    return service_pids

def stop_service(service, pid):
    try:
        process = subprocess.Popen(['kill', pid])
        process.wait()
        print(f'Stopped service {service} with pid {pid}.')
    except:
        print(f'Could not stop service {service}.')

def stop_services(service_csv):
    if os.path.exists(service_csv):
        service_csv = os.path.join(os.getcwd(), service_csv)
    else:
        service_csv = os.path.join(os.getcwd(), 'services.csv')
 
    service_pids = get_service_pids(service_csv)
    for service, pid in service_pids.items():
        stop_service(service, pid)
    print('All services stopped.')

def clear_sockets(socket_directory):
    try:
        shutil.rmtree(socket_directory)
    except FileNotFoundError:
        print('No sockets to clear.')
        return
    os.makedirs('/tmp/python-services')
    print('Sockets cleared.')

if __name__ == '__main__':
    config_parser = config_parser.read_config('config.yaml')
    if config_parser['clear_socket']:
        clear_sockets(config_parser['socket_directory'])
    if config_parser['stop_services']:
        stop_services(config_parser['services_csv'])
