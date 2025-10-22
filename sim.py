import simpy
import random
import matplotlib.pyplot as plt
import networkx as nx
from simpy import resources

# Parameters


Random_Seed = 42
SIM_Time = 480  # 8 hours
Start_Time = 0  # OPD start at 8.00 am
NO_Patients = 400  # Average Patients count for a day
NO_Doctors = 4  # Number of doctors at clinic

# Process times
Registration_Counter = 2  # No of registration counters

# Registration time can be between
Registration_Time_Min = 4
Registration_Time_Max = 7  # Avg 5 minutes per patient, but can be differed

Wait_Area_Time_Min = 10
Wait_Area_Time_Max = 20  # 10 - 20 minutes in waiting area before doctor checkup

Service_Time_Min = 10
Service_Time_Max = 15  # Checking time per patient between 10 - 15 based on criteria

# Random Arrival
Arrival_Time = 60  # To randomize the early arrival
Inter_Arrival = 2  # Inter arrival time

random.seed(Random_Seed)

# Statistic
Wait_Area_Time_Total = []
queue_length_registration = []
Queue_length_ServiceTime = []


# Patient Process

def patient(env, data, lineUp, registration, wait, output):
    # 1.Random arrival, since patients are wait long before OPD Open
    arrival = random.uniform(Arrival_Time, SIM_Time / NO_Patients)
    yield env.timeout(max(0, arrival))

    arrival_time = env.now
    data['arrival'] += 1

    # 2.Wait for starting OPD
    if env.now < Start_Time:
        yield env.timeout(Start_Time - env.now)

    # 3.wait for registration after OPD started
    with lineUp.request() as req:
        yield req
        wait_for_reg = env.now - arrival_time

    # 3.Registration period
    with registration.request() as req:
        yield req
        queue_length_registration.append(len(registration.queue))

        yield env.timeout(random.uniform(Registration_Time_Min, Registration_Time_Max))
        Reg_Finished_Time = env.now

    #  4.Doctor Queue wait(Nurse Checking)
    with wait.request() as req:
        yield req
        wait_for_nurse = env.now - Reg_Finished_Time
        yield env.timeout(random.uniform(Wait_Area_Time_Min, Wait_Area_Time_Max))

        Wait_Finished_Time = env.now

    #  5.Doctor Check Queue
    with resources['doctor'].request() as req:
        yield req  # wait for a free doctor
        wait_for_doctor = env.now - wait_for_nurse

        # do the doctor checkup
        yield env.timeout(random.uniform(Service_Time_Min, Service_Time_Max))
    # 6.Exit the premises
    finish_time = env.now

    output['arrival'].append(arrival_time)
    output['wait_reg'].append(wait_for_reg)
    output['wait_for_nurse'].append(wait_for_nurse)
    output['wait_doctor'].append(wait_for_doctor)
    output['total_time'].append(finish_time - arrival_time)
    output['throughput'] += 1  # count this patient as processed

    #  Generate new patients


def patients(env, output, arrival ):
     patient_id = 0
     while True:
         yield env.timeout(random.expovariate(1.0/arrival))
         patient_id += 1
         #create a new patient
         env.process(new_patient(env,f'Patient {patient_id}',output))
    # Simpy Environment
    env = simpy.Environment()
    registration = simpy.Resource(env, capacity=Registration_Counter)
    env.run(until=SIM_Time)


print("\n--- Simulation Summary ---")
print(f'Total customers: {NO_Patients}')
print(f'Max queue length at registration desk: {max(queue_length_registration) if queue_length_registration else 0}')
