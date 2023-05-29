import rpyc
import os

# Load dictionary from backup
dictionary = {}
with open("backup.txt", "r") as backup:
    for line in backup.readlines():
        line = line.strip()
        key, value = line.split(":")
        values = dictionary.get(key, [])
        values.append(value)
        dictionary[key] = values
print("Dictionary loaded from backup file.")

class MyService(rpyc.Service):
    def on_connect(self, conn):
        print("Client connected.")
    
    def on_disconnect(self, conn):
        # Save dictionary to backup
        with open("backup.txt", "w") as backup:
            for key, values in dictionary.items():
                for value in values:
                    backup.write(f"{key}:{value}\n")
        print("Dictionary saved to backup file.")
        print("Client disconnected.")

    def exposed_set(self, key, value):
        # Insert new key-value pair
        if key in dictionary:
            already_exists = True
        else:
            already_exists = False
        values = dictionary.get(key, [])
        values.append(value)
        dictionary[key] = values
        if already_exists:
            return f"Key '{key}' updated successfully."
        else:
            return f"Key '{key}' inserted successfully."

    def exposed_get(self, key):
        # Query the value associated with the key
        if key in dictionary:
            values = dictionary.get(key, [])
            return "\n".join(sorted(values))
        else:
            return f"Key '{key}' not found."

    def exposed_remove(self, key):
        # Remove the key-value pair
        if key in dictionary:
            dictionary.pop(key, None)
            return f"Key '{key}' removed successfully."
        else:
            return f"Key '{key}' not found."

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port = 8080)
    t.start()
