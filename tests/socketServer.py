import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345
s.bind((host, port))

s.listen(5)
while True:
    c, addr = s.accept()
    print('连接地址', addr)
    c.send(bytes('welcome!', encoding='utf-8'))
    c.close()

