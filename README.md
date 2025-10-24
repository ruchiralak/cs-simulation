
#EEX5362-Performance Modeling Simulation

# Medical Clinic Simulation
This Python program simulates the operations of a medical clinic using SimPy, a discrete-event simulation library. The simulation models :

         patient arrivals

         registration 

         doctor consultations to analyze clinic performance.

#Features
1.Simulates patient arrivals over a specified clinic working period (12 hours).

2.Models registration counters and doctors as resources with queueing.

3.Tracks key performance metrics:

    Average registration wait time

    Average doctor wait time

    Average total time in clinic

    Resource utilization (registration counters and doctors)

    Patient throughput (patients served per hour)

4.Supports multiple scenarios :
    such as adding more doctors/counters or simulating a busy day.

5.Generates visualizations:

     Waiting Times (Total wait, registration wait, doctor wait)

     Resource Utilization (registration, doctors, patient load %)

     Throughput (patients served per hour)

#Requirements

python 3+ version

Installed required libraries

    pip install simpy matplotlib numpy

#How to use

    Clone or download the project

    #Open and modify parameters as needed

    Sim_Time = 720  # 12 hours

    No_Patients = 400   # Number of Patients for a day

    No_Doctors = 4   # Number of doctors available

    Register_counters = 2  # Number of counters for registration

    Registration_Time = (4, 6)  # Registration time per patient

    Service_Time = (5, 10)  # Doctor consultation time per patient

Modify current scenario or add a scenario :

    scenarios = {
       #change values of num_reg, num_docs or num_patients

    "Main (2 reg, 4 doctors)": dict(num_reg=2, num_docs=4, num_patients=400),
    "Add Doctor & Counter (3 reg, 5 doctors)": dict(num_reg=3, num_docs=5, num_patients=400),
    "Busy Day (4 reg, 7 doctors, 600 pts)": dict(num_reg=4, num_docs=7, num_patients=600)    
  

     }

run the simulation

    python sim.py