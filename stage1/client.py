import socket
import tkinter
import threading
import sys

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
        return input_username()

#ユーザーネームを入力し、サーバーに伝える
username = input_username()

#サーバーからメッセージを受信する
threading.Thread(target=receive_messages, args = (sock,), daemon=True).start()

#一定時間入力がなかった場合にチャットを自動で終了するための関数
def quitChat(udp_socket):
    print("チャットを終了します。")
    quitChat = "quitchat" + username
    udp_socket.sendto(quitChat.encode(), serverAddressPort)
    sock.close()
    sys.exit()
    
autoQuit = tkinter.Tk()

#チャットメッセージを入力し、サーバーに送信する（「q」が入力された場合、チャットを終了する）
while True:
    #tkinterのafterメソッドを使って一定時間で自動終了の関数を実行する
    afterID = autoQuit.after(60000, quitChat, sock)

    msgFromClient = input()

    #メッセージが入力されたらafterメソッドによる自動終了関数の実行予約をキャンセルする
    autoQuit.after_cancel(afterID)

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

