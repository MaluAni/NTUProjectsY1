import socket
import threading

# Connection Details
host = socket.gethostbyname(socket.gethostname())
port = 55555
# Printing Server details for passing on to Clients
print('Server IP is: ', host)
# Starting Server, listening to connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(10)

# Lists For Clients and Their Usernames
clients = []
usernames = []

# Method for Sending Messages to All Connected Clients
def broadcastMessage(text):
    for client in clients:
        client.send(text)

# Method for Handling Messages From Clients
def handleClientMessages(client):
    while True:
        try:
            receivedMessage = client.recv(1024)
            broadcastMessage(receivedMessage)
        except:
            listPosition = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[listPosition]
            broadcastMessage('{} has left the Chat!'.format(username).encode('ascii'))
            usernames.remove(username)
            break

# Method for Receiving and Listening from/to Clients
def receiveFromClients():
    while True:
        client, address = server.accept()
        print("{} has connected to the Server".format(str(address)))
        client.send('CODEWORD'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)
        print("Your chosen username is {}".format(username))
        broadcastMessage("{} has joined the Chat!".format(username).encode('ascii'))
        client.send('You have connected to the server! '
                    '\nType your message in the bottom part of the window and press the Enter key'.encode('ascii'))
        thread = threading.Thread(target=handleClientMessages, args=(client,))
        thread.start()

receiveFromClients()
