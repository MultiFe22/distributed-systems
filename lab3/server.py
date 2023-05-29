import rpyc
import os

class MyService(rpyc.Service):
    def on_connect(self, conn):
        # Load dictionary from backup
        self.dictionary = {}
        with open("backup.txt", "r") as backup:
            for line in backup.readlines():
                line = line.strip()
                key, value = line.split(":")
                values = self.dictionary.get(key, [])
                values.append(value)
                self.dictionary[key] = values
        print("Dictionary loaded from backup file.")
    
    def on_disconnect(self, conn):
        # Save dictionary to backup
        with open("backup.txt", "w") as backup:
            for key, values in self.dictionary.items():
                for value in values:
                    backup.write(f"{key}:{value}\n")
        print("Dictionary saved to backup file.")

    def exposed_set(self, key, value):
        # Insert new key-value pair
        values = self.dictionary.get(key, [])
        values.append(value)
        self.dictionary[key] = values
        return f"Key '{key}' inserted successfully."

    def exposed_get(self, key):
        # Query the value associated with the key
        if key in self.dictionary:
            values = self.dictionary.get(key, [])
            return "\n".join(sorted(values))
        else:
            return f"Key '{key}' not found."

    def exposed_remove(self, key):
        # Remove the key-value pair
        if key in self.dictionary:
            self.dictionary.pop(key, None)
            return f"Key '{key}' removed successfully."
        else:
            return f"Key '{key}' not found."

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port = 8080)
    t.start()
