import socket
import tkinter
import threading
import sys

#UDPソケットを用意する
udp_serverAddressPort = ("0.0.0.0", 9001)
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#TCPソケットを用意する
tcp_serverAddressPort = ("0.0.0.0", 9002)
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#サーバーからメッセージを受信するための関数
def receive_messages(udp_socket):
    while True:
        data, address = udp_socket.recvfrom(4096)
        print(data.decode())
        if data.decode() == "ホストが退出したため、チャットルームを解散します。":
            print("「q」を入力してチャットを終了してください。")

#一定時間入力がなかった場合にチャットを自動で終了するための関数
def quitChat(udp_socket):
    print("チャットを終了します。")
    command = "quitchat"
    msg = f"{command},{token},dummy"
    udp_socket.sendto(msg.encode("utf-8"), udp_serverAddressPort)
    udp_socket.close()
    sys.exit()
autoQuit = tkinter.Tk()

#サーバーに送信されるヘッダ情報をフォーマットするための関数
def protocol_header(chatroomName_length, username_length):
    return  chatroomName_length.to_bytes(1, "big") + username_length.to_bytes(1, "big")

#TCP接続でサーバーと接続し、チャットルーム名とユーザーネームを伝える
try:
    tcp_sock.connect(tcp_serverAddressPort)
except tcp_sock.error as err:
    print(err)
    sys.exit(1)

#TCP接続でサーバーにチャットルーム名とユーザーネームを送ってトークンをもらい、そのトークンを使ってUDP接続を行ってチャットルームに参加する
try:
    chatroomName = input("チャットルーム名を入力してください: ")
    username = input("ユーザーネームを入力してください: ")

    chatroomName_bits = chatroomName.encode("utf-8")
    username_bits = username.encode("utf-8")
    
    header = protocol_header(len(chatroomName_bits), len(username_bits))
    body = chatroomName + username
    tcp_sock.send(header)
    tcp_sock.send(body.encode("utf-8"))

    token = tcp_sock.recv(4096)
    token = token.decode()

    joinMsg = f"join,{token},dummy"
    udp_sock.sendto(joinMsg.encode("utf-8"), udp_serverAddressPort)
    
finally:
    print("チャットを開始します。")
    tcp_sock.close()
    

#サーバーからメッセージを受信する
threading.Thread(target=receive_messages, args = (udp_sock,), daemon=True).start()

#チャットメッセージを入力し、サーバーに送信する（「q」が入力された場合、チャットを終了する）
while True:
    #tkinterのafterメソッドを使って一定時間で自動終了の関数を実行する
    afterID = autoQuit.after(60000, quitChat, udp_sock)

    msgFromClient = input()

    #メッセージが入力されたらafterメソッドによる自動終了関数の実行予約をキャンセルする
    autoQuit.after_cancel(afterID)

    if msgFromClient == "q":
        quitChat(udp_sock)

    else:
        command = "usualchat"
        data = f"{command},{token},{msgFromClient}"
        bytesTosend = data.encode()
        udp_sock.sendto(bytesTosend, udp_serverAddressPort)