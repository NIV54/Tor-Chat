from Classes import *
from Network_functions import *
import select
import json
from random import randint

SERVER_PORT = 54
SERVER_IP = "0.0.0.0"
BUFFER_SIZE = 1024
open_client_socket = []
messages_to_send = []
nodes = []


def build_path(path_len):
    """this function builds a random path in which the data will go through"""
    path = []
    if path_len > len(nodes):
        return None
    else:
        for i in range(path_len):
            rnd = randint(0, len(nodes)-1)
            next_node = nodes[rnd]
            path.append(next_node)
            nodes.remove(next_node)
        return path


def main():
    # running server socket
    server_socket = create_server_socket((SERVER_IP, SERVER_PORT))
    if server_socket:
        print "Directory server is running"

    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_socket, open_client_socket, [])
        for cur_sock in rlist:
            if cur_sock is server_socket:
                (new_socket, address) = server_socket.accept()
                open_client_socket.append(new_socket)
                print "new client connected"

            else:
                data = cur_sock.recv(BUFFER_SIZE)
                if data == "{[quit]}":
                    open_client_socket.remove(cur_sock)
                    print "client has disconnected"
                else:
                    loaded_data = json.loads(data)

                    if loaded_data["Request type"] == "Server data":
                        node_address = (loaded_data["Server_IP"], loaded_data["Server_Port"])
                        nodes.append(node_address)
                    elif loaded_data["Request type"] == "Path":
                        path_len = loaded_data["Path length"]
                        path = build_path(path_len)
                        cur_sock.send(json.dumps(path))
if __name__ == '__main__':
    main()
