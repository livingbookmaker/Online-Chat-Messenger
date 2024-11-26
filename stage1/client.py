import socket
import time
import threading


def receive_messages(udp_socket):
    while True:
        data, address = udp_socket.recvfrom(4096)
        print(data.decode())

serverAddressPort = ("0.0.0.0", 9001)
bufferSize = 4096
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

threading.Thread(target=receive_messages, args = (sock,), daemon=True).start()

username = input("Enter your name: ")

while True:
    msgFromClient = input()
    if msgFromClient == "q":
        print("チャットを終了します。")
        break

    data = str(len(username)) + username + msgFromClient
    bytesTosend = data.encode()

    sock.sendto(bytesTosend, serverAddressPort)

sock.close()

