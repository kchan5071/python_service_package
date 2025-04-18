import socket

def run_client(socket_name: str):
    sock = create_client_socket(socket_name)
    try:
        message = 'This is the message. It will be echoed.'
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
    server_address = '/tmp/python-services/' + socket_name
    # Connect the socket to the server
    print('connecting to %s' % server_address)
    sock.connect(server_address)
    return sock

if __name__ == '__main__':
    run_client("echo_service_test.sock")