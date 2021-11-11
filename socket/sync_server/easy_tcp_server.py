import socket
from views import *


HOST = '127.0.0.1'
PORT = 5151
URLS = {
    '/': index,
    '/blog': blog
}


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url]()


def generate_headers(method, url):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
    if url not in URLS:
        return ('HTTP/1.1 404 Method not allowed\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)


def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return (method, url)


def run():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(10)

        while True:
            client_socket, addres = server.accept()
            data = client_socket.recv(1024)
            print(data.decode('utf-8'))
            print()
            print(addres)

            response = generate_response(data.decode('utf-8'))

            client_socket.sendall(response)
            client_socket.close()
    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    run()
