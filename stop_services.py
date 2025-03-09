#!/opt/homebrew/anaconda3/bin/python

import subprocess
import argparse
import os
import shutil

def get_service_pids():
    service_pids = {}
    with open('services.csv', 'r') as file:
        for line in file:
            service, pid = line.strip().split(',')
            service_pids[service] = pid
    return service_pids

def stop_service(service, pid):
    try:
        process = subprocess.Popen(['kill', pid])
        process.wait()
        print(f'Stopped service {service}.')
    except:
        print(f'Could not stop service {service}.')

def stop_services():
    service_pids = get_service_pids()
    for service, pid in service_pids.items():
        stop_service(service, pid)
    print('All services stopped.')

def clear_sockets():
    try:
        shutil.rmtree('/tmp/python-services')
    except FileNotFoundError:
        print('No sockets to clear.')
        return
    os.makedirs('/tmp/python-services')
    print('Sockets cleared.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stop services.')
    parser.add_argument('-c', '--clear_sockets', help='Clear the sockets.', default=True)
    args = parser.parse_args()
    if args.clear_sockets:
        clear_sockets()
    stop_services()
