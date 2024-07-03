import os

class CommandLogger:
    def __init__(self):
        self.log_file = 'data/command_log.txt'

    def log_command(self, command, start_time, estimated_time):
        with open(self.log_file, 'a') as f:
            f.write(f"{command},{start_time},{estimated_time}\n")

    def list_commands(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                for line in f:
                    command, start_time, estimated_time = line.strip().split(',')
                    print(f"Command: {command}, Start time: {start_time}, Estimated time: {estimated_time}")
        else:
            print("No commands logged yet.")
