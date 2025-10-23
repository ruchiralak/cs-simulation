import numpy as np
import simpy
import random
import statistics

# =========================
# Parameters
# =========================
from matplotlib import pyplot as plt

RANDOM_SEED = 42
Sim_Time = 720  # 12 hours
No_Patients = 400   # Number of Patients for a day
No_Doctors = 4   # Number of doctors available
Register_counters = 2  # Number of counters for registration

Registration_Time = (4, 6)  # Registration time per patient
Service_Time = (10, 15)  # Doctor consultation time per patient


# Patient Process

def patient(env, name, registration, doctors, data):
    arrival = env.now
    data["arrivals"] += 1

    # Registration
    with registration.request() as req:
        yield req
        reg_wait = env.now - arrival
        data["reg_waits"].append(reg_wait)
        reg_time = random.uniform(*Registration_Time)
        data["reg_busy_time"] += reg_time
        yield env.timeout(reg_time)

    # Optional walking/waiting time
    yield env.timeout(random.uniform(2, 5))

    # Doctor consultation
    with doctors.request() as req:
        yield req
        doc_wait = env.now - arrival
        data["doctor_waits"].append(doc_wait)
        doc_time = random.uniform(*Service_Time)
        data["doctor_busy_time"] += doc_time
        yield env.timeout(doc_time)

    # Patient leaves
    total_time = env.now - arrival
    data["total_times"].append(total_time)
    data["served"] += 1


# setup arrival process

def setup(env, registration, doctors, num_patients, data):
    # inter_arrival time
    inter_arrival = Sim_Time / num_patients
    for i in range(num_patients):
        yield env.timeout(random.expovariate(1.0 / inter_arrival))
        env.process(patient(env, f"Patient {i + 1}", registration, doctors, data))


# Simulation

def sim(num_reg=Register_counters, num_docs=No_Doctors, num_patients=No_Patients):
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    registration = simpy.Resource(env, capacity=num_reg)
    doctors = simpy.Resource(env, capacity=num_docs)

    data = {
        "arrivals": 0,
        "served": 0,
        "reg_waits": [],
        "doctor_waits": [],
        "total_times": [],
        "reg_busy_time": 0,
        "doctor_busy_time": 0
    }

    env.process(setup(env, registration, doctors, num_patients, data))
    env.run(until=Sim_Time + 180)  # extra time for late patients

    # Metrics
    avg_reg_wait = statistics.mean(data["reg_waits"]) if data["reg_waits"] else 0
    avg_doc_wait = statistics.mean(data["doctor_waits"]) if data["doctor_waits"] else 0
    avg_total_time = statistics.mean(data["total_times"]) if data["total_times"] else 0

    throughput = (data["served"] / Sim_Time) * 60
    reg_util = (data["reg_busy_time"] / (num_reg * Sim_Time)) * 100
    doc_util = (data["doctor_busy_time"] / (num_docs * Sim_Time)) * 100

    return {
        "arrived": data["arrivals"],
        "served": data["served"],
        "avg_reg_wait": avg_reg_wait,
        "avg_doc_wait": avg_doc_wait,
        "avg_total_time": avg_total_time,
        "throughput": throughput,
        "reg_util": reg_util,
        "doc_util": doc_util
    }


# Scenarios

scenarios = {
    "Main (2 reg, 4 doctors)": dict(num_reg=2, num_docs=4, num_patients=400),
    "Add Doctor & Counter (3 reg, 5 doctors)": dict(num_reg=3, num_docs=5, num_patients=400),
    "Busy Day (4 reg, 7 doctors, 600 pts)": dict(num_reg=4, num_docs=7, num_patients=600)
}

print("=" * 60)
print("MEDICAL CLINIC SIMULATION - Performance Summary")
print("=" * 60)

results = {}
for name, params in scenarios.items():
    result = sim(**params)
    results[name] = result
    print(f"\nScenario: {name}")
    print(f"{'-' * 60}")
    print(f"Patients Arrived:        {result['arrived']}")
    print(f"Patients Served:         {result['served']}")
    print(f"Throughput:              {result['throughput']:.1f} patients/hour")
    print(f"Avg Registration Wait:   {result['avg_reg_wait']:.2f} minutes")
    print(f"Avg Doctor Wait:         {result['avg_doc_wait']:.2f} minutes")
    print(f"Avg Total Time:          {result['avg_total_time']:.2f} minutes")
    print(f"Registration Utilization:{result['reg_util']:.1f}%")
    print(f"Doctor Utilization:      {result['doc_util']:.1f}%")

# labels
labels = list(results.keys())
x = np.arange(len(labels))
width = 0.25

# patient load
max_patients = max(params["num_patients"] for params in scenarios.values())
patient_load = [params["num_patients"] / max_patients * 100 for params in scenarios.values()]

# 1: Waiting Time Bar Chart
total_waits = [results[l]["avg_total_time"] for l in labels]
reg_waits = [results[l]["avg_reg_wait"] for l in labels]
doc_waits = [results[l]["avg_doc_wait"] for l in labels]

plt.figure(figsize=(10, 5))
plt.bar(x - width, total_waits, width, label="Total Wait", color="blue")
plt.bar(x, reg_waits, width, label="Registration Wait", color="orange")
plt.bar(x + width, doc_waits, width, label="Doctor Wait", color="green")
plt.xticks(x, labels, rotation=15)
plt.ylabel("Time (minutes)")
plt.title("Waiting Times per Scenario")
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 2: Resource Utilization Bar Chart
reg_util = [results[l]["reg_util"] for l in labels]
doc_util = [results[l]["doc_util"] for l in labels]

plt.figure(figsize=(10, 5))
plt.bar(x - width, patient_load, width, label="Patient Load (%)", color="green")
plt.bar(x, reg_util, width, label="Registration Utilization (%)", color="blue")
plt.bar(x + width, doc_util, width, label="Doctor Utilization (%)", color="orange")
plt.xticks(x, labels, rotation=15)
plt.ylabel("Utilization / Patient Load (%)")
plt.title("Resource Utilization per Scenario")
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 3: Throughput Line Chart
throughputs = [results[l]["throughput"] for l in labels]

plt.figure(figsize=(8, 5))
plt.plot(labels, throughputs, marker='o', color="green")
plt.title("Throughput per Scenario (patients/hour)")
plt.xlabel("Scenario")
plt.ylabel("Throughput")
plt.grid(True)
plt.tight_layout()
plt.show()
