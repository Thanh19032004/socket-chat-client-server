import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = []
names = []


def broadcast(message, sender_client=None):
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except:
                remove_client(client)


def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()

        name = names[index]
        names.remove(name)

        broadcast(f"{name} đã thoát khỏi phòng chat.".encode("utf-8"))


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                remove_client(client)
                break

            decoded = message.decode("utf-8")

            if decoded.lower() == "/quit":
                remove_client(client)
                break

            index = clients.index(client)
            name = names[index]

            full_message = f"{name}: {decoded}"
            print(full_message)

            broadcast(full_message.encode("utf-8"), client)

        except:
            remove_client(client)
            break


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("SERVER ĐANG CHẠY...")
    print(f"Địa chỉ: {HOST}")
    print(f"Cổng: {PORT}")
    print("Đang chờ client kết nối...\n")

    while True:
        client, address = server.accept()
        print(f"Client mới kết nối: {address}")

        client.send("NAME".encode("utf-8"))
        name = client.recv(1024).decode("utf-8")

        names.append(name)
        clients.append(client)

        print(f"Tên client: {name}")
        broadcast(f"{name} đã tham gia phòng chat.".encode("utf-8"), client)

        client.send("Kết nối tới server thành công!".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


start_server()