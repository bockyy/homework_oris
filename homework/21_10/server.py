import json
import socket
import struct
import threading

HOST = "127.0.0.1"
PORT = 50505


class NetCom:
    def __init__(self, sock):
        self.sock = sock

    @staticmethod
    def _recv_exact(sock, size):
        chunks = []
        received = 0
        while received < size:
            chunk = sock.recv(size - received)
            if not chunk:
                return None
            chunks.append(chunk)
            received += len(chunk)
        return b"".join(chunks)

    def recv(self):
        header = self._recv_exact(self.sock, 4)
        if header is None:
            return None
        payload_size = struct.unpack("!I", header)[0]
        payload = self._recv_exact(self.sock, payload_size)
        if payload is None:
            return None
        return json.loads(payload.decode("utf-8"))

    def send(self, message):
        payload = json.dumps(message, ensure_ascii=False).encode("utf-8")
        header = struct.pack("!I", len(payload))
        self.sock.sendall(header + payload)


clients = []
clients_lock = threading.Lock()


def broadcast(message):
    with clients_lock:
        for client in list(clients):
            try:
                client.send(message)
            except OSError:
                clients.remove(client)


def handle_client(sock, addr):
    net = NetCom(sock)
    with clients_lock:
        clients.append(net)
    print(f"Подключился клиент: {addr}")

    net.send({
        "type": "system",
        "text": "Подключение установлено",
    })

    try:
        while True:
            message = net.recv()
            if message is None:
                break
            broadcast(message)
    finally:
        with clients_lock:
            if net in clients:
                clients.remove(net)
        sock.close()
        print(f"Отключился клиент: {addr}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер чата запущен и слушает {HOST}:{PORT}")

    try:
        while True:
            sock, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(sock, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server.close()


if __name__ == "__main__":
    main()