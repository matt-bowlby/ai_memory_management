def print_gantt_chart (gantt_data: list[tuple[str,int]]):
    '''
    Prints a formatted Gantt chart from the recorded threads (id, time) pair
    Highlights preemptions and idle CPU periods'''

    if not gantt_data:
        print("No Gantt data to display.")
        return
    
    print("\n----------- GANTT CHART ----------")

    merged = []
    current_thread, start_time = gantt_data[0]

    # Build merged blocks like: T1, start=0, end = 3
    for i in range(1, len(gantt_data)): 
        thread, time = gantt_data[i]

        if thread != current_thread: 
            # close previous block at this time
            merged.append((current_thread, start_time, time))
            current_thread = thread
            start_time = time

    # add the final block
    last_time = gantt_data[-1][1] + 1
    merged.append((current_thread, start_time, last_time))

    # print the merge blocks
    for thread, start, end in merged: 
        duration = end - start
        label = f"{thread}"

        if thread == "IDLE": # if nothing is running in the CPU 
            print(f"[{start:02d}-{end:02d}] CPU IDLE ({duration} unit)")
        else: 
            print(f"[{start:02d}-{end:02d}] {label:<5} ran ({duration} units)")

    print("----------------------------------------\n")

def print_metrics_table (metrics: dict, threads: list):
    '''
    Print a formatted table of metrics per thread and averages
    Metrics come from mentrics.py'''

    print("\n----------- METRICS SUMMARY ----------")
    print(f"{'Thread':<08}{'Arrive':<08}{'Burst':<08}{'Finish':<08}{'Waitign':<10}{'Turnaround':<12}") 
    
    for th in threads: 
        print(f"{th.thread_id:<08}{th.arrival:<08}{th.burst:<08}{th.completion_time:<08}{th.waiting_time:<10}{th.turnaround_time:<12}")

    print("\nAverages:")
    print(f"Average Waiting Time    : {metrics['average_waiting_time']: .2f}")
    print(f"Average Turnaround Time : {metrics['average_turnaround_time']: .2f}")
    print(f"CPU Utilization         : {metrics['cpu_utilization']: .2f}%")
    print("----------------------------------------\n")