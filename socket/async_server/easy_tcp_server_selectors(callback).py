import socket
import selectors


HOST = '127.0.0.1'
PORT = 5151

selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    selector.register(
        fileobj=server_socket,
        events=selectors.EVENT_READ,
        data=accept_connection
        )


def accept_connection(server_socket):
    client_socket, addres = server_socket.accept()
    print('Connection from:', addres)

    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
        )


def send_message(client_socket):
    request = client_socket.recv(1024)

    if request:
        response = 'Hello dude\n'.encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        # Возвращает список кортежей (key, events)
        # на каждый зарегистрированный объект
        events = selector.select()

        # Selectorkey (obj named tuple)
        for key, _ in events:
            callback = key.data  # в дате хранится функция
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
