import simpy
import random
import statistics
import matplotlib.pyplot as plt

#  Parameters
Random_Seed = 42
SIM_Time = 480  # 8 hours
Start_Time = 0  # OPD start at 8.00 am
NO_Patients = 400  # Average Patients count for a day
NO_Doctors = 4  # Number of doctors at clinic

# Process times
Registration_Counter = 2  # No of registration counters

# Registration time can be between

Registration_Time = (4, 7)  # Avg 5 minutes per patient, but can be differed

Service_Time = (10, 15)  # Checking time per patient between 10 - 15 based on criteria

# Random Arrival
Inter_Arrival = 1.2  # Sim time / No patients
random.seed(Random_Seed)


#  Patient Process
def patient(env, name, clinic, wait_times, register_times, service_times, queue_length, counter_busy_time,
            doctor_busy_time):
    arrival = env.now
    with clinic.request() as req:
        yield req
        wait = env.now - arrival
        wait_times.append(wait)
        queue_length.append(len(clinic.queue))

        # record registering process
        start_register = env.now
        registration_time = random.uniform(*Registration_Time)
        register_times.append(registration_time)
        yield env.timeout(registration_time)
        counter_busy_time.append(registration_time)

        # Patient checking time
        start_service = env.now
        service_time = random.uniform(*Service_Time)
        service_times.append(service_time)
        yield env.timeout(service_time)
        doctor_busy_time.append(service_time)


# Patient Generate
def setup(env, num_doctors, inter_arrivals, wait_times, register_times, service_times, queue_lengths, counter_busy_time,
          doctor_busy_time):
    clinic = simpy.Resource(env, capacity=num_doctors)
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / inter_arrivals))
        i += 1
        env.process(patient(env, f"Patient {i}", clinic, wait_times, register_times, service_times, queue_lengths,
                            counter_busy_time, doctor_busy_time))


# Simulation
env = simpy.Environment()
wait_times, register_times, service_times, queue_lengths, counter_busy_time, doctor_busy_time = [], [], [], [], [], []
env.process(setup(
    env,
    NO_Doctors,
    Inter_Arrival,
    wait_times,
    Registration_Time,
    Service_Time,
    queue_lengths,
    counter_busy_time,
    doctor_busy_time,
))

