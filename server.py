from socket import *
from threading import *
import sys

serverSocket =  socket(AF_INET, SOCK_STREAM)
clientlist = []
clientdict = {}
userlist = []

def NewClient(clientSocket, addr):
    global clientlist
    global clientdict
    clientlist += [clientSocket]
    clientdict[str(addr[1])] = clientSocket
    recipient = 'Server'
    while True:
        Incoming = clientSocket.recv(1024).decode()
        if Incoming == '/close':
            break
        while not recipient == 'Server':
            if Incoming == '/end':
                recipient = 'Server'
                break
            Incoming = '[Private Message]  ' + str(addr[1]) + ': ' + Incoming
            clientdict[recipient].send(Incoming.encode())
            break
        if Incoming in userlist:
            recipient = Incoming
        elif not Incoming == '/end':
            print(str(addr[1]) + ': ' + Incoming)
            Incoming = str(addr[1]) + ': ' + Incoming
            for c in clientlist:
                if not c == clientSocket:
                    c.send(Incoming.encode())
                
    clientSocket.close()
    clientlist.remove(clientSocket)
    del clientdict[str(addr[1])]
    userlist.remove(str(addr[1]))

def Broadcast():
    while True:
        global userlist
        Outgoing = input()
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        if Outgoing == '/shutdown':
            print('Server Shut Down')
            for c in clientlist:
                c.close()
            serverSocket.close()
        else:
            Outgoing = 'Server Broadcast: ' + Outgoing
            print(Outgoing)
            for c in clientlist:
                c.send(Outgoing.encode())

def main():
    global serverSocket
    global userlist
    global clientlist
    Host = '0.0.0.0'
    Port = 12345

    serverSocket.bind((Host, Port))

    serverSocket.listen(5)

    print('Server Open. Waiting for Clients to Connect...')
    serverMessage = 'Server Broadcast: Welcome, thank you for connecting!' + '\n'

    while True:
        BroadcastThread = Thread(target=Broadcast)
        BroadcastThread.start()
        Connection, addr = serverSocket.accept()
        userlist += [str(addr[1])]
        ClientThread = Thread(target=NewClient, args=(Connection,addr))
        ClientThread.start()
        print('Got Connection', addr)
        for c in clientlist:
            msg = 'Server Broadcast: ' + str(addr[1]) + ' has joined!' + '\n'
            c.send(msg.encode())
        Connection.send(serverMessage.encode())
        Connection.send('Current users:\n'.encode())
        for user in userlist:
            user = user + '\n'
            Connection.send(user.encode())

if __name__ == '__main__':
    main()
    