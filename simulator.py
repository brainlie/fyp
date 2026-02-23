import heapq
from models import Machine

TASK_ARRIVAL = 1
TASK_COMPLETION = 2

class Simulator:
    def __init__(self, policy="first_fit"):
        self.policy = policy
        self.current_time = 0
        self.event_queue = []
        self.active_machines = []
        self.total_machines_provisioned = 0
        
    def add_task(self, task):
        heapq.heappush(self.event_queue, (task.submit_time, TASK_ARRIVAL, task, None))
        
    def run(self):
        print(f"--- Starting Simulation ---")
        while self.event_queue:
            time, event_type, task, machine = heapq.heappop(self.event_queue)
            
            self.current_time = time 
            
            if event_type == TASK_ARRIVAL:
                self._handle_arrival(task)
            elif event_type == TASK_COMPLETION:
                self._handle_completion(task, machine)
        print(f"--- Simulation Ended at Time {self.current_time} ---")
        print(f"Total Machines Provisioned: {self.total_machines_provisioned}\n")
                
    def _handle_arrival(self, task):
        selected_machine = None
        
        # 1. Try to find a spot on an already active machine
        if self.policy == "first_fit":
            for m in self.active_machines:
                if m.can_fit(task):
                    selected_machine = m
                    break # Stop at the first one that fits
                    
        elif self.policy == "best_fit":
            best_score = float('inf')
            for m in self.active_machines:
                if m.can_fit(task):
                    # Calculate leftover resources (lower score = tighter fit)
                    score = (m.available_cpu - task.cpu_req) + (m.available_mem - task.mem_req)
                    if score < best_score:
                        best_score = score
                        selected_machine = m
                        
        # 2. If no active machine can fit the task, provision a new one
        if not selected_machine:
            self.total_machines_provisioned += 1
            # Assuming standard nodes with 4 CPU and 16GB RAM for this test
            new_m = Machine(machine_id=self.total_machines_provisioned, total_cpu=4.0, total_mem=16.0)
            self.active_machines.append(new_m)
            selected_machine = new_m
            print(f"[Time {self.current_time:02d}] Provisioned NEW Machine {new_m.machine_id}")
            
        # 3. Allocate the task to the selected machine
        selected_machine.allocate(task)
        task.start_time = self.current_time
        
        # Schedule completion based on ACTUAL runtime
        completion_time = self.current_time + task.actual_runtime
        task.end_time = completion_time
        
        heapq.heappush(self.event_queue, (completion_time, TASK_COMPLETION, task, selected_machine))
        print(f"[Time {self.current_time:02d}] Task {task.task_id} STARTED on Machine {selected_machine.machine_id}")
            
    def _handle_completion(self, task, machine):
        machine.available_cpu += task.cpu_req
        machine.available_mem += task.mem_req
        machine.active_tasks.remove(task)
        print(f"[Time {self.current_time:02d}] Task {task.task_id} COMPLETED on Machine {machine.machine_id}. Freed resources.")