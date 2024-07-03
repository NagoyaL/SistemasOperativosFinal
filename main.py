import os
from container_manager import ContainerManager
from scheduler import Scheduler
from command_logger import CommandLogger
import json

def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    container_manager = ContainerManager()
    logger = CommandLogger()
    scheduler = Scheduler(container_manager, logger)

    executions = load_executions()

    while True:
        print("1. New execution")
        print("2. List past executions")
        choice = int(input("Enter your choice (1-2): "))

        if choice == 1:
            commands = []
            while True:
                command = input("Enter command to schedule (or 'done' to finish): ")
                if command.lower() == 'done':
                    break
                start_time = int(input("Enter start time for the command: "))
                estimated_time = int(input("Enter estimated execution time for the command: "))
                commands.append((command, start_time, estimated_time))
                scheduler.add_command(command, start_time, estimated_time)
                logger.log_command(command, start_time, estimated_time)

            print("Select scheduling algorithm:")
            print("1. FCFS")
            print("2. Round Robin")
            print("3. SPN")
            print("4. SRT")
            print("5. HRRN")

            choice = int(input("Enter your choice (1-5): "))

            if choice == 1:
                print("Executing with FCFS scheduling:")
                scheduler.fcfs()
                algorithm = "FCFS"
            elif choice == 2:
                print("Executing with Round Robin scheduling:")
                scheduler.round_robin()
                algorithm = "Round Robin"
            elif choice == 3:
                print("Executing with SPN scheduling:")
                scheduler.spn()
                algorithm = "SPN"
            elif choice == 4:
                print("Executing with SRT scheduling:")
                scheduler.srt()
                algorithm = "SRT"
            elif choice == 5:
                print("Executing with HRRN scheduling:")
                scheduler.hrrn()
                algorithm = "HRRN"
            else:
                print("Invalid choice. Exiting.")
                return

            scheduler.show_times()
            save_execution(commands, algorithm, scheduler.execution_log)

        elif choice == 2:
            list_executions(executions)
        else:
            print("Invalid choice. Exiting.")
            return

        print("\nLogged commands:")
        logger.list_commands()

def load_executions():
    if os.path.exists('data/executions.json'):
        with open('data/executions.json', 'r') as f:
            return json.load(f)
    return []

def save_execution(commands, algorithm, execution_log):
    executions = load_executions()
    executions.append({
        "commands": commands,
        "algorithm": algorithm,
        "execution_log": execution_log
    })
    with open('data/executions.json', 'w') as f:
        json.dump(executions, f, indent=4)

def list_executions(executions):
    for i, execution in enumerate(executions):
        print(f"\nExecution {i+1}:")
        print(f"Algorithm: {execution['algorithm']}")
        for command, start_time, estimated_time in execution['commands']:
            print(f"Command: {command}, Start time: {start_time}, Estimated time: {estimated_time}")
        for log in execution['execution_log']:
            command, turnaround_time, response_time = log
            print(f"Command: {command}, Turnaround time: {turnaround_time:.2f}, Response time: {response_time:.2f}")

if __name__ == "__main__":
    main()
