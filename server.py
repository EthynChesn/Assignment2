from socket import *
from threading import *
import sys

#Create Socket
serverSocket =  socket(AF_INET, SOCK_STREAM)

#Client information storage. Client List stores connections, Client dictionary pairs connections with client IDs, userlist stores client IDs
clientlist = []
clientdict = {}
userlist = []

#Client Handler Function
def NewClient(clientSocket, addr):
    global clientlist
    global clientdict
    #Add connection to clientlist and clientdict. Set intended recipient to server/global
    clientlist += [clientSocket]
    clientdict[str(addr[1])] = clientSocket
    recipient = 'Server'
    #Listen for incoming data
    while True:
        Incoming = clientSocket.recv(1024).decode()
        #Close connection command
        if Incoming == '/close':
            break
        #Check if recipient is not server for private chats
        while not recipient == 'Server':
            #end private chat command
            if Incoming == '/end':
                recipient = 'Server'
                break
            #Send data to intended recipient privately
            Incoming = '[Private Message]  ' + str(addr[1]) + ': ' + Incoming
            clientdict[recipient].send(Incoming.encode())
            break
        #Check if incoming data is a client ID, set them as recipient
        if Incoming in userlist:
            recipient = Incoming
        #Else (and not /end), print data on server and send to every client
        elif not Incoming == '/end' and recipient == 'Server':
            print(str(addr[1]) + ': ' + Incoming)
            Incoming = str(addr[1]) + ': ' + Incoming
            for c in clientlist:
                if not c == clientSocket:
                    c.send(Incoming.encode())
   #close connection and remove from storage             
    clientSocket.close()
    clientlist.remove(clientSocket)
    del clientdict[str(addr[1])]
    userlist.remove(str(addr[1]))

#Broadcast function (send message from server to all clients)
def Broadcast():
    while True:
        global userlist
        Outgoing = input()
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        #Close all connections and close server socket
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

#Main function
def main():
    global serverSocket
    global userlist
    global clientlist
    #initiliaze Host and Port
    Host = '0.0.0.0'
    Port = 12345
    #Bind socket to Port
    serverSocket.bind((Host, Port))
    #Listen for clients
    serverSocket.listen(5)

    print('Server Open. Waiting for Clients to Connect...')
    serverMessage = 'Server Broadcast: Welcome, thank you for connecting!' + '\n'
    #Accept clients and send initial data
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
            
#Start
if __name__ == '__main__':
    main()
    
