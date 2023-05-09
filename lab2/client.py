import socket

# Cria o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
client_socket.connect(('localhost', 8080))

while True:
    # Lê a entrada do usuário
    request = input('> ')

    # Envia a mensagem para o servidor
    client_socket.sendall(request.encode())

    # Espera a resposta do servidor
    response = client_socket.recv(1024)

    # Imprime a resposta
    print(response.decode())
    if response.decode() == "Desconectando...":
        break

# Fecha o socket do cliente
client_socket.close()
