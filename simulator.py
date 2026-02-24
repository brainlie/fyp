import heapq
from models import Machine

TASK_ARRIVAL = 1
TASK_COMPLETION = 2
SCHEDULE_CYCLE = 3 #for CA Algo
MACHINE_SHUTDOWN = 4

class Simulator:
    def __init__(self, policy="first_fit", batch_window=10, idle_timeout=5):
        self.policy = policy
        self.batch_window = batch_window
        self.idle_timeout = idle_timeout

        self.current_time = 0
        self.event_queue = []
        self.event_counter = 0
        self.pending_queue = []
        self.active_machines = []

        self.total_machine_uptime = 0

        self._push_event(0, SCHEDULE_CYCLE, None, None)
        
    def _push_event(self, time, event_type, task, machine):
        self.event_counter += 1
        heapq.heappush(self.event_queue, (time, event_type, self.event_counter, task, machine))

    def add_task(self, task):
        self._push_event(task.submit_time, TASK_ARRIVAL, task, None)
        
    def run(self):
        print(f"--- Starting Simulation ({self.policy.upper()}) ---")
        while self.event_queue:
            time, event_type, _, task, machine = heapq.heappop(self.event_queue)
            
            self.current_time = time 
            
            if event_type == TASK_ARRIVAL:
                self.pending_queue.append(task)
                print(f"[Time {self.current_time:02d}] Task {task.task_id} arrived in queue.")
            elif event_type == TASK_COMPLETION:
                self._handle_completion(task, machine)
            elif event_type == SCHEDULE_CYCLE:
                self._handle_schedule_cycle()
            elif event_type == MACHINE_SHUTDOWN:
                self._handle_shutdown(machine)

        for m in list(self.active_machines):
            self._shutdown_machine(m)

        print(f"--- Simulation Ended at Time {self.current_time} ---")
        print(f"Total Machines Uptime (Cost): {self.total_machine_uptime}\n")
                

    def _handle_schedule_cycle(self):
        if not self.pending_queue:
            self._schedule_next_cycle_if_needed()
            return

        # 1. Sort queue using SJR using est
        self.pending_queue.sort(key=lambda t: t.estimated_runtime)
        
        tasks_to_keep_in_queue = []
        
        for task in self.pending_queue:
            selected_machine = None
            
            # 2. Find available
            if self.policy == "first_fit":
                for m in self.active_machines:
                    if m.can_fit(task):
                        selected_machine = m
                        break
                        
            elif self.policy in ["best_fit", "cost_aware"]:
                best_score = float('inf')
                for m in self.active_machines:
                    if m.can_fit(task):
                        score = (m.available_cpu - task.cpu_req) + (m.available_mem - task.mem_req)
                        if score < best_score:
                            best_score = score
                            selected_machine = m
                            
            # 3. Tasks not fitted
            if not selected_machine:
                wait_cycles = getattr(task, 'wait_cycles', 0)
                
                if self.policy == "cost_aware" and wait_cycles < 3:
                    task.wait_cycles = wait_cycles + 1
                    tasks_to_keep_in_queue.append(task)
                    print(f"[Time {self.current_time:02d}] Task {task.task_id} DELAYED to save cost (Wait: {task.wait_cycles}).")
                    continue
                
                # Spin up new machine
                new_m = Machine(machine_id=len(self.active_machines) + 100, total_cpu=4.0, total_mem=16.0)
                new_m.power_on_time = self.current_time
                self.active_machines.append(new_m)
                selected_machine = new_m
                print(f"[Time {self.current_time:02d}] Provisioned NEW Machine {new_m.machine_id}")
                
            selected_machine.allocate(task)
            selected_machine.expected_shutdown_time = None
            task.start_time = self.current_time
            
            completion_time = self.current_time + task.actual_runtime
            self._push_event(completion_time, TASK_COMPLETION, task, selected_machine)
            print(f"[Time {self.current_time:02d}] Task {task.task_id} STARTED on Machine {selected_machine.machine_id} (Est: {task.estimated_runtime})")
            
        # Retain tasks that were delayed
        self.pending_queue = tasks_to_keep_in_queue
        self._schedule_next_cycle_if_needed()
 
    def _schedule_next_cycle_if_needed(self):
        # Stop the batch cycle only if the queue is empty AND all machines are idle
        has_active_tasks = any(len(m.active_tasks) > 0 for m in self.active_machines)
        if self.pending_queue or has_active_tasks or any(e[1] == TASK_ARRIVAL for e in self.event_queue):
            self._push_event(self.current_time + self.batch_window, SCHEDULE_CYCLE, None, None)
    def _handle_completion(self, task, machine):
        machine.available_cpu += task.cpu_req
        machine.available_mem += task.mem_req
        machine.active_tasks.remove(task)
        print(f"[Time {self.current_time:02d}] Task {task.task_id} COMPLETED on Machine {machine.machine_id}. Freed resources.")

        if len(machine.active_tasks) == 0:
            shutdown_time = self.current_time + self.idle_timeout
            machine.expected_shutdown_time = shutdown_time
            self._push_event(shutdown_time, MACHINE_SHUTDOWN, None, machine)
            print(f"[Time {self.current_time:02d}] Machine {machine.machine_id} is idle. Scheduled shutdown at {shutdown_time}.")

    def _handle_shutdown(self, machine):
        if len(machine.active_tasks) == 0 and machine.expected_shutdown_time == self.current_time:
            self._shutdown_machine(machine)
            
    def _shutdown_machine(self, machine):
        if machine in self.active_machines:
            self.active_machines.remove(machine)
            uptime = self.current_time - machine.power_on_time
            self.total_machine_uptime += uptime
            print(f"[Time {self.current_time:02d}] Machine {machine.machine_id} SHUT DOWN. Cost added: {uptime}")