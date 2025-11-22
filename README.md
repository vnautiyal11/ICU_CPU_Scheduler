🏥 ICU CPU Scheduling Simulator
A real-time OS scheduler simulator for critical-care monitoring systems—compare FCFS, SJF, Priority, and Round Robin in life-critical ICU scenarios.

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

assets/ — (Optional) images/screenshots

requirements.txt — Dependencies

README.md — This file