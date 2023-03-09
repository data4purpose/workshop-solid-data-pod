import socket

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host, and a well-known port
server_socket.bind(('localhost', 12345))

# become a server socket
server_socket.listen(1)

print("Listening on port 12345...")

while True:
    # accept connections from outside
    (client_socket, client_address) = server_socket.accept()

    # read data from the client
    data = client_socket.recv(1024)

    # print the received data
    print("Received request:", data.decode())

    # close the client socket
    client_socket.close()