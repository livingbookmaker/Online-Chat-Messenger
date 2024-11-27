import socket

#ソケットを用意する
server_address = "0.0.0.0"
server_port = 9001
buffersize = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_address, server_port))

print("サーバー起動")

#クライアントを管理するためのリストを作成する
clients = []

#クライアントから受信したデータを処理する
while (True):
    bytesAddressPair = sock.recvfrom(buffersize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    #クライアントからの初回通信時にクライアントリストにアドレスを追加する
    if address not in clients:
        clients.append(address)
    
    #受信したデータをデコードする
    data = message.decode()

    #データの頭の11文字が「addusername」の場合、ユーザーがチャットに参加したことを各クライアントに伝える
    if len(data) >= 11 and data[0:11] == "addusername":
        addUser = data[11:] + "がチャットに参加しました。"
        print(addUser)
        for client in clients:
            sock.sendto(addUser.encode(), client)

    #データの頭の8文字が「quitchat」の場合、そのユーザーのアドレスをクライアントリストから削除し、ユーザーが退出したことを各クライアントに伝える
    elif len(data) >= 8 and data[0:8] == "quitchat":
        removeUser = data[8:] + "が退出しました"
        print(removeUser)
        clients.remove(address)
        for client in clients:
            sock.sendto(removeUser.encode(), client)

    #上記以外の場合、データを「ユーザー名の文字数」「ユーザー名」「メッセージ」に分解し、チャットメッセージを作って各クライアントに伝える
    else:
        usernamelen = int(data[0])
        username = data[1:1+usernamelen]
        m = data[1+usernamelen:]

        clientMsg = username + ": " + m
        print(clientMsg)

        bytesToSend = str.encode(clientMsg)

        for client in clients:
            sock.sendto(bytesToSend, client)