from models import Task
from simulator import Simulator

def test_scale_down():
    print("=== Testing Scale-Down Logic ===")
    
    # We set a batch window of 5 and an idle timeout of 5
    sim = Simulator(policy="first_fit", batch_window=5, idle_timeout=5)
    
    # Task A arrives at Time 0, takes 10 units of time. 
    # It should finish at Time 10. The machine should shut down 5 units later (Time 15).
    task_a = Task("A", submit_time=0, cpu_req=2.0, mem_req=4.0, actual_runtime=10, estimated_runtime=10)
    
    # Task B arrives at Time 25. 
    # Because Machine 1 shut down at Time 15, the simulator must provision Machine 2.
    task_b = Task("B", submit_time=25, cpu_req=2.0, mem_req=4.0, actual_runtime=5, estimated_runtime=5)

    sim.add_task(task_a)
    sim.add_task(task_b)
    
    sim.run()

if __name__ == "__main__":
    test_scale_down()