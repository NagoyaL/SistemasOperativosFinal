import os
import json
from container_manager import ContainerManager
from scheduler import Scheduler
from command_logger import CommandLogger

ALGORITHMS = {
    1: "FCFS",
    2: "Round Robin",
    3: "SPN",
    4: "SRT",
    5: "HRRN"
}

def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    container_manager = ContainerManager()
    logger = CommandLogger()
    scheduler = Scheduler(container_manager, logger)
    executions = load_executions()

    print("1. Nueva ejecucion")
    print("2. Usar ejecucion pasada con otro algoritmo")
    print("3. Listar ejecuciones pasadas")
    choice = int(input("Escoja (1-3): "))

    if choice == 1:
        commands = []

        while True:
            command = input("Ingrese el comando (o escriba 'done' para finalizar): ")
            if command.lower() == 'done':
                break
            start_time = int(input("Ingrese el tiempo de inicio para el comando: "))
            estimated_time = int(input("Ingrese el tiempo estimado de ejecucion para el comando: "))
            commands.append((command, start_time, estimated_time))
            scheduler.add_command(command, start_time, estimated_time)
            logger.log_command(command, start_time, estimated_time)

        print("Seleccione el algoritmo de planificacion:")
        for key, value in ALGORITHMS.items():
            print(f"{key}. {value}")

        choice = int(input("Escoja (1-5): "))

        algorithm_name = ALGORITHMS.get(choice, "Invalid")
        if algorithm_name == "Invalid":
            print("Invalid choice. Exiting.")
            return

        print(f"Ejecutando con {algorithm_name} :")
        if choice == 1:
            scheduler.fcfs()
        elif choice == 2:
            scheduler.round_robin()
        elif choice == 3:
            scheduler.spn()
        elif choice == 4:
            scheduler.srt()
        elif choice == 5:
            scheduler.hrrn()

        scheduler.show_times()
        execution = {
            'commands': commands,
            'algorithm': algorithm_name,
            'log': scheduler.execution_log
        }
        logger.save_execution(execution)

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

        print("Seleccione un nuevo algoritmo de planificacion:")
        for key, value in ALGORITHMS.items():
            print(f"{key}. {value}")

        new_choice = int(input("Escoja (1-5): "))

        new_algorithm_name = ALGORITHMS.get(new_choice, "Invalid")
        if new_algorithm_name == "Invalid":
            print("Invalid choice. Exiting.")
            return

        print(f"Executing with {new_algorithm_name} scheduling:")
        if new_choice == 1:
            scheduler.fcfs()
        elif new_choice == 2:
            scheduler.round_robin()
        elif new_choice == 3:
            scheduler.spn()
        elif new_choice == 4:
            scheduler.srt()
        elif new_choice == 5:
            scheduler.hrrn()

        scheduler.show_times()
        new_execution = {
            'commands': execution['commands'],
            'algorithm': new_algorithm_name,
            'log': scheduler.execution_log
        }
        logger.save_execution(new_execution)

    elif choice == 3:
        list_executions(executions)    
    else:
        print("Invalid choice. Exiting.")

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
        print("Commands:")
        for command, start_time, estimated_time in execution['commands']:
            print(f"  Command: {command}, Start time: {start_time}, Estimated time: {estimated_time}")
        print("Log:")
        for log in execution['log']:
            command, turnaround_time, response_time = log
            print(f"  Command: {command}, Turnaround time: {turnaround_time:.2f}, Response time: {response_time:.2f}")

if __name__ == "__main__":
    main()
