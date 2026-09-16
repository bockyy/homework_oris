import socket
import threading
import sys
from protocol import send_message, recv_message


def receive_messages(sock):
    try:
        while True:
            msg = recv_message(sock)
            if msg is None:
                print("\n[Сервер разорвал соединение]")
                break

            cmd, payload = msg

            if cmd == "TEXT":
                print(f"\n{payload.decode('utf-8')}")
            elif cmd == "LIST":
                print(f"\n[Онлайн]: {payload.decode('utf-8')}")
    except Exception as e:
        print(f"\n[Ошибка чтения]: {e}")
    finally:
        sock.close()
        sys.exit(0)


def run_client(host="127.0.0.1", port=8000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        print("Отказ в соединении. Сервер не запущен.")
        return

    nickname = input("Никнейм: ").strip()
    if not nickname:
        print("Никнейм не может быть пустым.")
        sock.close()
        return

    send_message(sock, "JOIN", nickname.encode('utf-8'))

    recv_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    recv_thread.start()

    try:
        while True:
            text = input()
            if not text:
                continue

            if text == "/list":
                send_message(sock, "LIST", b"")
            elif text == "/quit":
                send_message(sock, "QUIT", b"")
                break
            else:
                send_message(sock, "TEXT", text.encode('utf-8'))
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()


if __name__ == "__main__":
    run_client()