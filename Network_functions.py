import socket
import json
from time import sleep

def connect_client(address):
    """Creates a client socket and connects it to the server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(address)
    return client_socket


def create_server_socket(address):
    """Creating and binding a socket.
    :return server socket from type TCP Socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(address)
    server_socket.listen(1)
    return server_socket


def send_server_details(connection_address, server_address):
    client_socket = connect_client(connection_address)
    node_server_data = json.dumps({"Request type": "Server data", "Server_IP": server_address[0],
                                   "Server_Port": server_address[1]})
    client_socket.send(node_server_data)
    sleep(0.1)
    client_socket.send("{[quit]}")
    client_socket.close()


def send_data(server_address, data):
    """Gets a server address and data to be sent. Creates a socket connection and sends the data."""
    client_socket = connect_client(server_address)
    client_socket.send(data)
    client_socket.close()  # closing the connection.


def change_path(path):
    """This function handles changing of address from LOCAL HOST to correct address for client to connect with.
    The function is used in testing only! On a real system that contains more than 1 PC this function is redundant."""
    new_path = []
    for i in range(len(path)):
        if path[i][0] == "0.0.0.0":
            new_path.append(["127.0.0.1", path[i][1]])
        else:
            new_path.append([path[i][0], path[i][1]])
    return new_path
