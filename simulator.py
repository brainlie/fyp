import heapq

# Event type constants to keep things organized
TASK_ARRIVAL = 1
TASK_COMPLETION = 2

class Simulator:
    def __init__(self, machines):
        self.machines = machines
        self.current_time = 0
        self.event_queue = []
        
    def add_task(self, task):
        """Schedules a task's arrival into the future."""
        heapq.heappush(self.event_queue, (task.submit_time, TASK_ARRIVAL, task, None))
        
    def run(self):
        """The main loop of the simulator."""
        print(f"--- Starting Simulation ---")
        while self.event_queue:
            time, event_type, task, machine = heapq.heappop(self.event_queue)
            
            self.current_time = time 
            
            if event_type == TASK_ARRIVAL:
                self._handle_arrival(task)
            elif event_type == TASK_COMPLETION:
                self._handle_completion(task, machine)
        print(f"--- Simulation Ended at Time {self.current_time} ---")
                
    def _handle_arrival(self, task):
        """Try to schedule the task. Using basic First-Fit for now."""
        scheduled = False
        for m in self.machines:
            if m.allocate(task):
                scheduled = True
                task.start_time = self.current_time
                
                completion_time = self.current_time + task.actual_runtime
                task.end_time = completion_time
                
                heapq.heappush(self.event_queue, (completion_time, TASK_COMPLETION, task, m))
                print(f"[Time {self.current_time:02d}] Task {task.task_id} STARTED on Machine {m.machine_id}")
                break
                
        if not scheduled:
            print(f"[Time {self.current_time:02d}] Task {task.task_id} DROPPED (No available resources)")
            
    def _handle_completion(self, task, machine):
        """Release machine resources when a task finishes."""
        machine.available_cpu += task.cpu_req
        machine.available_mem += task.mem_req
        machine.active_tasks.remove(task)
        print(f"[Time {self.current_time:02d}] Task {task.task_id} COMPLETED on Machine {machine.machine_id}. Freed resources.")