import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5000

HEARTBEAT_INTERVAL = 5
TIMEOUT_LIMIT = 15

clients = {}
clients_lock = threading.Lock()


def send_keepalive(client_socket, address):
    while True:
        time.sleep(HEARTBEAT_INTERVAL)

        with clients_lock:
            client_info = clients.get(client_socket)

        if client_info is None:
            break

        name = client_info["name"]
        last_seen = client_info["last_seen"]

        if time.time() - last_seen > TIMEOUT_LIMIT:
            print(f"[TIMEOUT] {name} không phản hồi quá {TIMEOUT_LIMIT} giây → offline")
            try:
                client_socket.close()
            except:
                pass
            break

        try:
            client_socket.send("KEEPALIVE".encode("utf-8"))
            print(f"[KEEPALIVE] Đã gửi KEEPALIVE tới {name}")
        except:
            print(f"[LỖI] Không gửi được KEEPALIVE tới {name}")
            try:
                client_socket.close()
            except:
                pass
            break


def handle_client(client_socket, address):
    print(f"[+] Client kết nối từ {address}")

    name = None

    try:
        client_socket.send("NHAP_TEN".encode("utf-8"))
        name = client_socket.recv(1024).decode("utf-8")

        with clients_lock:
            clients[client_socket] = {
                "name": name,
                "address": address,
                "last_seen": time.time()
            }

        print(f"[SERVER] Client tên là: {name}")
        client_socket.send("KET_NOI_THANH_CONG".encode("utf-8"))

        heartbeat_thread = threading.Thread(
            target=send_keepalive,
            args=(client_socket, address),
            daemon=True
        )
        heartbeat_thread.start()

        while True:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:
                break

            if message == "KEEPALIVE_ACK":
                with clients_lock:
                    if client_socket in clients:
                        clients[client_socket]["last_seen"] = time.time()
                print(f"[KEEPALIVE] Nhận KEEPALIVE_ACK từ {name}")

            elif message == "/quit":
                print(f"[-] {name} đã thoát")
                break

            else:
                print(f"[TIN NHẮN] {name}: {message}")
                client_socket.send("SERVER_DA_NHAN_TIN_NHAN".encode("utf-8"))

    except:
        print(f"[LỖI] Mất kết nối với client {address}")

    finally:
        with clients_lock:
            if client_socket in clients:
                del clients[client_socket]

        try:
            client_socket.close()
        except:
            pass

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
