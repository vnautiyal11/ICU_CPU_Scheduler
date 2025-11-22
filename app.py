import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np
from datetime import datetime
from typing import List, Dict

# ---------------------------
# 🌑 Dark Mode Only (High-Contrast ICU Theme)
# ---------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 1200px;
    }
    h1, h2, h3, h4 {
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        color: #f1f5f9 !important;
    }
    .stSidebar {
        background-color: #1e293b !important;
        color: #cbd5e1 !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        color: #93c5fd !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #94a3b8 !important;
    }
    .hovertext {
        font-family: monospace !important;
        background-color: #3b82f6 !important;
        color: white !important;
    }
    footer { visibility: hidden; }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 8px;
        font-size: 0.85rem;
        color: #94a3b8;
        border-top: 1px solid #334155;
        background: #1e293b;
    }
    .risk-box {
        background: #3f1212;
        border-left: 4px solid #ef4444;
        padding: 12px;
        border-radius: 6px;
        margin: 10px 0;
    }
    .use-case-box {
        background: #0c4a6e;
        border-left: 4px solid #38bdf8;
        padding: 12px;
        border-radius: 6px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 🧠 Backend Logic
# ---------------------------
from scheduler.algorithms import Process, fcfs, sjf_non_preemptive, priority_non_preemptive, round_robin
from scheduler.metrics import calculate_metrics, cpu_utilization, avg_waiting_time, avg_turnaround_time

# ---------------------------
# 🔐 Config & Data
# ---------------------------
APP_TITLE = "🏥 ICU CPU Scheduling Simulator"
APP_ICON = "⚕️"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path(__file__).parent / "data"
SCENARIOS: Dict[str, List[Process]] = {}

try:
    with open(DATA_DIR / "icu_scenarios.json", "r") as f:
        raw = json.load(f)
        for name, procs in raw.items():
            SCENARIOS[name] = [
                Process(p["pid"], p["arrival"], p["burst"], p["priority"]) for p in procs
            ]
except Exception as e:
    st.error(f"⚠️ Failed to load ICU scenarios: {e}. Using fallback.")
    SCENARIOS = {
        "Normal Monitoring": [
            Process("ECG-01", 0, 4, 3),
            Process("SpO₂-02", 1, 2, 4),
            Process("BP-03", 2, 3, 3)
        ],
        "Hypotension Alert": [
            Process("BP-ALERT", 0, 5, 1),
            Process("ECG-01", 1, 3, 2),
            Process("SpO₂-02", 2, 1, 3)
        ],
        "Code Blue (Cardiac Arrest)": [
            Process("ECG-EMERG", 0, 2, 1),
            Process("Defib-Check", 0, 1, 1),
            Process("Vent-Status", 1, 3, 2),
            Process("SpO2-Monitor", 2, 1, 3)
        ]
    }

ALGORITHM_INFO = {
    "FCFS": {
        "full": "First-Come, First-Served",
        "desc": "Simple, fair, but poor for urgent tasks.",
        "icon": "⏱️",
        "color": "#94a3b8"
    },
    "SJF (Non-Preemptive)": {
        "full": "Shortest Job First",
        "desc": "Minimizes average wait time; risks delaying emergencies.",
        "icon": "📏",
        "color": "#38bdf8"
    },
    "Priority (Non-Preemptive)": {
        "full": "Priority Scheduling",
        "desc": "Critical tasks (low priority number) execute first.",
        "icon": "⚠️",
        "color": "#f87171"
    },
    "Round Robin": {
        "full": "Round Robin",
        "desc": "Time-sliced fairness; ideal for mixed-criticality systems.",
        "icon": "🔄",
        "color": "#818cf8"
    }
}

# ---------------------------
# 🛠️ Sidebar: Professional Input
# ---------------------------
st.sidebar.title(f"{APP_ICON} ICU Scheduler")

mode = st.sidebar.radio(
    "Mode",
    ["🏥 ICU Scenario", "🛠️ Custom Tasks"],
    horizontal=True
)

processes: List[Process] = []

if mode == "🏥 ICU Scenario":
    scenario = st.sidebar.selectbox(
        "Clinical Scenario",
        list(SCENARIOS.keys()),
        format_func=lambda x: f"🩺 {x}"
    )
    processes = SCENARIOS[scenario]
    st.sidebar.info(f"**{len(processes)} tasks** loaded.")
else:
    st.sidebar.markdown("#### ➕ Define Tasks")
    n = st.sidebar.number_input("Tasks", min_value=1, max_value=10, value=3, step=1)
    custom_procs = []
    for i in range(n):
        with st.sidebar.expander(f"Task {i+1}", expanded=(i < 2)):
            pid = st.text_input("Task ID", value=f"TASK-{i+1:02d}", key=f"pid_{i}")
            arrival = st.number_input("Arrival (s)", min_value=0, value=0, key=f"arr_{i}")
            burst = st.number_input("Burst (s)", min_value=1, value=3, key=f"burst_{i}")
            priority = st.slider("Priority (1=Critical)", 1, 5, 3, key=f"prio_{i}")
            custom_procs.append(Process(pid, arrival, burst, priority))
    processes = custom_procs

# Algorithm & Quantum
st.sidebar.markdown("#### 🧠 Algorithm")
algorithm = st.sidebar.selectbox(
    "Algorithm",
    list(ALGORITHM_INFO.keys()),
    format_func=lambda x: f"{ALGORITHM_INFO[x]['icon']} {x}"
)

quantum = 2
if algorithm == "Round Robin":
    quantum = st.sidebar.slider("Time Quantum (s)", 1, 5, 2)

# Run control
st.sidebar.markdown("---")
run = st.sidebar.button("▶️ Run Simulation", type="primary", use_container_width=True)

if not run:
    st.title(APP_TITLE)
    st.markdown(
        """
        <div style="
            background-color:#1e293b; 
            color:#e2e8f0;
            padding:16px; 
            border-radius:10px; 
            border-left:4px solid #3b82f6; 
            margin-bottom:1.5rem;
        ">
        <strong>🩺 Clinical Context:</strong> In ICU monitoring, timely processing of ECG, BP, and SpO₂ is life-critical.  
        Select a scenario and algorithm to simulate real-time scheduling behavior.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

# ---------------------------
# ⚙️ Execution
# ---------------------------
with st.spinner("🔬 Running ICU simulation..."):
    try:
        proc_copy = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
        if algorithm == "Round Robin":
            gantt, result = round_robin(proc_copy, quantum)
        elif algorithm == "FCFS":
            gantt, result = fcfs(proc_copy)
        elif algorithm == "SJF (Non-Preemptive)":
            gantt, result = sjf_non_preemptive(proc_copy)
        elif algorithm == "Priority (Non-Preemptive)":
            gantt, result = priority_non_preemptive(proc_copy)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        calculate_metrics(result)
        cpu_util = cpu_utilization(result)
        avg_wt = avg_waiting_time(result)
        avg_tt = avg_turnaround_time(result)
    except Exception as e:
        st.error(f"🛠️ Simulation failed: {str(e)}")
        st.stop()

# ---------------------------
# 📊 Results
# ---------------------------
st.success(f"✅ Simulation complete using **{ALGORITHM_INFO[algorithm]['full']}**")

col1, col2, col3, col4 = st.columns(4)
col1.metric("CPU Util", f"{cpu_util:.1%}")
col2.metric("Avg Wait", f"{avg_wt:.2f}s")
col3.metric("Avg Turnaround", f"{avg_tt:.2f}s")
col4.metric("Tasks", len(result))

# Tabs — NO COMPARISON TAB
tab_summary, tab_gantt, tab_table, tab_insights = st.tabs([
    "📊 Summary", "⏱️ Gantt Chart", "📋 Metrics", "🩺 Clinical Insights"
])

# Tab 1: Summary
with tab_summary:
    st.subheader(f"{ALGORITHM_INFO[algorithm]['icon']} {ALGORITHM_INFO[algorithm]['full']}")
    st.info(f"**Key Trait**: {ALGORITHM_INFO[algorithm]['desc']}")
    
    # Performance Profile
    scores = {
        "FCFS": [4, 2, 5, 5],
        "SJF (Non-Preemptive)": [3, 3, 5, 4],
        "Priority (Non-Preemptive)": [2, 5, 4, 3],
        "Round Robin": [5, 4, 3, 5]
    }
    data = {
        "Metric": ["Fairness", "Urgent Response", "Throughput", "Implementation"],
        "Score": scores.get(algorithm, [0]*4)
    }
    fig = px.bar(data, x="Score", y="Metric", orientation='h', color="Score",
                 color_continuous_scale=["#f87171", "#fbbf24", "#3b82f6", "#10b981", "#0d9488"],
                 range_x=[0, 5.5], text="Score")
    fig.update_layout(showlegend=False, height=250, xaxis=dict(dtick=1))
    fig.update_traces(textposition="outside", marker_line_width=0.5)
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Gantt Chart (Task-Based Colors)
with tab_gantt:
    if gantt:
        gantt_df = pd.DataFrame(gantt, columns=["Task", "Start", "Finish"])
        gantt_df["Duration"] = gantt_df["Finish"] - gantt_df["Start"]
        
        # Assign unique color per task
        task_colors = {
            "ECG-01": "#3b82f6",      # Blue
            "SpO2-02": "#10b981",     # Green
            "BP-03": "#8b5cf6",       # Purple
            "BP-ALERT": "#ef4444",    # Red
            "ECG-EMERG": "#f59e0b",   # Amber
            "Defib-Check": "#ec4899", # Pink
            "Vent-Status": "#06b6d4", # Cyan
            "SpO2-Monitor": "#84cc16" # Lime
        }
        gantt_df["Color"] = gantt_df["Task"].map(lambda x: task_colors.get(x, "#6c757d"))
        
        fig = go.Figure()
        for _, row in gantt_df.iterrows():
            fig.add_trace(go.Bar(
                y=[row["Task"]],
                x=[row["Duration"]],
                base=[row["Start"]],
                orientation='h',
                name=row["Task"],
                hovertemplate=f"<b>{row['Task']}</b><br>Start: %{{base:.1f}}s<br>End: %{{x:.1f}}s",
                marker=dict(color=row["Color"], line=dict(width=1, color='#1e293b')),
                showlegend=False
            ))
        
        max_time = gantt_df["Finish"].max()
        fig.update_layout(
            title="⏱️ Execution Timeline",
            xaxis_title="Time (seconds)",
            yaxis_title="Task",
            height=max(350, len(gantt_df) * 50),
            xaxis=dict(range=[0, max(max_time * 1.05, 1)], gridcolor='#334155'),
            plot_bgcolor='#0f172a',
            paper_bgcolor='#1e293b',
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Task Colors**: " + " • ".join([
            f"<span style='color:{task_colors[t]}; font-weight:bold;'>{t}</span>" 
            for t in gantt_df["Task"].unique()
        ]), unsafe_allow_html=True)
    else:
        st.warning("No timeline generated.")

# Tab 3: Metrics Table
with tab_table:
    df = pd.DataFrame([{
        "Task ID": p.pid,
        "Arrival (s)": p.arrival,
        "Burst (s)": p.burst,
        "Priority": f"{p.priority}",
        "Waiting (s)": round(p.waiting_time, 2),
        "Turnaround (s)": round(p.turnaround_time, 2)
    } for p in result])
    
    def style_row(row):
        styles = [''] * len(row)
        if row["Waiting (s)"] > 0:
            styles[df.columns.get_loc("Waiting (s)")] = 'background-color: #3f1212; color: #fecaca;'
        return styles
    
    st.dataframe(
        df.style.apply(style_row, axis=1).format({"Waiting (s)": "{:.2f}", "Turnaround (s)": "{:.2f}"}),
        use_container_width=True
    )
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export CSV", csv, f"icu_{algorithm}_{datetime.now():%H%M}.csv", "text/csv")

# Tab 4: Clinical Insights (Expanded — Algorithm-Specific)
with tab_insights:
    st.subheader("🩺 Clinical Insights & Real-World Suitability")
    
    # Critical task analysis (scenario-specific)
    critical = [p for p in result if p.priority <= 2]
    if critical:
        max_wait = max(critical, key=lambda x: x.waiting_time)
        if max_wait.waiting_time > 2.0:
            st.error(f"⚠️ **High Risk**: Critical task `{max_wait.pid}` waited **{max_wait.waiting_time:.1f}s** — may delay life-saving intervention.")
        else:
            st.success(f"✅ **Safe**: Max critical wait = **{max_wait.waiting_time:.1f}s** < 2s threshold.")
    
    st.markdown("---")
    
    # Algorithm-Specific Clinical Guidance
    if algorithm == "FCFS":
        st.markdown("### ⏱️ **First-Come, First-Served (FCFS)**")
        st.markdown("""
        <div class="use-case-box">
        <strong>✅ Safe Use Cases:</strong><br>
        • Non-urgent telemetry review (e.g., retrospective ECG analysis)<br>
        • Batch processing of archived vitals<br>
        • Low-stakes monitoring (e.g., step-down unit with stable patients)
        </div>
        <div class="risk-box">
        <strong>❌ ICU Risk:</strong><br>
        • Emergent alerts (e.g., asystole, VTach) may be delayed by long-running prior tasks<br>
        • “Convoy effect”: One long task (e.g., 10s BP trend analysis) blocks all subsequent alerts<br>
        • <strong>Not IEC 62304 Class C compliant</strong> for life-support systems
        </div>
        """, unsafe_allow_html=True)
        
    elif algorithm == "SJF (Non-Preemptive)":
        st.markdown("### 📏 **Shortest Job First (SJF)**")
        st.markdown("""
        <div class="use-case-box">
        <strong>✅ Safe Use Cases:</strong><br>
        • High-throughput labs (e.g., processing short ECG snippets)<br>
        • Offline analytics where latency is non-critical<br>
        • Resource-constrained devices with predictable task lengths
        </div>
        <div class="risk-box">
        <strong>❌ ICU Risk:</strong><br>
        • Critical but long tasks (e.g., 5s defibrillator self-test) starve short emergencies<br>
        • Burst time estimation errors → mis-scheduling (e.g., ECG-EMERG predicted as 1s, actual 3s)<br>
        • <strong>Unacceptable for real-time medical devices</strong> (FDA guidance §5.2.3)
        </div>
        """, unsafe_allow_html=True)
        
    elif algorithm == "Priority (Non-Preemptive)":
        st.markdown("### ⚠️ **Priority Scheduling (Non-Preemptive)**")
        st.markdown("""
        <div class="use-case-box">
        <strong>✅ Safe Use Cases:</strong><br>
        • Mixed-priority monitoring (e.g., routine vitals + arrhythmia detection)<br>
        • Systems with hardware interrupts for true emergencies<br>
        • Pre-certified medical devices (e.g., Philips IntelliVue modules)
        </div>
        <div class="risk-box">
        <strong>⚠️ ICU Risk:</strong><br>
        • <strong>Non-preemptive = dangerous</strong>: Critical task arriving mid-burst (e.g., during 4s BP analysis) must wait<br>
        • Starvation of low-priority tasks (e.g., SpO₂ drops after 60s of no updates)<br>
        • <strong>Mitigation</strong>: Use <em>Preemptive Priority</em> or add aging
        </div>
        """, unsafe_allow_html=True)
        
    elif algorithm == "Round Robin":
        st.markdown("### 🔄 **Round Robin**")
        st.markdown("""
        <div class="use-case-box">
        <strong>✅ Safe Use Cases:</strong><br>
        • Multi-parameter monitors (ECG, SpO₂, BP, EtCO₂) with equal update needs<br>
        • Tele-ICU hubs handling multiple patients<br>
        • Systems where fairness > urgency (e.g., wellness tracking)
        </div>
        <div class="risk-box">
        <strong>⚠️ ICU Risk:</strong><br>
        • Large quantum (>1s) → critical tasks wait full slice before execution<br>
        • Context-switch overhead reduces CPU for analysis (↓ throughput)<br>
        • <strong>Only safe with quantum ≤1s</strong> and watchdog timer
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📚 Clinical Standards Reference")
    st.markdown("""
    | Standard | Requirement |
    |----------|-------------|
    | **IEC 62304** | Class C software (life-support) requires bounded response time |
    | **FDA Guidance (2022)** | Real-time systems must guarantee worst-case execution time (WCET) |
    | **ACLS Guidelines** | Arrhythmia detection → defibrillation in ≤90s; algorithmic delay must be ≤2s |
    """)

# ---------------------------
# 📝 Footer
# ---------------------------
st.markdown(
    """
    <div class="footer">
        ⚕️ ICU CPU Scheduling Simulator • Dark Mode • Academic Use Only • © 2025
    </div>
    """,
    unsafe_allow_html=True
)