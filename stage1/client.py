import socket
import time
import threading

#ソケットを用意する
serverAddressPort = ("0.0.0.0", 9001)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#サーバーからメッセージを受信するための関数
def receive_messages(udp_socket):
    while True:
        data, address = udp_socket.recvfrom(4096)
        print(data.decode())

#適切なユーザーネームが入力されるまで再起する関数
def input_username():
    usernameInput = input("ユーザーネームを入力してください（最大9文字）：")
    if len(usernameInput) <= 9:
        addUsername = "addusername" + usernameInput
        sock.sendto(addUsername.encode(), serverAddressPort)
        return usernameInput
    
    else:
        print("ユーザーネームは9文字以内にしてください。")
        input_username()

#ユーザーネームを入力し、サーバーに伝える
username = input_username()

#サーバーからメッセージを受信する
threading.Thread(target=receive_messages, args = (sock,), daemon=True).start()

#チャットメッセージを入力し、サーバーに送信する（「q」が入力された場合、チャットを終了する）
while True:
    msgFromClient = input()
    if msgFromClient == "q":
        print("チャットを終了します。")
        quitChat = "quitchat" + username
        sock.sendto(quitChat.encode(), serverAddressPort)
        break

    data = str(len(username)) + username + msgFromClient
    bytesTosend = data.encode()

    sock.sendto(bytesTosend, serverAddressPort)

#breakでwhile文から抜けたら、ソケットを閉じてプログラムを終了する
sock.close()

