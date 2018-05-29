from Classes import *
from Network_functions import *
import select
import json
import tkinter
from threading import Thread

SERVER_PORT = 45
SERVER_IP = "0.0.0.0"
BUFFER_SIZE = 1024
TEXT_SIZE = 15
USER_MSG_COLOR = "forest green"
QUIT_CHAT = "{[quit]}"

msg_count = 0


def main():
    def send(event=None):
        pass

    #     global msg_count
    #     """Handles sending of messages"""
    #     msg_txt = msg.get()
    #     if msg_txt != "":
    #         data = json.dumps({"user_name": user_name, "txt": msg_txt})
    #         client_socket.send(data)  # sending the msg to the server
    #
    #         msg.set("")  # Clears input field
    #
    #         msg_count += 1
    #         msg_list.insert(tkinter.END, msg_txt + "\n")    # printing message to window
    #         msg_list.itemconfig(msg_count - 1, {'fg': USER_MSG_COLOR})  # changing sent message color
    #
    #         if msg_txt == QUIT_CHAT:
    #             client_socket.close()
    #             root.quit()
    #

    def receive():
        open_client_socket = []
        messages_to_send = []
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
                        msg_list.insert(tkinter.END, data + "\n")  # printing message to window

    def on_closing(event=None):
        """This function is to be called when the GUI window is closed"""
        msg.set(QUIT_CHAT)  # quit message to server (assumed that will not be send during actual chatting)
        # send(msg_count)
        tkinter.Tk().quit()  # stopping the thread

    # creating a socket
    # client_socket = connect_client((IP, PORT))

    # opening a thread for receiving messages
    # receive_loop = True
    # receive_thread = Thread(target=receive)
    # receive_thread.start()

    user_name = raw_input("User Name: ")  # TODO: Change to insert user name by GUI

    # running server socket
    server_socket = create_server_socket((SERVER_IP, SERVER_PORT))

    # opening a thread for receiving messages
    receive_thread = Thread(target=receive)
    receive_thread.setDaemon(True)
    receive_thread.start()


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

    # GUI (has to be written at the end of the main)
    root.protocol("WM_DELETE_WINDOW", on_closing)  # window close action
    tkinter.mainloop()  # Starts GUI execution


if __name__ == '__main__':
    main()
