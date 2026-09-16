import socket
import struct

MAX_MESSAGE_SIZE = 10 * 1024 * 1024

def recv_exact(sock, size):
    buffer = bytearray()
    while len(buffer) < size:
        chunk = sock.recv(size - len(buffer))
        if not chunk:
            raise ConnectionError("Соединение разорвано до получения всех данных")
        buffer.extend(chunk)
    return buffer

def send_message(sock, command, payload):
    message_bytes = command.encode('utf-8')
    if len(message_bytes) != 4:
        raise ValueError("Команда должна содержать ровно 4 байта")
    else:
        pack = struct.pack('!I', len(payload)) + payload
        sock.sendall(message_bytes + pack)

def recv_message(sock):
    try:
        header = recv_exact(sock, 8)
    except ConnectionError:
        return None

    command = header[:4].decode('utf-8')
    payload_len = struct.unpack('!I', header[4:])[0]

    if payload_len > MAX_MESSAGE_SIZE:
        raise ValueError(f"Размер сообщения {payload_len} превышает лимит {MAX_MESSAGE_SIZE}")
    try:
        payload = recv_exact(sock, payload_len)
    except ConnectionError:
        raise ConnectionError("Соединение оборвалось во время чтения тела сообщения")

    return command, payload