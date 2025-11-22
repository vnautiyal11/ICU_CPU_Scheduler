🏥 ICU CPU Scheduling Simulator
A real-time OS scheduler simulator for critical-care monitoring systems—compare FCFS, SJF, Priority, and Round Robin in life-critical ICU scenarios.

Link:https://icucpuscheduler-nung657nguo9h4qfyzgnk6.streamlit.app/

Project Overview
This project models how process scheduling affects patient outcomes in ICU systems, especially for vital-sign monitoring (ECG, BP, SpO₂). Different algorithms are tested for their clinical responsiveness and fairness.

Key Features
4 Scheduling Algorithms: FCFS, SJF (Non-Preemptive), Priority (Non-Preemptive), Round Robin (configurable quantum)

Clinical Scenario Simulation: Routine monitoring, hypotension alert, and cardiac arrest simulations

Visual Analytics: Gantt charts, risk-highlighted waiting times, algorithm performance profiling

Risk Assessment: Alerts for tasks waiting >2s, starvation warnings, and clinical compliance notes

Quick Start
Clone repo:

bash
git clone https://github.com/vnautiyal11/ICU_CPU_Scheduler.git
cd ICU_CPU_Scheduler
Install dependencies:

bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
Run Simulator:

bash
streamlit run app.py
Project Structure
app.py — Main Streamlit app

scheduler/ — Algorithms and metrics

data/icu_scenarios.json — ICU workload configs
<img width="1374" height="522" alt="Screenshot 2025-11-22 220312" src="https://github.com/user-attachments/assets/76e5ccdf-4246-4d4e-b013-ceed112e8a0a" />
<img width="1919" height="874" alt="Screenshot 2025-11-22 220252" src="https://github.com/user-attachments/assets/353944e1-1b08-4331-9824-1f22cfabfc4f" />

<img width="1918" height="762" alt="image" src="https://github.com/user-attachments/assets/9cd9740b-5731-4b69-ad7e-3295f2239fb9" />



requirements.txt — Dependencies

README.md — This file
