from socket import *
from threading import *
import sys

Connected = False

def ReceiveMessage():
    global CanReceive
    if Connected:
        incoming = Connection.recv(1024).decode()
        print(incoming)
        Connection.send(incoming.encode())

def SendMessage():
    global Connected
    if Connected:
        outgoing = input()
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')

        if outgoing == 'close':
            Connected = False
        else: 
            outgoing = "Server Broadcast: " + outgoing
            print(outgoing)
            Connection.send(outgoing.encode())


serverSocket = socket(AF_INET, SOCK_STREAM)
print('Socket Created')

Port = 12345

serverSocket.bind(('', Port))
print('Socket Bound to port 12345')


serverSocket.listen(5)
print('Socket is listening')

serverMessage = 'Server Broadcast: Thank you for connecting!'

Connection, addr = serverSocket.accept() 
print('Got Connection', addr)
Connected = True
Connection.send(serverMessage.encode())


while Connected:
    ReceiveThread = Thread(target=ReceiveMessage)
    ReceiveThread.start()
    SendThread = Thread(target = SendMessage)
    SendThread.start()

if not Connected:
    Connection.close()