class Task:
    def __init__(self, task_id, submit_time, cpu_req, mem_req, actual_runtime, estimated_runtime):
        self.task_id = task_id
        self.submit_time = submit_time
        self.cpu_req = cpu_req
        self.mem_req = mem_req
        self.actual_runtime = actual_runtime
        self.estimated_runtime = estimated_runtime
        
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        """Tie-breaker for heapq when two events happen at the exact same time."""
        return str(self.task_id) < str(other.task_id)

    def __repr__(self):
        return f"Task_{self.task_id}(cpu={self.cpu_req}, mem={self.mem_req}, est_time={self.estimated_runtime})"


class Machine:
    def __init__(self, machine_id, total_cpu, total_mem):
        self.machine_id = machine_id
        self.total_cpu = total_cpu
        self.total_mem = total_mem
        
        self.available_cpu = total_cpu
        self.available_mem = total_mem
        
        self.active_tasks = []

    def can_fit(self, task):
        """Checks if the machine has enough resources for the task."""
        return self.available_cpu >= task.cpu_req and self.available_mem >= task.mem_req

    def allocate(self, task):
        """Assigns a task to the machine and updates available resources."""
        if self.can_fit(task):
            self.available_cpu -= task.cpu_req
            self.available_mem -= task.mem_req
            self.active_tasks.append(task)
            return True
        return False

    def __repr__(self):
        return f"Machine_{self.machine_id}(avail_cpu={self.available_cpu}/{self.total_cpu}, avail_mem={self.available_mem}/{self.total_mem})"