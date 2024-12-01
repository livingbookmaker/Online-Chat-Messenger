import socket
import threading
import secrets

#UDPソケットを用意する
server_address = "0.0.0.0"
server_port = 9001
buffersize = 4096

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((server_address, server_port))

#TCPソケットを用意する
tcp_serverAddressPort = ("0.0.0.0", 9002)
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tcp_sock.close
except:
    pass
tcp_sock.bind(tcp_serverAddressPort)
tcp_sock.listen()

print("サーバー起動")

#チャットルームとクライアントを管理するためのリストを作成する
chatrooms = {}
tokens = {}

#トークンを生成する関数
def token_generator():
    token = secrets.token_hex(16)
    if token not in tokens and "," not in token:
        return token
    else:
        return token_generator()

#クライアントからの初回通信時にチャットルームを確認し、トークンを生成して渡す関数
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

            else:
                msg = username + "が" + chatroomName + "に参加しました。"
                print(msg)

            token = token_generator()
            print("トークンを生成しました。")
            tokens[token] = [chatroomName, username]
            connection.sendall(token.encode("utf-8"))

        except Exception as e:
            print("エラー: " + str(e))
        finally:
            connection.close()

#スレッドでクライアントからの初回通信を待つ
threading.Thread(target=first_contact, args = (tcp_sock,), daemon=True).start()

#クライアントから受信したデータを処理する
while (True):
    bytesAddressPair = udp_sock.recvfrom(buffersize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    #受信したデータをデコードする
    data = message.decode()

    #受信したデータを「コマンド」「トークン」「メッセージ」に分解する
    command, token, message = data.split(",", 2)
    if token not in tokens:
        msg = "そのトークンは使用できません。"
        print("存在しないトークンからの通信がありました。")
        udp_sock.sendto(msg.encode("utf-8"), address)
        continue
    
    #トークンが存在する場合は、トークンを「チャットルーム名」と「ユーザーネームに分解する」
    chatroomName = tokens[token][0]
    username = tokens[token][1]

    #コマンドが「join」の場合は、チャットルームにクライアントのアドレスを追加する
    if command == "join":
        if address not in chatrooms[chatroomName]:
            chatrooms[chatroomName].append(address)
            msg = f"{username}がチャットに参加しました。"
            for client in chatrooms[chatroomName]:
                if client != address:
                    udp_sock.sendto(msg.encode("utf-8"), client)
    
    #存在しないチャットルームへの通信があった場合（ホスト退出後の非ホストからの通信などの場合）は、チャットルームが存在しないことをクライアントに伝える
    elif chatroomName not in chatrooms:
        msg = f"チャットルーム「{chatroomName}」は存在しません。「q」を入力してチャットを終了してください。"
        print("存在しないチャットルームへの通信がありました。")
        udp_sock.sendto(msg.encode("utf-8"), address)
    
    #コマンドが「quitchat」の場合、チャットルームの解散またはチャットルームからの退出処理を行う
    elif command == "quitchat":
        if address == chatrooms[chatroomName][0]:
            msg = "ホストが退出したため、チャットルームを解散します。"
            print(f"チャットルーム{chatroomName}を解散しました。")
            for client in chatrooms[chatroomName]:
                if client != address:
                    udp_sock.sendto(msg.encode("utf-8"), client)
            chatrooms.pop(chatroomName)
            
        else:
            msg = f"{username}がチャットルーム「{chatroomName}」から退出しました。"
            print(msg)
            chatrooms[chatroomName].remove(address)
            for client in chatrooms[chatroomName]:
                udp_sock.sendto(msg.encode("utf-8"), client)

    #上記以外の場合、通常のメッセージ処理を行い、チャットルーム内の各クライアントにメッセージを送信する
    else:
        msg = username + ": " + message
        print(f"{chatroomName}: {msg}")
        bytesToSend = str.encode(msg)

        for client in chatrooms[chatroomName]:
            udp_sock.sendto(bytesToSend, client)
