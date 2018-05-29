from Classes import *
from Encapsulation_Funcstions import *
from Network_functions import *
import json
import tkinter
from threading import Thread
from random import randint

PORT = 54
IP = "127.0.0.1"

END_USER_PORT = 45
END_USER_IP = "127.0.0.1"  # for test reasons. can't send data to LOCAL HOST address ("0.0.0.0")

BUFFER_SIZE = 1024
PATH_LENGTH = 3

TEXT_SIZE = 15
USER_MSG_COLOR = "forest green"
QUIT_CHAT = "{[quit]}"
msg_count = 0

private_key = 0
public_key = 0
public_prime = 0
public_base = 0
keys = ["key"]  # TODO: insert diffie helman key exchange


def main():
    def send(event=None):
        """Handles sending of messages"""
        global msg_count
        msg_txt = msg.get()
        if msg_txt != "":

            if msg_txt == QUIT_CHAT:
                client_socket.close()
                root.quit()

            else:
                data = encapsulate_message(user_name + ": " + msg_txt, keys, path,
                                           (END_USER_IP, END_USER_PORT), PATH_LENGTH)
                send_data(tuple(path[0]), data)

                msg.set("")  # Clears input field

                msg_count += 1
                msg_list.insert(tkinter.END, msg_txt + "\n")    # printing message to window
                msg_list.itemconfig(msg_count - 1, {'fg': USER_MSG_COLOR})  # changing sent message color

    def receive():
        """handles receiving of messages"""
        global msg_count
        while True:
            try:
                data = client_socket.recv(BUFFER_SIZE)  # string of sender_user_name: msg_txt
                msg_count += 1
                msg_list.insert(tkinter.END, data + "\n")  # printing message to window
            except OSError:  # client has left the chat
                break

    def on_closing(event=None):
        """This function is to be called when the GUI window is closed"""
        msg.set(QUIT_CHAT)  # quit message to server (assumed that will not be send during actual chatting).
        send()
        tkinter.Tk().quit()
        receive_loop = False  # stopping the thread.

    def key_parametrs():
        global public_key
        global private_key
        global public_prime
        global public_base
        public_key = randint(2, 100)
        private_key = randint(2, 100)


    # Creating a socket.
    client_socket = connect_client((IP, PORT))
    # Getting the path from the directory server.
    client_socket.send(json.dumps({"Request type": "Path", "Path length": PATH_LENGTH}))
    path = json.loads(client_socket.recv(BUFFER_SIZE))
    path = change_path(path)
    client_socket.send("{[quit]}")  # ending the connection with the server


    # inputs

    user_name = raw_input("User Name: ")  # TODO: Change to insert user name by GUI
    # TODO: Add end_ip, end_port, and path_length input
    # path_length must be 3 or above so that'll be mid nodes that have no clear information


    # GUI

    root = tkinter.Tk()
    root.title("Encoded Chat")  # header
    messages_frame = tkinter.Frame(root)

    msg = tkinter.StringVar()  # Var for saving the msg

    # Gui message window (and chat history)
    scrollbar = tkinter.Scrollbar(messages_frame)  # initializing a Scroll Bar
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    # txt field
    entry_field = tkinter.Entry(root, textvariable=msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    # send button
    send_button = tkinter.Button(root, text="Send", command=send)
    send_button.pack()

    # opening a thread for receiving messages
    receive_thread = Thread(target=receive)
    receive_thread.setDaemon(True)  # making sure the thread will close on exit.
    receive_thread.start()

    # GUI (has to be written at the end of the main)
    root.protocol("WM_DELETE_WINDOW", on_closing)  # window close action
    tkinter.mainloop()  # Starts GUI execution

if __name__ == '__main__':
    main()
