import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "127.0.0.1"
port = 8888
s.connect((ip, port))

while True:
    cmd = input(">>")
    if not cmd.strip():
        continue

    s.sendall(cmd.encode("utf-8"))

    if cmd == "/quit":
        break

    response = s.recv(1024).decode("utf-8")
    print(response, end="")

s.close()