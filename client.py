import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5000

running = True


def receive_message(client):
    global running

    while running:
        try:
            message = client.recv(1024).decode("utf-8")

            if message == "NHAP_TEN":
                client.send(name.encode("utf-8"))

            elif message == "KET_NOI_THANH_CONG":
                print("[CLIENT] Kết nối tới server thành công")

            elif message == "KEEPALIVE_ACK":
                print("[CLIENT] Server phản hồi KEEPALIVE_ACK → OK")

            elif message == "SERVER_DA_NHAN_TIN_NHAN":
                print("[CLIENT] Server đã nhận tin nhắn")

            else:
                print("[SERVER]:", message)

        except:
            print("[CLIENT] Mất kết nối tới server")
            running = False
            client.close()
            break


def send_keepalive(client):
    global running

    while running:
        try:
            time.sleep(5)
            client.send("KEEPALIVE".encode("utf-8"))
        except:
            running = False
            break


def send_message(client):
    global running

    while running:
        message = input()

        if message == "/quit":
            client.send(message.encode("utf-8"))
            running = False
            client.close()
            print("[CLIENT] Đã thoát chương trình")
            break

        client.send(message.encode("utf-8"))


name = input("Nhập tên của bạn: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive_message, args=(client,))
receive_thread.start()

keepalive_thread = threading.Thread(target=send_keepalive, args=(client,))
keepalive_thread.start()

send_thread = threading.Thread(target=send_message, args=(client,))
send_thread.start()