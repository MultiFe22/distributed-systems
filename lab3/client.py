import rpyc

def client_interface():
    conn = rpyc.connect("localhost", 8080)

    while True:
        command = input(">")
        if command.startswith("remove"):
            if len(command.split("=")) != 2:
                print("Invalid command.")
                continue
            key = command.split("=")[1]
            print(conn.root.remove(key))
        elif command.startswith("get"):
            if len(command.split("=")) != 2:
                print("Invalid command.")
                continue
            key = command.split("=")[1]
            print(conn.root.get(key))
        elif command.startswith("set"):
            if len(command.split("=")) != 2:
                print("Invalid command.")
                continue
            key_value = command.split("=")[1]
            key, value = key_value.split(":")
            print(conn.root.set(key, value))
        elif command == "quit":
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    client_interface()
