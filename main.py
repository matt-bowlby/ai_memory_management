import time
from pathlib import Path

from algorithms.first_come_first_serve import FCFS
from algorithms.shortest_job_first import SJF
from algorithms.priority import Priority
from algorithms.round_robin import RR
from algorithms.preemptive_shortest_job_first import PreemptiveSJF
from algorithms.multilevel_queue import MultilevelQueue

from dispatcher import Dispatcher
from thread_file_loader import load_threads_from_file
from thread_generator import generate_threads

from metrics import calculate_metrics
from visualize import display_gantt_chart, print_metrics_table
from thread import Thread
from algorithms import Algorithm

TICK_RATE = 100  # Ticks per second


def input_validate(prompt: str, condition_func, error_msg: str = "Invalid input. Please try again.\n") -> str:
    while True:
        value = input(prompt)
        if condition_func(value):
            return value
        else:
            print(error_msg)


def run(threads: list[Thread], algorithm: Algorithm) -> None:
    tick_interval = 1.0 / TICK_RATE
    next_tick = time.time() + tick_interval

    dispatcher = Dispatcher(threads, algorithm)

    # Main loop
    while not dispatcher.is_finished():
        dispatcher.tick()

        # Wait until the next tick
        sleep_duration = next_tick - time.time()
        if sleep_duration > 0:
            time.sleep(sleep_duration)
        next_tick += tick_interval

    # Simulation Finished
    total_time = dispatcher.time_step
    print("\n---------- SIMULATION COMPLETE ----------")
    print(f"Total Time: {total_time} ticks\n")

    # Print Metrics and Gantt Chart
    metrics = calculate_metrics(dispatcher.threads, dispatcher.gantt_chart)
    display_gantt_chart(dispatcher.gantt_chart)
    print_metrics_table(metrics, dispatcher.threads)


def main():
    print("Welcome to the thread scheduling simulator.")
    while True:
        print("Please select an algorithm to run:")
        print("1. FCFS")
        print("2. SJF")
        print("3. Priority")
        print("4. Round Robin")
        print("5. Preemptive SJF")
        print("6. Multilevel Queue")
        print("0. Exit")
        choice = input_validate(
            "Please enter your choice: ",
            lambda x: x in {"0", "1", "2", "3", "4", "5", "6"}
        )

        algorithm = None
        match choice:
            case "0":
                break
            case "1":
                algorithm = FCFS()
            case "2":
                algorithm = SJF()
            case "3":
                algorithm = Priority()
            case "4":
                quantum = int(input("Please specify a qauntum: "))
                algorithm = RR(quantum)
            case "5":
                algorithm = PreemptiveSJF()
            case "6":
                quantum = int(input("Please specify a qauntum: "))
                algorithm = MultilevelQueue(quantum)

        print("How do you want to input threads?")
        print("1. From a file")
        print("2. From the console")
        print("3. Randomly generate")
        choice = input_validate(
            "Please enter your choice: ",
            lambda x: x in {"1", "2", "3"}
        )

        threads = []

        match choice:
            case "1":
                file_name = input_validate(
                    "Please specify a file name: ",
                    lambda x: Path(x).is_file()
                )
                threads = load_threads_from_file(file_name)

            case "2":
                thread_id = input_validate(
                    "Please specify a thread ID: ",
                    lambda x: x != ""
                )
                arrival = int(
                    input_validate(
                        "Please specify an arrival time: ",
                        lambda x: x.isdigit() and int(x) >= 0,
                        "Arrival time cannot be negative. Please try again.\n",
                    )
                )
                burst = int(
                    input_validate(
                        "Please specify a burst time: ",
                        lambda x: x.isdigit() and int(x) > 0,
                        "Burst time must be positive. Please try again.\n",
                    )
                )
                priority = int(
                    input_validate(
                        "Please specify a priority: ",
                        lambda x: x.isdigit() and int(x) >= 0,
                        "Priority cannot be negative. Please try again.\n",
                    )
                )
                threads.append(Thread(thread_id, arrival, burst, priority))

            case "3":
                num = int(
                    input_validate(
                        "Enter the number of threads: ",
                        lambda x: x.isdigit() and int(x) > 0,
                        "Number of threads must be positive. Please try again.\n",
                    )
                )
                max_arrival_time = int(
                    input_validate(
                        "Enter the maximum arrival time: ",
                        lambda x: x.isdigit() and int(x) >= 0,
                        "Maximum arrival time cannot be negative. Please try again.\n",
                    )
                )
                max_burst_time = int(
                    input_validate(
                        "Enter the maximum burst time: ",
                        lambda x: x.isdigit() and int(x) > 0,
                        "Maximum burst time must be positive. Please try again.\n",
                    )
                )
                max_priority = int(
                    input_validate(
                        "Enter the maximum priority: ",
                        lambda x: x.isdigit() and int(x) >= 0,
                        "Maximum priority cannot be negative. Please try again.\n",
                    )
                )
                threads = generate_threads(
                    num,
                    max_arrival_time,
                    (1, max_burst_time),
                    (0, max_priority),
                )

        print("Running threads...\n")

        if threads and algorithm:
            run(threads, algorithm)

        input("Press enter to continue...")


if __name__ == "__main__":
    main()
