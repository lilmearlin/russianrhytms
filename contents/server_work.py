import socket


def request(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('176.57.215.122', 65433))
    sock.sendall(data)
    data = sock.recv(1024)
    return data
