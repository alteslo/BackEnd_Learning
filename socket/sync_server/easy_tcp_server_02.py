import socket


HOST = '127.0.0.1'
PORT = 5151
URLS = {
    '/': 'index',
    '/blog': 'blog'
}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()


def accept_connection(server):
    while True:
        client_socket, addres = server.accept()
        print('Connection from', addres)
        send_message(client_socket)


def send_message(client_socket):
    while True:
        print('Before .recv()')
        request = client_socket.recv(1024)
        if not request:
            break
        else:
            response = 'Hello dude\n'.encode()
            client_socket.send(response)

    client_socket.close()


if __name__ == '__main__':
    accept_connection(server)
