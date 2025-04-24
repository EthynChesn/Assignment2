from socket import *
from threading import *
import sys

def Send():
    Outgoing = input()
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    clientSocket.send(Outgoing.encode())
    print(IPAddr + ': ' + Outgoing)

hostname = gethostname()
IPAddr = gethostbyname(hostname) 

clientSocket = socket(AF_INET, SOCK_STREAM)
Port = 12345

clientSocket.connect(('10.200.4.67', Port))

print(clientSocket.recv(1024).decode())

while True:
    SendThread = Thread(target = Send)
    SendThread.start()
    Incoming = clientSocket.recv(1024).decode()
    print(Incoming)
clientSocket.close()