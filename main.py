from models import Task
from simulator import Simulator

def generate_test_tasks():
    return [
        Task("A", submit_time=0, cpu_req=2.0, mem_req=8.0, actual_runtime=10, estimated_runtime=10),
        Task("B", submit_time=1, cpu_req=2.0, mem_req=8.0, actual_runtime=15, estimated_runtime=15),
        Task("C", submit_time=2, cpu_req=1.0, mem_req=4.0, actual_runtime=5,  estimated_runtime=5),
        Task("D", submit_time=3, cpu_req=1.0, mem_req=4.0, actual_runtime=5,  estimated_runtime=5)
    ]

def test_algorithms():
    print("=== Testing First Fit ===")
    sim_ff = Simulator(policy="first_fit")
    for t in generate_test_tasks():
        sim_ff.add_task(t)
    sim_ff.run()

    print("=== Testing Best Fit ===")
    sim_bf = Simulator(policy="best_fit")
    for t in generate_test_tasks():
        sim_bf.add_task(t)
    sim_bf.run()

if __name__ == "__main__":
    test_algorithms()