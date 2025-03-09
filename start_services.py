#!/usr/bin/python3

import os
import subprocess
import argparse

def get_service_directory():
    return os.path.join(os.path.dirname(__file__), 'services')

def get_python_executable():
    return '/opt/homebrew/anaconda3/bin/python'

def get_process_name_list(user_directory=None):
    if user_directory is None:
        user_directory = get_service_directory()
    
    process_name_list = []
    for file in os.listdir(user_directory):
        if file.endswith('.py'):
            process_name_list.append(file)

    return process_name_list

def start_service(service_name, service_directory):
    if service_directory is None:
        print("No service directory provided.")
        quit()

    for file in os.listdir(service_directory):
        if file.endswith('.py') and file.startswith(service_name):

            process = subprocess.Popen([get_python_executable(), os.path.join(service_directory, service_name)], cwd=service_directory)
            pid = process.pid
            return (service_name, pid)
        
    return (None, None)

def start_services(user_directory):
    if user_directory is None:
        print("No service directory provided.")
    directory = get_service_directory()
    name_list = get_process_name_list(directory)
    service_list = []
    for name in name_list:
        service_list.append(start_service(name, directory))
    return service_list

def write_to_csv(services, filename='services.csv'):
    with open(filename, 'w') as file:
        for service in services:
            file.write(f'{service[0]},{service[1]}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start services.' )
    parser.add_argument('-d','--service_directory', help='The directory containing the services.', default=None)
    args = parser.parse_args()
    print(args.service_directory)
    service_list = start_services(args.service_directory)
    write_to_csv(service_list)
    print('Services started.')