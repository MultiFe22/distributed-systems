import socket

# Configure the IP address and port number that the server will listen to
HOST = 'localhost'
PORT = 6000

# Create a socket object of type AF_INET and SOCK_STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to the specified IP address and port
server.bind((HOST, PORT))

# Set the server to listen for connections
server.listen()

print('Echo server waiting for connections on port', PORT)

while True:
    # Wait for a connection
    connection, address = server.accept()
    print('Connection established with', address)

    while True:
        # Receive the message from the client
        message = connection.recv(1024)
        if not message:
            break

        # Send the message back to the client
        connection.sendall(message)

    print('Connection closed with', address)
    connection.close()
    break
