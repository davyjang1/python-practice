from socket import *

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

while True:
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    data = input('> ')
    if not data:
        break
    data_bytes = bytes(data + '\r\n', 'utf-8')
    tcpCliSock.send(data_bytes)
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print (data.decode('utf-8'))
    tcpCliSock.close()
