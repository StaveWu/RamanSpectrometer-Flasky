import socket
from threading import Thread


class SocketTool(Thread):

    def __init__(self, port=None):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if port:
            print('binding in constructor...')
            self.socket.bind((socket.gethostname(), port))
            self.socket.listen(5)
        self.stop = False

    def init_app(self, app):
        port = app.config['SOCKET_PORT']
        print('binding...')
        self.socket.bind((socket.gethostname(), port))
        self.socket.listen(5)

    def run(self) -> None:
        # self.socket.bind((socket.gethostname(), self.port))
        # self.socket.listen(5)
        while not self.stop:
            sock, addr = self.socket.accept()
            print('address {} is connected.'.format(addr))
            # do nothing, to handle msg from client we can use http instead
            sock.close()

    def send(self, msg):
        self.socket.send(bytes(msg, encoding='utf-8'))

    def stop(self):
        self.stop = True
        self.socket.close()
