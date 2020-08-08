import socket
import threading

client_base = {}

# host
address = "SECRET"
port = 1235

host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host.bind((address, port))
host.listen(100)


# demon
def connected_clients():
    while True:
        client, addr = host.accept()
        user = client.recv(1024)
        print(user.decode("utf8"))
        client_base[user.decode("utf8")] = client


unsent_message = {}
def queue_unsent():
    while True:
        for uns in set(unsent_message):
            if uns != None and uns in client_base:
                for message in unsent_message[uns]:
                    client_base[uns].send(message)
                del unsent_message[uns]
        # дописать функцию, которая будет контролировать подключение "ждущего клиента" и отправлять ему сообщение


connect_thread = threading.Thread(target=connected_clients)
connect_thread.daemon = True
connect_thread.start()

unsent_thread = threading.Thread(target=queue_unsent)
unsent_thread.daemon = True
unsent_thread.start()

# logic
if __name__ == "__main__":
    while True:
        try:
            rec = client_base['FATHER'].recv(1024)
            print(rec)
            dest, sender, data, key = rec.split(b"//sep//")
            dest = dest.decode("utf8")
            print(dest)
            try:
                client_base[dest].send(rec)
            except KeyError:
                if dest in unsent_message:
                    unsent_message[dest].append(rec)
                else:
                    unsent_message[dest] = [rec]
        except KeyError:
            pass

