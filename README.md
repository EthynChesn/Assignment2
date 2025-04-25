v1.0 - As of now - it's at least possible for the server and client to communicate without waiting one at a time... but there are Thread errors when the connection is closed. I'm not sure what happens when multiple clients try to connect to the server.


v2.0 - Server and Client and communicate. No threading errors. Multiple clients connect and can message the server, but the server seems to send messages to a random client


v3.0 - Server now broadcasts to all clients. Server announces when a member has joined, and shows the lists of current members when client first joins. Clients can send messages to server and all clients, but not privately.


v4.0 - Clients can now send messages privately, but can't stop sending them once switching. There are many bugs with Private Chat mode.


v5.0 - Clients can now exit Private Chat, but the feature is still very buggy between two clients
