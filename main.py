from workload_generator import create_task_with_error

def test_uncertainty_model():
    print("--- Testing Runtime Uncertainty ---")
    
    actual_time = 100.0 # A job that takes exactly 100 units of time
    
    print(f"Ground Truth Actual Runtime: {actual_time}")
    
    # Perfect Information (0% error)
    task_perfect = create_task_with_error("T_0", 0, 1.0, 1.0, actual_time, error_bound=0.0)
    print(f"0% Error Bound:   Estimated = {task_perfect.estimated_runtime}")

    # Low Error (±10%)
    task_low = create_task_with_error("T_10", 0, 1.0, 1.0, actual_time, error_bound=0.10)
    print(f"10% Error Bound:  Estimated = {task_low.estimated_runtime}")

    # Medium Error (±25%)
    task_med = create_task_with_error("T_25", 0, 1.0, 1.0, actual_time, error_bound=0.25)
    print(f"25% Error Bound:  Estimated = {task_med.estimated_runtime}")
    
    # High Error (±50%)
    task_high = create_task_with_error("T_50", 0, 1.0, 1.0, actual_time, error_bound=0.50)
    print(f"50% Error Bound:  Estimated = {task_high.estimated_runtime}")

if __name__ == "__main__":
    test_uncertainty_model()