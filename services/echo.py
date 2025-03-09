import socket
import os


def run_server(socket_name):
    while True:
        if not test_socket_connection(socket_name):
            print('Socket file exists.')
            # Clean up the socket file
            try:
                os.unlink('/tmp/python-services' + socket_name)
            except FileNotFoundError:
                pass
        sock = create_server_socket(socket_name)
        sock.listen(1)
        connection = accept_connection(sock)
        echo(connection)
        connection.close()
        sock.close()
        
def test_socket_connection(socket_name):
    try:
        os.unlink('/tmp/python-services' + socket_name)
    except:
        return True
    return False

def create_server_socket(socket_name):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_address = '/tmp/python-services' + socket_name
    # Bind the socket to the address
    sock.bind(server_address)
    return sock

def accept_connection(sock):
    # Wait for a connection
    connection, client_address = sock.accept()
    return connection

def echo(connection):
    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(1024)
        if data:
            connection.sendall(data)
        else:
            break

if __name__ == '__main__':
    run_server("echo_service_test.sock")