def calculate_metrics(processes):
    """
    Given list of Process objects with .completion_time,
    compute waiting_time, turnaround_time.
    """
    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival
        p.waiting_time = p.turnaround_time - p.burst

def cpu_utilization(processes):
    if not processes:
        return 0.0
    total_burst = sum(p.burst for p in processes)
    makespan = max(p.completion_time for p in processes)
    return total_burst / makespan if makespan > 0 else 0.0

def avg_waiting_time(processes):
    return sum(p.waiting_time for p in processes) / len(processes) if processes else 0

def avg_turnaround_time(processes):
    return sum(p.turnaround_time for p in processes) / len(processes) if processes else 0