import socket
import select

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
        client(client_socket)


def client(client_socket):

    while True:

        yield ('read', client_socket)
        request = client_socket.recv(1024)  # read

        if request:
            response = 'Hello dude\n'.encode()

            yield ('write', client_socket)
            client_socket.send(response)  # write
        else:
            client_socket.close()
            break


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_write, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))


if __name__ == '__main__':
    tasks.append(server())
    try:
        server()
    except ConnectionResetError:
        print('Соединение разорвано...')
