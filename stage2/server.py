import socket
import threading

#UDPソケットを用意する
server_address = "0.0.0.0"
server_port = 9001
buffersize = 4096

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((server_address, server_port))

#TCPソケットを用意する
tcp_serverAddressPort = ("0.0.0.0", 9002)
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.close
tcp_sock.bind(tcp_serverAddressPort)
tcp_sock.listen()

print("サーバー起動")

#チャットルームとクライアントを管理するためのリストを作成する
chatrooms = {}
tokens = {}

#クライアントからの初回通信時にチャットルームやユーザーネームを確認する関数
def first_contact(tcp_socket):
    while True:
        connection, client_address = tcp_sock.accept()
        try:
            print("接続中: ", client_address)
            header = connection.recv(2)
            chatroomName_length = int.from_bytes(header[:1], "big")
            username_length = int.from_bytes(header[1:2], "big")

            chatroomName = connection.recv(chatroomName_length).decode("utf-8")
            username = connection.recv(username_length).decode("utf-8")

            if chatroomName not in chatrooms:
                chatrooms[chatroomName] = []
                msg = username + "が" + chatroomName + "を作成しました。"
                print(msg)
                print(chatrooms[chatroomName])

            else:
                msg = username + "が" + chatroomName + "に参加しました。"
                print(msg)

        except Exception as e:
            print("エラー: " + str(e))
        finally:
            connection.close()

threading.Thread(target=first_contact, args = (tcp_sock,), daemon=True).start()

#クライアントから受信したデータを処理する
while (True):
    bytesAddressPair = udp_sock.recvfrom(buffersize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    #受信したデータをデコードする
    data = message.decode()

    command, chatroomName, username, message = data.split(",", 3)

    if address not in chatrooms[chatroomName]:
        chatrooms[chatroomName].append(address)

    if command == "quitchat":
        if address == chatrooms[chatroomName][0]:
            msg = f"ホストが退出したため、チャットルームを解散します。"
            for client in chatrooms[chatroomName]:
                if client != address:
                    udp_sock.sendto(msg.encode("utf-8"), client)
            chatrooms.pop(chatroomName)
            
        else:
            msg = f"{username}が退出しました。"
            chatrooms[chatroomName].remove(address)
            for client in chatrooms[chatroomName]:
                udp_sock.sendto(msg.encode("utf-8"), client)

    else:
        msg = username + ": " + message
        print(msg)
        bytesToSend = str.encode(msg)

        for client in chatrooms[chatroomName]:
            udp_sock.sendto(bytesToSend, client)
