import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = {}


def handle_client(client_socket, address):
    print(f"[+] Client kết nối từ {address}")

    try:
        client_socket.send("NHAP_TEN".encode("utf-8"))
        name = client_socket.recv(1024).decode("utf-8")

        clients[client_socket] = name
        print(f"[SERVER] Client tên là: {name}")

        client_socket.send("KET_NOI_THANH_CONG".encode("utf-8"))

        while True:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:
                break

            if message == "KEEPALIVE":
                print(f"[KEEPALIVE] Nhận keepalive từ {name}")
                client_socket.send("KEEPALIVE_ACK".encode("utf-8"))

            elif message == "/quit":
                print(f"[-] {name} đã thoát")
                break

            else:
                print(f"[TIN NHẮN] {name}: {message}")
                client_socket.send("SERVER_DA_NHAN_TIN_NHAN".encode("utf-8"))

    except:
        print(f"[LỖI] Mất kết nối với client {address}")

    finally:
        if client_socket in clients:
            del clients[client_socket]

        client_socket.close()
        print(f"[-] Đã đóng kết nối với {address}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("SERVER ĐANG CHẠY...")
    print(f"Địa chỉ: {HOST}")
    print(f"Cổng: {PORT}")
    print("Đang chờ client kết nối...\n")

    while True:
        client_socket, address = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address)
        )
        thread.start()


start_server()