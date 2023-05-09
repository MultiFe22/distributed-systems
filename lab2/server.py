import socket
import select
import threading
import os

def read_input():
    while True:
        command = input(">")
        if command.startswith("remove"):
            if len(command.split("=")) != 2:
                print("Comando inválido.")
                continue
            key = command.split("=")[1]
            print(key)
            if key in dictionary:
                dictionary.pop(key, None)
                print(f"Chave '{key}' removida com sucesso.")
            else:
                print(f"Chave '{key}' não encontrada.")
        elif command == "quit":
            with open("backup.txt", "w") as backup:
                for key, values in dictionary.items():
                    for value in values:
                        backup.write(f"{key}:{value}\n")
                print("Dicionário salvo no arquivo de backup.")
            os._exit(0)
        else:
            print("Comando inválido.")
# Estrutura de dados para armazenar o dicionário
# Carrega o dicionário a partir do arquivo de backup
dictionary = {}
with open("backup.txt", "r") as backup:
    for line in backup.readlines():
        line = line.strip()
        key, value = line.split(":")
        values = dictionary.get(key, [])
        values.append(value)
        dictionary[key] = values
    print("Dicionário carregado a partir do arquivo de backup.")



# Função para processar as requisições do cliente
def handle_client(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break

        # Decodifica a mensagem do cliente e extrai a chave e o valor (se houver)
        message = data.decode()
        if "=" in message:
            key, value = message.split("=")
        else:
            key = message
            value = None

        # Processa a mensagem do cliente
        response = ""
        if key == "quit":
            # Encerra a conexão com o cliente
            response = "Desconectando..."
            conn.sendall(response.encode())
            break
        elif key == "get" and value is not None:
            # Consulta o valor associado à chave informada
            if value in dictionary:
                values = dictionary.get(value, [])
                response = "\n".join(sorted(values))
            elif value == "":
                response = "Chave não informada."
            else:
                response = f"Chave '{value}' não encontrada."
        elif key == "set" and value is not None:
            # Insere um novo par chave-valor no dicionário
            if value:
                # Separa os valores entre chave e valor
                if ":" not in value:
                    response = "Valor não informado."
                    conn.sendall(response.encode())
                    continue
                insert_key, insert_value = value.split(":")
                values = dictionary.get(insert_key, [])
                values.append(insert_value)
                dictionary[insert_key] = values
                response = f"Chave '{insert_key}' inserida com sucesso."
            else:
                response = "Valor não informado."
        elif len(key)==0:
            response = "Comando inválido."
        else:
            response = "Comando inválido."


        # Codifica a resposta e a envia para o cliente
        conn.sendall(response.encode())

    # Encerra a conexão com o cliente
    conn.close()


# Função para lidar com as conexões de entrada
def accept_connection(server_socket):
    while True:
        conn, addr = server_socket.accept()
        print('Novo cliente conectado:', addr)
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

# Cria o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

server_terminal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_terminal.bind(('localhost', 8081))
server_terminal.listen(1)

# Adiciona o socket do terminal do servidor às entradas do select
inputs = [server_socket, server_terminal]

# Inicia a thread para ler as entradas do terminal do servidor
terminal_thread = threading.Thread(target=read_input)
terminal_thread.start()

# Inicia a thread para aceitar conexões de entrada
accept_thread = threading.Thread(target=accept_connection, args=(server_socket,))
accept_thread.start()

while True:
    # Espera até que uma das entradas esteja pronta para ser lida
    read_sockets, _, _ = select.select(inputs, [], [])
    for sock in read_sockets:
        if sock == server_socket:
            # Uma nova conexão de entrada está pendente
            continue
        elif sock == server_terminal:
            # O socket do terminal do servidor está pronto para ser lido
            conn, _ = server_terminal.accept()
            inputs.append(conn)
        else:
            # O socket está pronto para ser lido
            # Chama a função handle_client em uma nova thread
            client_thread = threading.Thread(target=handle_client, args=(sock,))
            client_thread.start()
