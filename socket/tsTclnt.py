from socket import *

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('> ')
    if not data:
        break
    data_bytes = bytes(data + '\n', 'utf-8')
    tcpCliSock.sendall(data_bytes)
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print (data.decode('utf-8'))

tcpCliSock.close()
