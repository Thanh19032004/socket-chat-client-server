import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

running = True


def receive_message(client):
    global running

    while running:
        try:
            message = client.recv(1024).decode("utf-8")

            if not message:
                print("[CLIENT] Server đã đóng kết nối")
                running = False
                client.close()
                break

            if message == "NHAP_TEN":
                client.send(name.encode("utf-8"))

            elif message == "KET_NOI_THANH_CONG":
                print("[CLIENT] Kết nối tới server thành công")

            elif message == "KEEPALIVE":
                print("[CLIENT] Nhận KEEPALIVE từ server → gửi KEEPALIVE_ACK")
                client.send("KEEPALIVE_ACK".encode("utf-8"))

            elif message == "SERVER_DA_NHAN_TIN_NHAN":
                print("[CLIENT] Server đã nhận tin nhắn")

            else:
                print("[SERVER]:", message)

        except:
            if running:
                print("[CLIENT] Mất kết nối tới server")
            running = False
            try:
                client.close()
            except:
                pass
            break


def send_message(client):
    global running

    while running:
        try:
            message = input()

            if message == "/quit":
                client.send(message.encode("utf-8"))
                running = False
                client.close()
                print("[CLIENT] Đã thoát chương trình")
                break

            client.send(message.encode("utf-8"))

        except:
            running = False
            break


name = input("Nhập tên của bạn: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive_message, args=(client,))
receive_thread.start()

send_thread = threading.Thread(target=send_message, args=(client,))
send_thread.start()
