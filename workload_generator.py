import random
from models import Task

def create_task_with_error(task_id, submit_time, cpu_req, mem_req, actual_runtime, error_bound):
    """
    Creates a Task object with an estimated runtime based on the error_bound.
    
    Parameters:
    - error_bound (float): The maximum percentage error. For 25% error, pass 0.25.
                           If 0, perfect information is used.
    """
    if error_bound == 0.0:
        estimated_runtime = actual_runtime
    else:
        # Generate a random error (epsilon) between -error_bound and +error_bound
        epsilon = random.uniform(-error_bound, error_bound)
        
        # Apply the error
        estimated_runtime = actual_runtime * (1 + epsilon)
    
    # Ensure the scheduler never gets a zero or negative estimated time
    estimated_runtime = max(1.0, estimated_runtime)
    
    # We round to 2 decimal places to simulate standard reporting metrics
    estimated_runtime = round(estimated_runtime, 2)
    
    return Task(
        task_id=task_id,
        submit_time=submit_time,
        cpu_req=cpu_req,
        mem_req=mem_req,
        actual_runtime=actual_runtime,
        estimated_runtime=estimated_runtime
    )