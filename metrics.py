from thread import Thread

def calculate_metrics(threads: list[Thread], gantt_chart: list[tuple[str,int]]) -> dict:
    '''
    Computes summary performance metircs for teh scheduling simulation
    Args: 
    threads: List of completed thread objects
    total_time: Total simulation time (in ticks)
    Returns:
    dict: containing the average waiting time, average turnarround time, 
     CPU utilization, and throughput.
    '''
    n = len(threads)

    # Computing the total simulation time
    total_time = len(gantt_chart)

    # CPU busy_time = count the number of tickc where CPU was NOT IDLE
    busy_time = sum(1 for tid, _ in gantt_chart if tid != "IDLE")

    # Average Waiting Time
    avg_waiting = sum(th.waiting_time for th in threads) / n if n > 0 else 0

    # Average Turnaround Time
    avg_turnaround = sum(th.turnaround_time for th in threads) / n if n >0 else 0

    # CPU Utilization (percentage) = (Time CPU busy(which is sum of all bursts) / Total simulation time
    cpu_utilization = (busy_time / total_time * 100) if total_time > 0 else 0

    # Throughput = completed threads / total simulation time
    throughput = (n/ total_time) if total_time > 0 else 0

    return {
        "average_waiting_time" : avg_waiting, 
        "average_turnaround_time" : avg_turnaround, 
        "cpu_utilization" : cpu_utilization, 
        "throughput" : throughput, 
        "total_time": total_time
    }
    