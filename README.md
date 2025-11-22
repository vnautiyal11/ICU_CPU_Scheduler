# 🏥 ICU CPU Scheduling Simulator

> A real-time OS scheduler simulator for critical-care monitoring systems — comparing FCFS, SJF, Priority, and Round Robin in life-critical ICU scenarios.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-username-icu-cpu-scheduler.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)

---

## 🎯 Project Overview

This simulator models how operating system scheduling algorithms impact **response latency in ICU patient monitoring**, where timely processing of ECG, BP, and SpO₂ data can be life-saving.

### Real-World Analogy: ICU Monitoring System
| OS Concept          | ICU Equivalent                     |
|---------------------|------------------------------------|
| Process             | Vital sign analysis task (e.g., ECG arrhythmia detection) |
| CPU Burst Time      | Time to analyze sensor data (e.g., 2s for ECG waveform) |
| Priority            | Clinical urgency (1 = cardiac arrest, 5 = routine check) |
| Preemption          | Interrupting low-priority task for emergent alert |

---

## 🔬 Key Features

✅ **4 Scheduling Algorithms**  
- First-Come, First-Served (FCFS)  
- Shortest Job First (SJF, Non-Preemptive)  
- Priority Scheduling (Non-Preemptive)  
- Round Robin (configurable quantum)

✅ **Clinical Scenario Simulation**  
- `Normal Monitoring`: Routine vitals  
- `Hypotension Alert`: BP drop detection  
- `Code Blue (Cardiac Arrest)`: Asystole + defibrillator check

✅ **Professional Visual Analytics**  
- Interactive Gantt charts (task-based coloring)  
- Metrics table with risk-highlighted waiting times  
- Algorithm performance profiling (Fairness, Urgent Response, etc.)

✅ **Clinical Risk Assessment**  
- Alerts if critical tasks wait >2s (per ACLS guidelines)  
- Starvation warnings for low-priority tasks  
- IEC 62304/FDA compliance notes per algorithm

---

## 🖥️ Live Demo

👉 **[Try the Simulator](https://your-username-icu-cpu-scheduler.streamlit.app)**

![Demo Screenshot](assets/demo-screenshot.png)  
*(Add a screenshot later and place in `assets/demo-screenshot.png`)*

---

## 📁 Project Structure
OS project/
├── app.py # Main Streamlit application
├── scheduler/
│ ├── algorithms.py # FCFS, SJF, Priority, Round Robin
│ └── metrics.py # Waiting time, turnaround, CPU util
├── data/
│ └── icu_scenarios.json # Predefined ICU workloads
├── assets/ # (Optional) Screenshots, logos
├── requirements.txt # Dependencies
└── README.md # This file

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- Git (for updates)

### Installation
```bash
# Clone repository (if not done)
git clone https://github.com/vnautiyal11/icu-cpu-scheduler.git
cd icu-cpu-scheduler

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows CMD

# Install dependencies
pip install -r requirements.txt

# Run the simulator
streamlit run app.py