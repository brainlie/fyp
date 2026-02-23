import random
from models import Task

def create_task_with_error(task_id, submit_time, cpu_req, mem_req, actual_runtime, error_bound):
    if error_bound == 0.0:
        estimated_runtime = actual_runtime
    else:
        epsilon = random.uniform(-error_bound, error_bound)
        
        estimated_runtime = actual_runtime * (1 + epsilon)
    
    estimated_runtime = max(1.0, estimated_runtime)
    
    estimated_runtime = round(estimated_runtime, 2)
    
    return Task(
        task_id=task_id,
        submit_time=submit_time,
        cpu_req=cpu_req,
        mem_req=mem_req,
        actual_runtime=actual_runtime,
        estimated_runtime=estimated_runtime
    )