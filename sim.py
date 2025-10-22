import simpy
import random
import matplotlib.pyplot as plt
import networkx as nx

# Parameters
Random_Seed = 42
SIM_Time = 480  # 8 hours
Start_Time = 0  # OPD start at 8.00 am
NO_Patients = 400  # Average Patients count for a day
NO_Doctors = 4  # Number of doctors at clinic

# Process times
Registration_Time = 5  # 5 minutes per patient
Wait_Area_Time = 20  # 20 minutes in waiting area before doctor checkup
Service_Time = 10  # Checking time per patient
Registration_Counter = 2  # No of registration counters

# Random Arrival
Arrival_Time = 60  # To randomize the early arrival
Inter_Arrival = 2  # Inter arrival time

random.seed(Random_Seed)

# Statistic
Wait_Area_Time_Total = []
queue_length_registration = []
Queue_length_ServiceTime = []


# Patient Process

def patient(env, data, registration):
    # Random arrival, since patients are wait long before OPD Open
    arrival = random.uniform(Arrival_Time, SIM_Time / NO_Patients)
    yield env.timeout(max(0, arrival))
    arrival_time = env.now
    data['arrival'] += 1

    # Wait for starting OPD
    if env.now < Start_Time:
        yield env.timeout(Start_Time - env.now)

    # Registration period
    with registration.request() as req:
        queue_length_registration.append(len(registration.queue))
        yield req
        yield env.timeout(Registration_Time)


env = simpy.Environment()

registration = simpy.Resource(env, capacity=Registration_Counter)


env.run(until=SIM_Time)

print("\n--- Simulation Summary ---")
print(f'Total customers: {NO_Patients}')
print(f'Max queue length at registration desk: {max(queue_length_registration) if queue_length_registration else 0}')
