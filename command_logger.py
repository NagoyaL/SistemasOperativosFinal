import os
import json

class CommandLogger:
    def __init__(self):
        self.log_file = 'data/command_log.json'
        self.execution_file = 'data/executions.json'
        self.commands = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                self.commands = json.load(f)
        self.executions = []
        if os.path.exists(self.execution_file):
            with open(self.execution_file, 'r') as f:
                self.executions = json.load(f)

    def log_command(self, command, start_time, estimated_time):
        self.commands.append({'command': command, 'start_time': start_time, 'estimated_time': estimated_time})
        with open(self.log_file, 'w') as f:
            json.dump(self.commands, f, indent=4)

    def list_commands(self):
        for command in self.commands:
            print(f"Command: {command['command']}, Start time: {command['start_time']}, Estimated time: {command['estimated_time']}")

    def save_execution(self, execution):
        self.executions.append(execution)
        with open(self.execution_file, 'w') as f:
            json.dump(self.executions, f, indent=4)

    def load_executions(self):
        if os.path.exists(self.execution_file):
            with open(self.execution_file, 'r') as f:
                self.executions = json.load(f)
        return self.executions
