from socket import *
from threading import *
import sys

PrivateMode = False

def Send():
    global PrivateMode
    while True:
        if PrivateMode == True:
            Outgoing = input('Enter Private Message: ')
        else:
            Outgoing = input()
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        if Outgoing == '/private':
            PrivateMode = True
            recipient = input('Enter user ID of intended recipient: ')
            clientSocket.send(recipient.encode())
        elif Outgoing == '/end':
            if PrivateMode == True:
                PrivateMode = False
                print('Ended Private Chat')
                clientSocket.send(Outgoing.encode())
            else:
                print('You are not in a Private Chat.')
                clientSocket.send(Outgoing.encode())
        else:
            clientSocket.send(Outgoing.encode())
            if PrivateMode == True:
                print('[Private Message]'  + IPAddr + ': ' + Outgoing)
            else:
                print(IPAddr + ': ' + Outgoing)

hostname = gethostname()
IPAddr = gethostbyname(hostname)
Server = '10.200.4.67'

clientSocket = socket(AF_INET, SOCK_STREAM)
Port = 12345

clientSocket.connect((Server, Port))

print(clientSocket.recv(1024).decode())
print(clientSocket.recv(1024).decode())

while True:
    SendThread = Thread(target = Send)
    SendThread.start()
    Incoming = clientSocket.recv(1024).decode()
    sys.stdout.write('\x1b[2K')
    print(Incoming)