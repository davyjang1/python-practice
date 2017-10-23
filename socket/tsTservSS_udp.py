from socketserver import (UDPServer as UDP,
        BaseRequestHandler as SRH)
from time import ctime

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

class MyRequestHandler(SRH):
    def handle(self):
        print ('...msg from:', self.client_address)
        data = self.request[0].strip()
        socket = self.request[1]
        socket.sendto(bytes(ctime() + " : ", 'utf-8') + data, self.client_address)

udpServ = UDP(ADDR, MyRequestHandler)
print("waiting for mdg")
udpServ.serve_forever()
