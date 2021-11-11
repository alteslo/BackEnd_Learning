import socket

req = "Hello tcp!"

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect(('127.0.0.1', 5555))
        soc.send(req)
        rsp = soc.recv(1024)
        print(rsp)
except ConnectionError:
    print("Не получилось установить соединение")
