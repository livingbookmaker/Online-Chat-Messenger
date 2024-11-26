import socket

server_address = "0.0.0.0"
server_port = 9001
buffersize = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((server_address, server_port))

print("UDP server up and listening")

clients = set()

while (True):
    bytesAddressPair = sock.recvfrom(buffersize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    if address not in clients:
        clients.add(address)

    data = message.decode()
    usernamelen = int(data[0])
    username = data[1:1+usernamelen]
    m = data[1+usernamelen:]

    clientMsg = username + ": " + m
    print(clientMsg)

    bytesToSend = str.encode(clientMsg)

    for client in clients:
        sock.sendto(bytesToSend, client)

    