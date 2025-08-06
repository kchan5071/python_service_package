import socket
import socket_manager
import config_parser
import os
import time

def run_client(socket_name: str):
    sock = create_client_socket(socket_name)
    try:
        time.sleep(1)  # Wait for the server to be ready
        message = 'color: [255, 0, 0] title: ' \
        '"Welcome to the Dashboard"' \
        'subtitle: "Here is a quick overview of your metrics"'
        # Send data
        sock.sendall(bytes(message, 'utf-8'))
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            print('Received:', data.decode())
    finally:
        sock.close()

def create_client_socket(socket_name: str) -> socket.socket:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Get the socket directory from the config
    config = config_parser.read_config('config.yaml')
    socket_directory = config['socket_directory']
    
    # Ensure the socket directory exists
    if not os.path.exists(socket_directory):
        os.makedirs(socket_directory)

    print(socket_manager.list_open_sockets(socket_directory))
    server_address = os.path.join(socket_manager.list_open_sockets(socket_directory)[0])
    # Connect the socket to the server
    print('connecting to %s' % server_address)
    sock.connect(server_address)
    return sock

if __name__ == '__main__':
    run_client("echo_service_test.sock")