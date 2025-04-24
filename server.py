from socket import *
from threading import *
import sys

clientlist = []
clientdict = {}
userlist = []

def NewClient(clientSocket, addr):
    global clientlist
    global clientdict
    clientlist += [clientSocket]
    clientdict[str(addr[1])] = clientSocket
    while True:
        Incoming = clientSocket.recv(1024).decode()
        if Incoming == 'close':
            break
        print(str(addr[0]) + ': ' + Incoming)
    clientSocket.close()
    clientlist.remove(clientSocket)

def Broadcast():
    global userlist
    Outgoing = input()
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    Outgoing = 'Server Broadcast: ' + Outgoing
    print(Outgoing)
    for c in clientlist:
        c.send(Outgoing.encode())

def main():
    global userlist
    global clientlist
    Host = '0.0.0.0'
    Port = 12345

    serverSocket =  socket(AF_INET, SOCK_STREAM)

    serverSocket.bind((Host, Port))

    serverSocket.listen(5)

    print('Server Open. Waiting for Clients to Connect...')
    serverMessage = 'Server Broadcast: Thank you for connecting!' + '\n'

    while True:
        BroadcastThread = Thread(target=Broadcast)
        BroadcastThread.start()
        Connection, addr = serverSocket.accept()
        userlist += [addr[0]]
        ClientThread = Thread(target=NewClient, args=(Connection,addr))
        ClientThread.start()
        print('Got Connection', addr)
        for c in clientlist:
            msg = addr[0] + ' has joined!' + '\n'
            c.send(msg.encode())
        Connection.send(serverMessage.encode())
        Connection.send('Current members: '.encode())
        for user in userlist:
            user = user + '\n'
            Connection.send(user.encode())


if __name__ == '__main__':
    main()
    