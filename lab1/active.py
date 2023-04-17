import socket

# Configure the IP address and port number of the echo server
HOST = 'localhost'
PORT = 6000

# Create a socket object of type AF_INET and SOCK_STREAM
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the echo server
client.connect((HOST, PORT))

while True:
    # Read the message typed by the user
    message = input('Type your message (or "fim" to exit): ').encode()

    # Send the message to the server
    client.sendall(message)

    # Close the connection if the message is "quit"
    if message == b'fim':
        client.close()
        break

    # Receive the message back from the server and print it on the screen
    message_back = client.recv(1024).decode()
    print('Message back:', message_back)
