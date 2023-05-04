# The code imports the socket module for network communication,
# the Thread class from the threading module for handling concurrent
# execution of multiple threads

import socket
from threading import Thread

# The code initializes the IP address and port number on which the server socket will listen.
ip = "127.0.0.1"
port = 12355

# The code creates a TCP socket using IPv4 address family (AF_INET) and the stream data transmission protocol (SOCK_STREAM).
# It then binds the socket to the specified IP address and port number and listens for incoming client connections.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, port))
server_socket.listen()

# Prints a message to the console indicating that the server is listening.
print(f"Socket is listen on port {port}")

# The code initializes several variables to store information about connected clients, active groups, and user names and IDs.
clients_sockets = []
IDs = []
users = []

server_menu = """
===================================
1) View active users
2) Chat with all active users
3) Exit from app
Choose An Option From 1 To 3 : 
"""


# The broadcast function is defined to handle sending messages from a client to all connected clients.
def broadcast(message):
    try:
        for client_socket in clients_sockets:
            client_socket.send(message.encode())
    except (OSError, TimeoutError):
        return


# The connection function is defined to handle the connection of a new client to the server.
# It receives the client socket as client_socket and adds the client to the clients list.
# it also receives the user name and ID from the client and adds them to the users list.
# The function then sends a welcome message to the client.
# and then keep listening for messages from the client and sending them to all other clients.
# also if the client send "3" the function will remove the client from the clients list and the users list.
def connection(client_socket):
    try:
        user_name = client_socket.recv(1024).decode()
        user_id = client_socket.recv(1024).decode()
        while user_id in IDs:
            client_socket.send("Your ID is not valid , Enter a valid ID :".encode())
            user_id = client_socket.recv(1024).decode()

        IDs.append(user_id)
        clients_sockets.append(client_socket)
        users.append((user_name, user_id))
        client_socket.send("Account ready".encode())
    except (OSError, TimeoutError):
        return

    while True:
        try:
            client_socket.send(server_menu.encode())
            data = client_socket.recv(1024).decode()
            if data == "1":
                try:
                    client_socket.send("===================================\nLIST OF All ACTIVE USER\n".encode())
                    client_socket.send("name >>>>>>  id\n".encode())
                    for user_name, user_id in users:
                        client_socket.send(f"{user_name} >>>>>>  {user_id}\n".encode())
                except (OSError, TimeoutError):
                    return

            elif data == "2":
                client_socket.send("Start Chat\nIf you want to end chatting type 'end'".encode())

                while True:
                    # the Client enter in a while loop to send message to all clients and if he want to end chat he type "end"
                    client_message = client_socket.recv(1024).decode()
                    if client_message == "end":
                        broadcast(f"{user_name} End chat")
                        break
                    client_message = f"{user_name} > {client_message}"
                    broadcast(client_message)

            elif data == "3":
                client_socket.send("client exit the Chat App".encode())
                # get the index of the client in the list of clients sockets
                index = clients_sockets.index(client_socket)
                # remove the client from the list of clients sockets
                clients_sockets.remove(client_socket)
                # remove the client from the list of users
                user_name = users[index]
                users.remove(users[index])
                # remove the client from the list of IDs
                user_id = IDs[index]
                IDs.remove(IDs[index])
                print(f"Client > ({user_name}) with ID > ({user_id}) has left the Chat App.")

        except (OSError, TimeoutError):
            continue


while True:
    try:
        # accept return address(ip of client) and socket Address.
        client_socket, addr = server_socket.accept()
        connection_thread = Thread(target=connection, args=(client_socket,))
        connection_thread.start()
    except KeyboardInterrupt:
        server_socket.close()
        exit(0)