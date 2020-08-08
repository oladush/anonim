import socket

ID = "FATHER"

address = "SECRET"
port = 1233

# server stream connect
server_stream_addr = "SECRET"
server_stream_port = 1235

server_stream = socket.socket()
server_stream.connect((server_stream_addr, server_stream_port))
server_stream.send(ID.encode("utf8"))


while True:
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host.bind((address, port))
    host.listen(1)
    client, addr = host.accept()
    data = client.recv(1024)
    server_stream.send(data)
    print(data)
    host.close()
