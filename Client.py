import socket
from threading import Thread

def main():
# Setting up the connection information
    ip = "127.0.0.1" #local ip
    port = 12355

    # create a socket object for the client and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# to Initialization the socket
    client_socket.connect((ip, port)) # then we will add the ip and port for it
    print("client ready")

    # prompt the user to enter username, ID and wait until the server confirms the account is ready
    client_socket.send(input("Enter User Name : ").encode())
    client_socket.send(input("Enter ID : ").encode())

# Entering a loop to ensure that the user has a unique ID    
    while client_socket.recv(1024).decode() != "Account ready":
        client_socket.send(input("Enter Unique ID : ").encode())
        
    # create two threads to handle receiving and sending messages
    recv_data_thread = Thread(target=client_recv, args=(client_socket,))
    recv_data_thread.start()

    send_data_thread = Thread(target=client_send, args=(client_socket,))
    send_data_thread.start()

def client_send(client_socket):
    # the client enters a while loop to send messages to the server until they type "end"
    while True:
        try:
            #it will just recive the message from the user and send it to the socket 
            message = input()
            client_socket.send(message.encode())
            
        except (OSError, TimeoutError):
            return
    # close the socket when finished
    client_socket.close()
    return
    
def client_recv(client_socket):
    # the client enters a while loop to receive messages from the server until they receive "client exit the Chat App" message
    while True:
        try:
            #will recive the data which came from the server
            data = client_socket.recv(1024).decode()
            print(data)
            if data == "client exit the Chat App":
                break
        except (OSError, TimeoutError):
            return
    # close the socket and exit the program
    client_socket.close()


if __name__ == "__main__":
    main()
