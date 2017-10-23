from socketserver import (TCPServer as TCP,
        StreamRequestHandler as SRH)
from time import ctime

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

class MyRequestHandler(SRH):
    def handle(self):
        print ('...connected from:', self.client_address)
        data = self.rfile.readline()
        self.wfile.write(bytes(ctime() + " : ", 'utf-8') + data)

tcpServ = TCP(ADDR, MyRequestHandler)
print("waiting for connection")
tcpServ.serve_forever()
