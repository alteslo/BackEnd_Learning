import socket


HOST = '127.0.0.1'
PORT = 5151
URLS = {
    '/': 'index',
    '/blog': 'blog'
}


def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        print('Before .accept()')
        client_socket, addres = server.accept()
        print('Connection from', addres)
        while True:
            print('Before .recv()')
            request = client_socket.recv(1024)
            if not request:
                break
            else:
                response = 'Hello dude\n'.encode()
                client_socket.send(response)

        print('Outside inner while loop')
        client_socket.close()


if __name__ == '__main__':
    run()
