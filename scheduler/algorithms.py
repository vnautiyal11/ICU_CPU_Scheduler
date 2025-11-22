from typing import List, Tuple
import copy

class Process:
    def __init__(self, pid, arrival, burst, priority=None):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority  # lower = higher priority
        self.remaining = burst
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

    def __repr__(self):
        return f"Process({self.pid}, arr={self.arrival}, burst={self.burst})"


def fcfs(processes: List[Process]) -> Tuple[List[Tuple], List[Process]]:
    proc = sorted(copy.deepcopy(processes), key=lambda p: (p.arrival, p.pid))
    gantt = []
    current_time = 0
    for p in proc:
        if current_time < p.arrival:
            current_time = p.arrival
        start = current_time
        current_time += p.burst
        p.completion_time = current_time
        gantt.append((p.pid, start, current_time))
    return gantt, proc


def sjf_non_preemptive(processes: List[Process]) -> Tuple[List[Tuple], List[Process]]:
    proc = sorted(copy.deepcopy(processes), key=lambda p: (p.arrival, p.burst, p.pid))
    gantt = []
    ready_queue = []
    current_time = 0
    completed = []
    i = 0
    n = len(proc)

    while len(completed) < n:
        # Add arrived processes to ready queue
        while i < n and proc[i].arrival <= current_time:
            ready_queue.append(proc[i])
            i += 1
        if not ready_queue:
            current_time = proc[i].arrival
            continue
        # Select shortest job
        ready_queue.sort(key=lambda p: (p.burst, p.pid))
        p = ready_queue.pop(0)
        start = current_time
        current_time += p.burst
        p.completion_time = current_time
        gantt.append((p.pid, start, current_time))
        completed.append(p)
    return gantt, completed


def priority_non_preemptive(processes: List[Process]) -> Tuple[List[Tuple], List[Process]]:
    proc = sorted(copy.deepcopy(processes), key=lambda p: (p.arrival, p.priority, p.pid))
    gantt = []
    ready_queue = []
    current_time = 0
    completed = []
    i = 0
    n = len(proc)

    while len(completed) < n:
        while i < n and proc[i].arrival <= current_time:
            ready_queue.append(proc[i])
            i += 1
        if not ready_queue:
            current_time = proc[i].arrival
            continue
        # Lower priority number = higher priority
        ready_queue.sort(key=lambda p: (p.priority, p.pid))
        p = ready_queue.pop(0)
        start = current_time
        current_time += p.burst
        p.completion_time = current_time
        gantt.append((p.pid, start, current_time))
        completed.append(p)
    return gantt, completed


def round_robin(processes: List[Process], quantum: int) -> Tuple[List[Tuple], List[Process]]:
    proc = copy.deepcopy(processes)
    # Sort by arrival, then PID for deterministic tie-breaking
    proc.sort(key=lambda p: (p.arrival, p.pid))
    gantt = []
    queue = []
    current_time = 0
    i = 0
    n = len(proc)

    while i < n or queue:
        # Add newly arrived processes
        while i < n and proc[i].arrival <= current_time:
            queue.append(proc[i])
            i += 1
        if not queue:
            current_time = proc[i].arrival
            continue

        p = queue.pop(0)
        exec_time = min(p.remaining, quantum)
        start = current_time
        current_time += exec_time
        p.remaining -= exec_time

        gantt.append((p.pid, start, current_time))

        # Re-add if not finished
        if p.remaining > 0:
            # Add newly arrived during execution
            while i < n and proc[i].arrival <= current_time:
                queue.append(proc[i])
                i += 1
            queue.append(p)
        else:
            p.completion_time = current_time
            # Add newly arrived before next
            while i < n and proc[i].arrival <= current_time:
                queue.append(proc[i])
                i += 1

    # Return original (non-deepcopy needed — we mutated remaining but preserved burst)
    # Reconstruct completion times from gantt if needed (robust way)
    # But easier: recompute from gantt for accuracy
    completion_map = {}
    for pid, _, end in gantt:
        completion_map[pid] = end
    for p in processes:
        p.completion_time = completion_map.get(p.pid, 0)

    return gantt, processes