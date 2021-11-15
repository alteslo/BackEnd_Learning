import socket
from select import select

# David Beazley
# 2015 PyCon
# Concurrency from the Ground up Live

HOST = '127.0.0.1'
PORT = 5151

tasks = []

to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    while True:

        yield ('read', server_socket)
        client_socket, addres = server_socket.accept()  # read

        print('Connection from:', addres)
        tasks.append(client(client_socket))


def client(client_socket):

    while True:

        yield ('read', client_socket)
        request = client_socket.recv(1024)  # read

        if request:
            response = 'Hello dude\n'.encode()

            yield ('write', client_socket)
            client_socket.send(response)  # write
        else:
            break
    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            print(f'-----------------------\ntask в event_loop: {next(task)}')
            print(f'-----------------------\ntasks в event_loop после pop: {next(tasks[0])}')

            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print('Done')


if __name__ == '__main__':
    tasks.append(server())

    print(f'-----------------------\ntasks перед event_loop: {next(tasks[0])}')

    try:
        event_loop()
    except ConnectionResetError:
        print('Соединение разорвано...')
