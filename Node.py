from Classes import *
from Encapsulation_Funcstions import *
from Network_functions import *
import select
import json


SERVER_PORT = 11110  # change between each run to create multiple different nodes.
SERVER_IP = "0.0.0.0"
CLIENT_PORT = 54
CLIENT_IP = "127.0.0.1"

BUFFER_SIZE = 1024

open_client_socket = []
messages_to_send = []

KEY = "key"


def main():
    # running server socket.
    server_socket = create_server_socket((SERVER_IP, SERVER_PORT))
    if server_socket:
        print "Node is running"

    # sending server information to the directory server.
    send_server_details((CLIENT_IP, CLIENT_PORT), (SERVER_IP, SERVER_PORT))
    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_socket, open_client_socket, [])
        for cur_sock in rlist:
            if cur_sock is server_socket:
                (new_socket, address) = server_socket.accept()
                open_client_socket.append(new_socket)
                print "new client connected"

            else:
                data = cur_sock.recv(BUFFER_SIZE)
                if data:
                    # data = decapsulate(KEY, encoded_data)
                    data = AESCipher(KEY).decrypt(data)
                    data = json.loads(data)

                    if "next_layer" in data:  # testing input

                        if not data["next_layer"]:
                            next_address = data["next_address"]
                            content = data["content"]
                            send_data(tuple(next_address), content)
                        else:
                            next_address = data["next_address"]
                            next_layer = data["next_layer"]
                            send_data(tuple(next_address), next_layer)
                    print "data sent"

                # for client in wlist:
                #     if client != cur_sock:
                #         client.send(data["user_name"] + ": " + data["txt"])

if __name__ == '__main__':
    main()
