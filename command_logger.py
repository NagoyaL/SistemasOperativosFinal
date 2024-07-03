import json
import os

class CommandLogger:
    def __init__(self, log_file='data/commands_log.json'):
        self.log_file = log_file
        self.commands = self.load_commands()

    def load_commands(self):
        if not os.path.exists(self.log_file):
            # Crear el archivo y escribir una lista vacía si no existe
            with open(self.log_file, 'w') as f:
                json.dump([], f)
            return []
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Si el archivo existe pero está vacío o no es un JSON válido, inicializarlo
            with open(self.log_file, 'w') as f:
                json.dump([], f)
            return []

    def save_commands(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.commands, f, indent=4)

    def log_command(self, command, start_time, estimated_time):
        self.commands.append({
            'command': command,
            'start_time': start_time,
            'estimated_time': estimated_time
        })
        self.save_commands()

    def list_commands(self):
        for cmd in self.commands:
            print(f"Command: {cmd['command']}, Start Time: {cmd['start_time']}, Estimated Time: {cmd['estimated_time']}")

    def get_commands(self):
        return self.commands
