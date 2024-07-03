import os
import json
from container_manager import ContainerManager
from scheduler import Scheduler
from command_logger import CommandLogger

def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    container_manager = ContainerManager()
    logger = CommandLogger()
    scheduler = Scheduler(container_manager, logger)

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
        elif choice == 2:
            print("Executing with Round Robin scheduling:")
            scheduler.round_robin()
        elif choice == 3:
            print("Executing with SPN scheduling:")
            scheduler.spn()
        elif choice == 4:
            print("Executing with SRT scheduling:")
            scheduler.srt()
        elif choice == 5:
            print("Executing with HRRN scheduling:")
            scheduler.hrrn()
        else:
            print("Invalid choice. Exiting.")
            return

        scheduler.show_times()
        execution = {
            'commands': commands,
            'algorithm': choice,
            'log': scheduler.execution_log
        }
        logger.save_execution(execution)

        print("\nLogged commands:")
        logger.list_commands()
    elif choice == 2:
        past_executions = logger.load_executions()
        if not past_executions:
            print("No past executions found.")
            return

        for idx, execution in enumerate(past_executions):
            print(f"{idx + 1}. Execution with algorithm {execution['algorithm']} and commands: {execution['commands']}")

        exec_choice = int(input("Select execution to re-run: ")) - 1
        if exec_choice < 0 or exec_choice >= len(past_executions):
            print("Invalid choice. Exiting.")
            return

        execution = past_executions[exec_choice]
        scheduler.clear_commands()
        for command, start_time, estimated_time in execution['commands']:
            scheduler.add_command(command, start_time, estimated_time)

        print("Select new scheduling algorithm:")
        print("1. FCFS")
        print("2. Round Robin")
        print("3. SPN")
        print("4. SRT")
        print("5. HRRN")

        new_choice = int(input("Enter your choice (1-5): "))

        if new_choice == 1:
            print("Executing with FCFS scheduling:")
            scheduler.fcfs()
        elif new_choice == 2:
            print("Executing with Round Robin scheduling:")
            scheduler.round_robin()
        elif new_choice == 3:
            print("Executing with SPN scheduling:")
            scheduler.spn()
        elif new_choice == 4:
            print("Executing with SRT scheduling:")
            scheduler.srt()
        elif new_choice == 5:
            print("Executing with HRRN scheduling:")
            scheduler.hrrn()
        else:
            print("Invalid choice. Exiting.")
            return

        scheduler.show_times()
        new_execution = {
            'commands': execution['commands'],
            'algorithm': new_choice,
            'log': scheduler.execution_log
        }
        logger.save_execution(new_execution)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
