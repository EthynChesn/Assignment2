from socket import *
from threading import *
import sys

Connected = False

hostname = gethostname()
IPAddr = gethostbyname(hostname) 


def ReceiveMessage():
    if Connected:
        incoming = clientSocket.recv(1024).decode()
        print(incoming)

def SendMessage():
    global Connected
    if Connected:
        outgoing = input()
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        if outgoing == 'close': 
            Connected = False
        else:
            outgoing = IPAddr + ": " + outgoing
            clientSocket.send(outgoing.encode())

clientSocket = socket(AF_INET, SOCK_STREAM)

Port = 12345

clientSocket.connect(('10.200.4.67', Port))
Connected = True
print(clientSocket.recv(1024).decode())


while Connected:
    ReceiveThread = Thread(target=ReceiveMessage)
    ReceiveThread.start()  
    SendThread = Thread(target = SendMessage)
    SendThread.start()



if not Connected:
    clientSocket.close()
