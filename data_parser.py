import pandas as pd
from workload_generator import create_task_with_error

def load_google_trace(file_path, error_bound=0.0, max_tasks=5000):
    """
    Parses a Google Cluster Trace CSV, cleans it, and converts it into simulator Tasks.
    """
    print(f"Loading Google Trace data from {file_path}...")
    
    # 1. Read the dataset
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}.")
        return []

    initial_count = len(df)
    
    # 2. Standardize Column Names (Adjust these if your specific CSV differs slightly)
    # Assuming columns like: task_id, submit_time, start_time, end_time, cpu_req, mem_req
    required_cols = ['task_id', 'submit_time', 'start_time', 'end_time', 'cpu_req', 'mem_req']
    if not all(col in df.columns for col in required_cols):
        print("Warning: CSV is missing standard columns. Attempting to map...")
        # Add custom column mapping here if you download a differently formatted Kaggle subset

    # 3. Clean the Data: Drop rows with missing timestamps or zero resource requests
    df = df.dropna(subset=['start_time', 'end_time', 'cpu_req', 'mem_req'])
    df = df[(df['cpu_req'] > 0) & (df['mem_req'] > 0)]

    # 4. Calculate Ground Truth (Actual Runtime)
    # Google traces often use microseconds. We divide by 1,000,000 to get seconds.
    # (If your CSV is already in seconds, remove the division)
    df['submit_time'] = df['submit_time'] / 1e6
    df['actual_runtime'] = (df['end_time'] - df['start_time']) / 1e6

    # Filter out impossible physics (zero/negative time) and massive outliers (e.g., > 24 hours)
    df = df[(df['actual_runtime'] > 0) & (df['actual_runtime'] < 86400)]

    # 5. Scale Resources
    # Google normalizes CPU/Mem requests from 0.0 to 1.0 (1.0 being the largest machine in their cluster).
    # Since our simulator machines have 4.0 CPU and 16.0 Mem, we scale Google's fractions up to our limits.
    df['cpu_req'] = df['cpu_req'] * 4.0
    df['mem_req'] = df['mem_req'] * 16.0

    # 6. Sort Chronologically
    df = df.sort_values(by='submit_time')
    
    final_count = len(df)
    print(f"Data Cleaned. Filtered out {initial_count - final_count} invalid tasks.")
    print(f"Extracting {min(final_count, max_tasks)} tasks for simulation...\n")
    
    # 7. Generate Error-Injected Task Objects
    tasks = []
    for index, row in df.head(max_tasks).iterrows():
        task = create_task_with_error(
            task_id=f"G_{int(row['task_id'])}",
            submit_time=round(row['submit_time'], 2),
            cpu_req=round(row['cpu_req'], 3),
            mem_req=round(row['mem_req'], 3),
            actual_runtime=round(row['actual_runtime'], 2),
            error_bound=error_bound
        )
        tasks.append(task)
        
    return tasks

if __name__ == "__main__":
    # Test the parser with a 25% error bound
    # Make sure you have a 'google_trace_subset.csv' in your folder!
    tasks = load_google_trace('google_trace_subset.csv', error_bound=0.25, max_tasks=5)
    for t in tasks:
        print(t)