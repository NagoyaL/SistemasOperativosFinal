import os
from container_manager import ContainerManager
from scheduler import Scheduler
from command_logger import CommandLogger

def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    container_manager = ContainerManager()
    logger = CommandLogger()
    scheduler = Scheduler(container_manager, logger)

    while True:
        command = input("Enter command to schedule (or 'done' to finish): ")
        if command.lower() == 'done':
            break
        start_time = int(input("Enter start time for the command: "))
        estimated_time = int(input("Enter estimated execution time for the command: "))
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

    print("\nLogged commands:")
    logger.list_commands()

if __name__ == "__main__":
    main()
