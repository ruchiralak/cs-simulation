import simpy
import random
import statistics
import matplotlib.pyplot as plt

#   Parameters
RANDOM_SEED = 42
SIM_TIME = 480  # simulation time (8 hours)
INTER_ARRIVAL_TIME = 2  # avg time between arrivals (minutes)
SERVICE_TIME = (3, 8)  # range of service time in minutes


# Customer Process
def customer(env, name, bank, wait_times, service_times, queue_lengths, teller_busy_time):
    arrival = env.now
    with bank.request() as req:
        yield req
        wait = env.now - arrival
        wait_times.append(wait)
        queue_lengths.append(len(bank.queue))

        # Record teller busy start
        start_service = env.now
        service_time = random.uniform(*SERVICE_TIME)
        service_times.append(service_time)
        yield env.timeout(service_time)
        teller_busy_time.append(service_time)


#  Customer setup
def setup(env, num_tellers, inter_arrival, wait_times, service_times, queue_lengths, teller_busy_time):
    bank = simpy.Resource(env, num_tellers)
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / inter_arrival))
        i += 1
        env.process(customer(env, f"Customer {i}", bank, wait_times, service_times, queue_lengths, teller_busy_time))


#  Run Simulation Function
def run_simulation(num_tellers):
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    wait_times, service_times, queue_lengths, teller_busy_time = [], [], [], []
    env.process(setup(env, num_tellers, INTER_ARRIVAL_TIME, wait_times, service_times, queue_lengths, teller_busy_time))
    env.run(until=SIM_TIME)

    total_customers = len(wait_times)
    avg_wait = statistics.mean(wait_times) if wait_times else 0
    avg_service = statistics.mean(service_times) if service_times else 0
    avg_queue = statistics.mean(queue_lengths) if queue_lengths else 0
    throughput = total_customers / (SIM_TIME / 60)  # customers per hour
    utilization = (sum(teller_busy_time) / (SIM_TIME * num_tellers)) * 100

    return {
        "tellers": num_tellers,
        "avg_wait": avg_wait,
        "avg_service": avg_service,
        "avg_queue": avg_queue,
        "throughput": throughput,
        "utilization": utilization,
        "total_customers": total_customers
    }


#  Run Experiments
teller_configs = [2, 3, 4, 5]
results = [run_simulation(t) for t in teller_configs]

# Extract Data for Visualization
tellers = [r["tellers"] for r in results]
avg_waits = [r["avg_wait"] for r in results]
throughputs = [r["throughput"] for r in results]
utilizations = [r["utilization"] for r in results]
avg_queues = [r["avg_queue"] for r in results]

#   Waiting Time
plt.figure(figsize=(8, 5))
plt.plot(tellers, avg_waits, marker='o', color='blue')
plt.title("Average Waiting Time vs Number of Tellers")
plt.xlabel("Number of Tellers")
plt.ylabel("Average Waiting Time (minutes)")
plt.grid(True)
plt.show()

#  Teller Utilization
plt.figure(figsize=(8, 5))
plt.bar(tellers, utilizations, color='orange')
plt.title("Teller Utilization (%) vs Number of Tellers")
plt.xlabel("Number of Tellers")
plt.ylabel("Utilization (%)")
plt.grid(True, axis='y')
plt.show()

#  Throughput
plt.figure(figsize=(8, 5))
plt.plot(tellers, throughputs, marker='s', color='green')
plt.title("Throughput (Customers/hour) vs Number of Tellers")
plt.xlabel("Number of Tellers")
plt.ylabel("Throughput (customers/hour)")
plt.grid(True)
plt.show()

# Detailed Performance Summary
print("="*60)
print("=== PERFORMANCE SUMMARY FOR ALL SCENARIOS ===")
print("="*60)
print(f"{'Tellers':<10} {'Avg Wait':<12} {'Avg Queue':<12} {'Utilization':<12} {'Throughput':<12}")
print("-"*60)

for r in results:
    print(f"{r['tellers']:<10} "
          f"{r['avg_wait']:<12.2f} "
          f"{r['avg_queue']:<12.2f} "
          f"{r['utilization']:<12.1f} "
          f"{r['throughput']:<12.2f}")
print("="*60)
