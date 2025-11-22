🏥 ICU CPU Scheduling Simulator
Simulate and compare classic OS scheduling algorithms (FCFS, SJF, Priority, Round Robin) for real-time ICU monitoring tasks.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg(https://your-username-icu-cpu-scheduler.streamhttps://img.shields.io/badge/Python-3.10%

Project Overview
This project models how process scheduling affects patient outcomes in ICU systems, especially for vital-sign monitoring (ECG, BP, SpO₂). Different algorithms are tested for their clinical responsiveness and fairness.

Features
📊 Multiple algorithms: FCFS, SJF, Priority, Round Robin

🏥 Simulated ICU signals (ECG alerts, BP drops, cardiac arrest scenario)

⚡ Performance metrics (waiting/turnaround time, urgent response)

📈 Gantt chart visualizations, risk and starvation alerts

Quick Start

Clone repo:
git clone https://github.com/vnautiyal11/ICU_CPU_Scheduler.git
cd ICU_CPU_Scheduler

Install dependencies:
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

Run Simulator:
streamlit run app.py
