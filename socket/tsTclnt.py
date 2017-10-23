from socket import *

HOST = 'localhost'
PORT = 21568
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('> ')
    if not data:
        break
    data_bytes = bytes(data, 'utf-8')
    tcpCliSock.send(data_bytes)
    data = tcpCliSock.recv(BUFSIZ)
    print (data.decode('utf-8'))

tcpCliSock.close()
