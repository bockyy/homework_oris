import socket
import threading
from protocol import send_message, recv_message

clients = {}
clients_lock = threading.Lock()

rooms = {}
rooms_lock = threading.Lock()


def broadcast(command: str, payload: bytes, room_name: str, exclude_sock=None):
    with rooms_lock:
        target_sockets = list(rooms.get(room_name, set()))

    for sock in target_sockets:
        if sock == exclude_sock:
            continue
        try:
            send_message(sock, command, payload)
        except (ConnectionError, BrokenPipeError, OSError):
            pass


def handle_client(sock, addr):
    msg = recv_message(sock)
    if not msg:
        sock.close()
        return

    command, payload = msg
    if command != "JOIN":
        sock.close()
        return

    try:
        decoded = payload.decode('utf-8').strip()
        nickname, room_name = decoded.split(':', 1)
        if not nickname or not room_name:
            raise ValueError
    except (ValueError, UnicodeDecodeError):
        send_message(sock, "ERRO", b"Invalid JOIN format. Use: nickname:room")
        sock.close()
        return

    with clients_lock:
        clients[sock] = {"nickname": nickname, "room": room_name}

    with rooms_lock:
        rooms.setdefault(room_name, set()).add(sock)

    print(f"[+] {nickname} ({addr}) вошел в комнату [{room_name}]")
    broadcast("TEXT", f"{nickname} присоединился к комнате".encode('utf-8'), room_name, exclude_sock=sock)

    try:
        while True:
            msg = recv_message(sock)
            if not msg:
                break

            cmd, data = msg

            if cmd == "TEXT":
                text = data.decode('utf-8', errors='replace')
                broadcast("TEXT", f"{nickname}: {text}".encode('utf-8'), room_name, exclude_sock=sock)

            elif cmd == "LIST":
                with rooms_lock, clients_lock:
                    room_members = [
                        clients[s]["nickname"]
                        for s in rooms.get(room_name, set())
                        if s in clients
                    ]
                users_str = ", ".join(room_members)
                send_message(sock, "LIST", users_str.encode('utf-8'))

            elif cmd == "QUIT":
                break
            elif cmd == "ROOM":
                new_room = data.decode('utf-8', errors='replace').strip()
                if not new_room:
                    continue

                old_room = room_name

                with rooms_lock:
                    if old_room in rooms:
                        rooms[old_room].discard(sock)
                        if not rooms[old_room]:
                            del rooms[old_room]

                    rooms.setdefault(new_room, set()).add(sock)

                with clients_lock:
                    clients[sock]["room"] = new_room

                if old_room != new_room:
                    broadcast("TEXT", f"{nickname} покинул комнату {old_room}".encode('utf-8'), old_room, exclude_sock=sock)
                    broadcast("TEXT", f"{nickname} присоединился к комнате {new_room}".encode('utf-8'), new_room, exclude_sock=sock)

                room_name = new_room
                print(f"[-] {nickname} перешел в комнату {room_name}")
                send_message(sock, "TEXT", f"Вы теперь в комнате {room_name}".encode('utf-8'))
            else:
                send_message(sock, "ERRO", f"Неизвестная команда: {cmd}".encode('utf-8'))

    finally:
        with clients_lock:
            clients.pop(sock, None)

        with rooms_lock:
            if room_name in rooms:
                rooms[room_name].discard(sock)
                if not rooms[room_name]:
                    del rooms[room_name]

        print(f"[-] {nickname} ({addr}) отключился.")
        broadcast("TEXT", f"{nickname} покинул чат".encode('utf-8'), room_name)
        sock.close()


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
        print("\nОстановка сервера...")
    finally:
        server_sock.close()
        with clients_lock:
            for sock in list(clients.keys()):
                sock.close()
            clients.clear()
        with rooms_lock:
            rooms.clear()


if __name__ == "__main__":
    run_server()
