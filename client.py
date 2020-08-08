import aese

import os
import json
import socket
import threading

sep = b"//sep//"

server_stream_addr = ("SECRET", 1235)
server_handler_addr = ("SECRET", 1233)


ID = ""
private_key = b""

contacts = {}
none_elegant = {}


def import_parameters(): 
    global ID, private_key
    with open("profile\\private.json", "r") as read_json:
        par = json.load(read_json)
        ID = par['id']
        private_key = par['private key'].encode('utf8')

    global contacts
    list_contacts = os.listdir('contacts')
    for contact in list_contacts:
        with open("contacts\\" + contact, 'r') as read_contact:
            cont = json.load(read_contact)
            contacts[cont['username']] = [cont['id'], cont['public key']]
            none_elegant[cont['id']] = cont['username'] 


# thread
def receive_messages():
    while True:
        inp = server_stream.recv(1024)
        dest, sender, data, key = inp.split(sep)
        mes = aese.decode_run(data, key, private_key)
        print(none_elegant[sender.decode("utf8")] + ": " + mes.decode("utf8"))

def chat():
    while True:
        dest = input("dest: ")
        data = input().encode('utf8')
        server_handler = socket.socket()
        server_handler.connect(server_handler_addr)
        send_file = aese.encode_run(data, contacts[dest][1])
        server_handler.send(contacts[dest][0].encode('utf8') + sep + ID.encode('utf8') + sep + send_file[0] + sep + send_file[1])
        server_handler.close()

if __name__ == "__main__":
    import_parameters()
    # connect server_stream
    server_stream = socket.socket()
    server_stream.connect(server_stream_addr)
    server_stream.send(ID.encode("utf8"))
    # get_message_thread
    receive_messages_thread = threading.Thread(target=receive_messages)
    receive_messages_thread.daemon = True
    receive_messages_thread.start()
    chat()

