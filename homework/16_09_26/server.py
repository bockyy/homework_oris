import threading
from protocol import recv_exact, send_message, recv_message
import socket

clients = {}
clients_lock = threading.Lock()

def handle_client(conn, addr):
    msg = recv_message(conn)
    if msg is None:
        conn.close()
        return

    command, payload = msg
    if command != "JOIN":
        conn.close()
        return

    nickname = payload.decode('utf-8')
    with clients_lock:
        clients[conn] = nickname

    print(f"[ПОДКЛЮЧЕНИЕ] Клиент {nickname} ({addr}) вошел в чат.")

    broadcast("TEXT", f"{nickname} присоединился к чату".encode('utf-8'), sender_conn=conn)

    try:
        while True:
            choice = recv_message(conn)
            if choice is None:
                break

            cmd, data = choice

            if cmd == "TEXT":
                text = data.decode('utf-8')
                broadcast("TEXT", f"{nickname}: {text}".encode('utf-8'), sender_conn=conn)
            elif cmd == "LIST":
                with clients_lock:
                    user_list = ", ".join(clients.values())
                send_message(conn, "LIST", user_list.encode('utf-8'))
            elif cmd == "QUIT":
                break
            else:
                send_message(conn, "ERROR", f"Неизвестная команда: {cmd}".encode('utf-8'))
    finally:
        with clients_lock:
            clients.pop(conn, None)

        print(f"[ОТКЛЮЧЕНИЕ] Клиент {nickname} ({addr}) отключился.")

        broadcast("TEXT", f"{nickname} покинул чат".encode('utf-8'))
        conn.close()



def broadcast(command, payload, sender_conn=None):
    with clients_lock:
        recipients = [conn for conn in clients if conn != sender_conn]

    for conn in recipients:
        try:
            send_message(conn, command, payload)
        except (ConnectionResetError, BrokenPipeError):
            pass

def run_server(host: str = "0.0.0.0", port: int = 8000):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_sock.bind((host, port))
        server_sock.listen()
        print(f"Сервер запущен на {host}:{port}")

        while True:
            conn, addr = server_sock.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True,
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("\nСервер останавливается...")
    finally:
        server_sock.close()
        with clients_lock:
            for sock in list(clients.keys()):
                sock.close()
            clients.clear()


if __name__ == "__main__":
    run_server()