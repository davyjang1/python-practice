from socket import *

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

while True:
    udpCliSock = socket(AF_INET, SOCK_DGRAM)
    #udpCliSock.connect(ADDR)
    data = input('> ')
    if not data:
        break
    data_bytes = bytes(data + '\r\n', 'utf-8')
    udpCliSock.sendto(data_bytes, ADDR)
    data, ADDR = udpCliSock.recvfrom(BUFSIZ)
    if not data:
        break
    print (data.decode('utf-8'))
    #udpCliSock.close()
