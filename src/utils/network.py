from contextlib import closing
import socket


def is_port_open(port: int, host: str = 'localhost'):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0