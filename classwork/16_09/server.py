import socket

HOST = '0.0.0.0'
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Сервер слушает на {HOST}:{PORT}...")

    conn, addr = s.accept()
    print(f"Подключился клиент: {addr}")


    data = conn.recv(1024)
    if not data:
        print("Данные не были получены")
    else:
        print(f"Получено: {data}")

    s.close()