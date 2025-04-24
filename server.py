from socket import *
from threading import *
import sys

def NewClient(clientSocket, addr):
    while True:
        SendThread = Thread(target=Send, args=(clientSocket,addr))
        SendThread.start()
        Incoming = clientSocket.recv(1024).decode()
        if Incoming == 'close':
            break
        print(str(addr[0]) + ': ' + Incoming)
    clientSocket.close()

def Send(client, ClientAddr):
    Outgoing = input()
    client.send(Outgoing.encode())
    

def main():
    Host = '0.0.0.0'
    Port = 12345

    serverSocket =  socket(AF_INET, SOCK_STREAM)

    serverSocket.bind((Host, Port))

    serverSocket.listen(5)

    print('Server Open. Waiting for Clients to Connect...')
    serverMessage = 'Server Broadcast: Thank you for connecting!'

    while True:
        Connection, addr = serverSocket.accept()
        ClientThread = Thread(target=NewClient, args=(Connection,addr))
        ClientThread.start()
        print('Got Connection', addr)
        Connection.send(serverMessage.encode())

    Connection.close()
    ClientThread.join()

if __name__ == '__main__':
    main()