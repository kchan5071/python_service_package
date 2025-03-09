#!/opt/homebrew/anaconda3/bin/python

import os
import subprocess
import argparse

import config_parser

def initialize_socket_directory(socket_directory):
    try:
        os.makedirs(socket_directory)
    except FileExistsError:
        pass
    return socket_directory

def get_process_name_list(user_directory=None):
    if user_directory is None:
        user_directory = os.path.join(os.getcwd(), 'services')
    
    process_name_list = []
    for file in os.listdir(user_directory):
        if file.endswith('.py'):
            process_name_list.append(file)

    return process_name_list

def start_service(service_name, service_directory, python_executable):
    for file in os.listdir(service_directory):
        if file.endswith('.py') and file.startswith(service_name):
            process = subprocess.Popen([python_executable, os.path.join(service_directory, service_name)], cwd=service_directory)
            pid = process.pid
            return (service_name, pid)
        
    return (None, None)

def start_services(user_directory, python_executable):
    if user_directory is None:
        print("No service directory provided, using default: cwd/services")
    user_directory = os.path.join(os.getcwd(), 'services')
    name_list = get_process_name_list(user_directory)
    service_list = []
    for name in name_list:
        service_list.append(start_service(name, user_directory, python_executable))
        print(f'Started service {name}.')
    return service_list

def write_to_csv(services, filename):
    if os.path.exists(filename):
        filename = os.path.join(os.getcwd(), filename)
    else:
        filename = os.path.join(os.getcwd(), 'services.csv')
    with open(filename, 'w') as file:
        for service in services:
            file.write(f'{service[0]},{service[1]}\n')

if __name__ == '__main__':
    config_parser = config_parser.read_config('config.yaml')
    initialize_socket_directory(config_parser['socket_directory'])
    service_list = start_services(config_parser['service_directory'], config_parser['python_executable'])
    write_to_csv(service_list, config_parser['services_csv'])
    print('Services started.')