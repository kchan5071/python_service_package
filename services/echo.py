import socket
import os


import sys
sys.path.append("..")


import socket_manager

class EchoServer:
    def __init__(self):
        self.socket_address = socket_manager.get_available_socket_name("echo_service_test.sock")
        self.sock = None


    def run_server(self):
        while True:
            # Check if the socket file exists
            if not self.test_socket_connection():
                print('Socket file exists.')
                try:
                    os.unlink(self.socket_address)
                except FileNotFoundError:
                    pass

            # Create a socket
            self.create_server_socket()
            self.sock.listen(1)

            # Wait for a connection
            self.accept_connection()

            # perform the echo operation
            self.echo()

            # Clean up the connection
            self.connection.close()
            self.sock.close()
            
    def test_socket_connection(self):
        try:
            os.unlink(self.socket_address)
        except Exception:
            return True
        return False

    def create_server_socket(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Bind the socket to the address
        self.sock.bind(self.socket_address)

    def accept_connection(self):
        # Wait for a connection
        self.connection, _ = self.sock.accept()

    def echo(self):
        # Receive the data in small chunks and retransmit it
        while True:
            data = self.connection.recv(1024)
            if data:
                self.connection.sendall(data)
            else:
                break

if __name__ == '__main__':
    echo_server = EchoServer()
    echo_server.run_server()
