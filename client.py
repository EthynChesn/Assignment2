from socket import *
from threading import *
import sys

PrivateMode = False

#Send function
def Send():
    global PrivateMode
    while True:
        if PrivateMode == True:
            Outgoing = input('Enter Private Message: ')
        else:
            Outgoing = input()
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        #Private mode command, ask for client ID of recipient and send to server
        if Outgoing == '/private':
            PrivateMode = True
            recipient = input('Enter user ID of intended recipient: ')
            clientSocket.send(recipient.encode())
        #End Private Mode command, send to server
        elif Outgoing == '/end':
            if PrivateMode == True:
                PrivateMode = False
                print('Ended Private Chat')
                clientSocket.send(Outgoing.encode())
            else:
                print('You are not in a Private Chat.')
                clientSocket.send(Outgoing.encode())
        #Send message to server. Print on client-side
        else:
            clientSocket.send(Outgoing.encode())
            if PrivateMode == True:
                print('[Private Message]  '  + IPAddr + ': ' + Outgoing)
            else:
                print(IPAddr + ': ' + Outgoing)

#Initiliaze User informatio, server IP, and Port
hostname = gethostname()
IPAddr = gethostbyname(hostname)
Server = '10.200.4.67'
Port = 12345

#Create socket
clientSocket = socket(AF_INET, SOCK_STREAM)

#Connect client to server
clientSocket.connect((Server, Port))

#Receive and print initial information
print(clientSocket.recv(1024).decode())
print(clientSocket.recv(1024).decode())

#Listen for and receive further information
while True:
    SendThread = Thread(target = Send)
    SendThread.start()
    Incoming = clientSocket.recv(1024).decode()
    sys.stdout.write('\x1b[2K')
    print(Incoming)