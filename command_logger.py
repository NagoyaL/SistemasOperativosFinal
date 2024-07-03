import json

class CommandLogger:
    def __init__(self, filename='data/command_log.json'):
        self.filename = filename
        self.load_commands()

    def log_command(self, command, start_time, estimated_time):
        self.commands.append({
            'command': command,
            'start_time': start_time,
            'estimated_time': estimated_time
        })
        self.save_commands()

    def save_commands(self):
        with open(self.filename, 'w') as f:
            json.dump(self.commands, f, indent=4)

    def load_commands(self):
        try:
            with open(self.filename, 'r') as f:
                self.commands = json.load(f)
        except FileNotFoundError:
            self.commands = []

    def list_commands(self):
        for cmd in self.commands:
            print(f"Command: {cmd['command']}, Start time: {cmd['start_time']}, Estimated time: {cmd['estimated_time']}")

    def save_execution(self, execution):
        executions = self.load_executions()
        executions.append(execution)
        with open('data/executions.json', 'w') as f:
            json.dump(executions, f, indent=4)

    def load_executions(self):
        try:
            with open('data/executions.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def list_executions(self):
        executions = self.load_executions()
        for execution in executions:
            print(f"Commands: {execution['commands']}")
            print(f"Algorithm: {execution['algorithm']}")
            print(f"Log: {execution['log']}")
