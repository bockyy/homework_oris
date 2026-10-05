import socket
import threading

ip = '127.0.0.1'
port = 8888

tasks = []
tasks_lock = threading.Lock()

def get_tasks_list(tasks):
    lines = []
    if not tasks:
        return "Список задач пуст.\n"
    for i, task in enumerate(tasks, start=1):
        if task["done"]:
           lines.append(f"{i}. [x] {task['text']}")
        else:
           lines.append(f"{i}. [ ] {task['text']}")
    return "\n".join(lines) + "\n"

def mark_done(tasks, task_number):
    if task_number < 1 or task_number > len(tasks):
        return "Ошибка: задача с таким номером не найдена.\n"

    tasks[task_number - 1]['done'] = True
    return "Задача выполнена.\n"

def delete_tasks(tasks, task_number):
    if task_number < 1 or task_number > len(tasks):
        return "Ошибка: задача с таким номером не найдена.\n"

    tasks.pop(task_number - 1)
    return "Задача успешно удалена.\n"

def add_tasks(tasks, text):
    if text.split():
        tasks.append({'text': text.strip(), 'done': False})
        return "Задача добавлена.\n"
    else:
        return "Ошибка: текст задачи не может быть пустым.\n"

def handle_client(client_sock, addr):
    print(f"[+] Клиент {addr} подключился")
    while True:
        data = client_sock.recv(1024)
        if not data:
            break

        parts = data.decode('utf-8').split(maxsplit=1)
        if not parts:
            continue
        command = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        if command == "/quit":
            break
        elif command == "/list":
            with tasks_lock:
                response = get_tasks_list(tasks).encode('utf-8')
            client_sock.sendall(response)
        elif command == "/add":
            with tasks_lock:
                response = add_tasks(tasks, text).encode('utf-8')
            client_sock.sendall(response)
        elif command == "/done":
            try:
                num = int(text)
                with tasks_lock:
                    response = mark_done(tasks, num).encode('utf-8')
                client_sock.sendall(response)
            except ValueError:
                client_sock.sendall(f"Введите порядковый номер задачи числом\n".encode('utf-8'))
        elif command == "/delete":
            try:
                num = int(text)
                with tasks_lock:
                    response = delete_tasks(tasks, num).encode('utf-8')
                client_sock.sendall(response)
            except ValueError:
                client_sock.sendall(f"Введите порядковый номер задачи числом\n".encode('utf-8'))
        else:
            client_sock.sendall("Неизвестная команда.\n".encode('utf-8'))


    client_sock.close()
    print(f"[-] Клиент {addr} отключился")

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip, port))
server_sock.listen()
print("Сервер запущен и ждет подключений...")

while True:
    client_sock, addr = server_sock.accept()
    thread = threading.Thread(target=handle_client, args=(client_sock, addr))
    thread.start()