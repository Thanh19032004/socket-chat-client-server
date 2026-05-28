import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if message == "NAME":
                client.send(name.encode("utf-8"))
            else:
                print(message)

        except:
            print("Mất kết nối tới server.")
            client.close()
            break


def send_messages(client):
    while True:
        message = input()

        if message.lower() == "/quit":
            client.send(message.encode("utf-8"))
            client.close()
            print("Bạn đã thoát phòng chat.")
            break

        client.send(message.encode("utf-8"))


name = input("Nhập tên của bạn: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

send_thread = threading.Thread(target=send_messages, args=(client,))
send_thread.start()