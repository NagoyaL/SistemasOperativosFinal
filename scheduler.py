import time
from collections import deque

class Scheduler:
    def __init__(self, container_manager, logger):
        self.container_manager = container_manager
        self.logger = logger
        self.commands = []
        self.execution_log = []

    def add_command(self, command, start_time, estimated_time):
        self.commands.append((command, start_time, estimated_time))

    def fcfs(self):
        self.commands.sort(key=lambda x: x[1])
        for command, start_time, estimated_time in self.commands:
            image = self.container_manager.create_or_get_image(command)
            time.sleep(start_time)
            start_exec_time = time.time()
            self.container_manager.run_container(image)
            time.sleep(estimated_time)
            end_exec_time = time.time()
            turnaround_time = end_exec_time - start_exec_time
            response_time = start_exec_time - start_time
            self.execution_log.append((command, turnaround_time, response_time))
            print(f"Executed command: {command}, Turnaround time: {turnaround_time:.2f}, Response time: {response_time:.2f}")

    def round_robin(self, quantum=2):
        queue = deque(self.commands)
        current_time = 0

        while queue:
            command, start_time, estimated_time = queue.popleft()

            if current_time < start_time:
                time.sleep(start_time - current_time)
                current_time = start_time

            image = self.container_manager.create_or_get_image(command)
            start_exec_time = time.time()

            if estimated_time <= quantum:
                self.container_manager.run_container(image)
                time.sleep(estimated_time)
                end_exec_time = time.time()
                turnaround_time = end_exec_time - start_exec_time
                response_time = start_exec_time - start_time
                self.execution_log.append((command, turnaround_time, response_time))
                current_time += estimated_time
            else:
                self.container_manager.run_container(image)
                time.sleep(quantum)
                end_exec_time = time.time()
                remaining_time = estimated_time - quantum
                queue.append((command, current_time + quantum, remaining_time))
                turnaround_time = end_exec_time - start_exec_time
                response_time = start_exec_time - start_time
                self.execution_log.append((command, turnaround_time, response_time))
                current_time += quantum

    def spn(self):
        self.commands.sort(key=lambda x: x[2])
        for command, start_time, estimated_time in self.commands:
            image = self.container_manager.create_or_get_image(command)
            time.sleep(start_time)
            start_exec_time = time.time()
            self.container_manager.run_container(image)
            time.sleep(estimated_time)
            end_exec_time = time.time()
            turnaround_time = end_exec_time - start_exec_time
            response_time = start_exec_time - start_time
            self.execution_log.append((command, turnaround_time, response_time))
            print(f"Executed command: {command}, Turnaround time: {turnaround_time:.2f}, Response time: {response_time:.2f}")

    def srt(self):
        self.commands.sort(key=lambda x: x[1])
        remaining_times = {command: estimated_time for command, start_time, estimated_time in self.commands}
        current_time = 0

        while remaining_times:
            next_command = min(remaining_times, key=remaining_times.get)
            estimated_time = remaining_times[next_command]
            image = self.container_manager.create_or_get_image(next_command)
            start_exec_time = time.time()

            if estimated_time > 0:
                self.container_manager.run_container(image)
                time.sleep(1)
                remaining_times[next_command] -= 1
                if remaining_times[next_command] <= 0:
                    del remaining_times[next_command]
                    end_exec_time = time.time()
                    turnaround_time = end_exec_time - start_exec_time
                    response_time = start_exec_time - current_time
                    self.execution_log.append((next_command, turnaround_time, response_time))
                    current_time += estimated_time
                else:
                    current_time += 1

    def hrrn(self):
        self.commands.sort(key=lambda x: x[1])
        current_time = 0
        while self.commands:
            hrrn_scores = []
            for command, start_time, estimated_time in self.commands:
                wait_time = max(0, current_time - start_time)
                hrrn = (wait_time + estimated_time) / estimated_time
                hrrn_scores.append((hrrn, command, start_time, estimated_time))
            hrrn_scores.sort(reverse=True)
            _, command, start_time, estimated_time = hrrn_scores.pop(0)
            self.commands.remove((command, start_time, estimated_time))
            image = self.container_manager.create_or_get_image(command)
            if current_time < start_time:
                time.sleep(start_time - current_time)
                current_time = start_time
            start_exec_time = time.time()
            self.container_manager.run_container(image)
            time.sleep(estimated_time)
            end_exec_time = time.time()
            turnaround_time = end_exec_time - start_exec_time
            response_time = start_exec_time - start_time
            self.execution_log.append((command, turnaround_time, response_time))
            current_time += estimated_time

    def show_times(self):
        total_turnaround_time = sum(t[1] for t in self.execution_log)
        total_response_time = sum(t[2] for t in self.execution_log)
        num_commands = len(self.execution_log)

        print("\nExecution times:")
        for command, turnaround_time, response_time in self.execution_log:
            print(f"Command: {command}, Turnaround time: {turnaround_time:.2f}, Response time: {response_time:.2f}")

        print(f"\nAverage Turnaround time: {total_turnaround_time / num_commands:.2f}")
        print(f"Average Response time: {total_response_time / num_commands:.2f}")
