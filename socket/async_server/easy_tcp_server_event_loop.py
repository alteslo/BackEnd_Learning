import socket
from select import select


HOST = '127.0.0.1'
PORT = 5151
URLS = {
    '/': 'index',
    '/blog': 'blog'
}

to_monitor = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()


def accept_connection(server):
    client_socket, addres = server.accept()
    print('Connection from:', addres)
    to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(1024)

    if request:
        response = 'Hello dude\n'.encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])  # read, write, errors

        for sock in ready_to_read:
            if sock is server:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server)
    event_loop()
