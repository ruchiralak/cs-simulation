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
Wait_Area_Time = 20   # 20 minutes in waiting area before doctor checkup
Service_Time = 10  # Cheking time per patient

# Random Arrival
Arrival_Time = 60  # To randomize the early arrival
Inter_Arrival = 2  # Inter arrival time


