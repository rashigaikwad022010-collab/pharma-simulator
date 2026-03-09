import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
from pyvis.network import Network
import streamlit.components.v1 as components

# --- UI SETTINGS ---
st.set_page_config(page_title="Universal Pharma Simulator", layout="wide", page_icon="🧬")

# Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 8px; background-color: #007bff; color: white; font-weight: bold; }
    .explanation-box { background-color: #f1f3f5; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Universal Pharmaceutical Research Pipeline")

# --- EXPANDED DATABASE ---
drug_db = {
    "Statins (Cholesterol)": ["Atorvastatin", "Simvastatin", "Rosuvastatin"],
    "Antihistamines (Allergy)": ["Loratadine", "Cetirizine", "Diphenhydramine"],
    "NSAIDs (Pain/Inflam)": ["Aspirin", "Ibuprofen", "Naproxen"],
    "Antipsychotics/Mood": ["Quetiapine", "Sertraline", "Risperidone"],
    "Antidiabetics": ["Metformin", "Glipizide"],
}

protein_categories = {
    "CASP3": "Enzyme (Apoptosis/Cell Death)", 
    "H1-Receptor": "Receptor (Allergy Response)", 
    "HMG-CoA": "Enzyme (Cholesterol Production)",
    "COX2": "Enzyme (Pain/Inflammation)", 
    "EGFR": "Receptor (Cancer/Growth)", 
}

all_drugs = [item for sublist in drug_db.values() for item in sublist]
all_proteins = list(protein_categories.keys())

# --- INITIALIZE SESSION STATE ---
if 'selected_energy' not in st.session_state: st.session_state.selected_energy = -7.5
if 'selected_drug' not in st.session_state: st.session_state.selected_drug = "Atorvastatin"
if 'selected_target' not in st.session_state: st.session_state.selected_target = "CASP3"
if 'selected_tox' not in st.session_state: st.session_state.selected_tox = 15.0

# --- SIDEBAR & MANUAL CONTROL ---
st.sidebar.header("🕹️ Manual Research Controls")
st.session_state.selected_drug = st.sidebar.selectbox("Choose Drug:", all_drugs, index=all_drugs.index(st.session_state.selected_drug))
st.session_state.selected_target = st.sidebar.selectbox("Choose Target:", all_proteins, index=all_proteins.index(st.session_state.selected_target))
st.session_state.selected_energy = st.sidebar.slider("Binding Energy (kcal/mol)", -11.5, -4.0, st.session_state.selected_energy)
st.session_state.selected_tox = st.sidebar.slider("Toxicity Threshold (%)", 5.0, 90.0, st.session_state.selected_tox)

module = st.sidebar.selectbox("Select Simulator Module", 
    ["Virtual Drug Screening", "Dose Response Simulator", "Protein Pathway Simulator", "Network Pharmacology Explorer", "Molecular Docking Simulator"])

# -------------------------------------------------
# 1. VIRTUAL DRUG SCREENING
# -------------------------------------------------
if module == "Virtual Drug Screening":
    st.header("🧪 Step 1: High-Throughput Screening")
    if st.button("🚀 Run Screen on Global Library"):
        results = [[d, random.choice(all_proteins), round(random.uniform(-11, -4), 2), round(random.uniform(5, 85), 1)] for d in all_drugs]
        st.session_state.screening_results = pd.DataFrame(results, columns=["Drug", "Target", "Energy", "Toxicity (%)"])
    
    if 'screening_results' in st.session_state:
        st.dataframe(st.session_state.screening_results.style.background_gradient(subset=['Toxicity (%)'], cmap='RdYlGn_r'), use_container_width=True)

# -------------------------------------------------
# 2. DOSE RESPONSE SIMULATOR
# -------------------------------------------------
elif module == "Dose Response Simulator":
    st.header(f"📈 Dose-Response: {st.session_state.selected_drug}")
    ec50 = np.interp(st.session_state.selected_energy, [-12, -4], [0.5, 200])
    conc = np.logspace(-1, 4, 100)
    response = (100 * (conc**1.2)) / ( (ec50**1.2) + (conc**1.2) )
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=conc, y=response, line=dict(color='#00CC96', width=4)))
    fig.add_hline(y=st.session_state.selected_tox, line_dash="dot", line_color="red")
    fig.update_layout(xaxis_type="log", title="Dose-Response Curve", yaxis_title="Effect %", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"### 📋 Graph Explanation: This is a **Sigmoid Curve**. It shows that {st.session_state.selected_drug} becomes more effective as the dose increases until it hits a plateau. The red line is your safety limit.")
    

# -------------------------------------------------
# 3. PROTEIN PATHWAY SIMULATOR
# -------------------------------------------------
elif module == "Protein Pathway Simulator":
    st.header(f"⚡ Pathway Analysis: {st.session_state.selected_target}")
    inhibition = np.interp(st.session_state.selected_energy, [-12, -4], [95, 20])
    steps = [st.session_state.selected_target, "Signal Relay", "Kinase Activation", "Transcription", "Cell Response"]
    signal = [inhibition * (0.8**i) for i in range(len(steps))]
    
    st.plotly_chart(go.Figure(go.Bar(x=steps, y=signal, marker_color='firebrick')), use_container_width=True)
    st.info("### 📉 Bar Chart Explanation: This shows **Signal Attenuation**. Each bar is a protein in a chain. The drug hits the first protein, and the 'power' of that message fades as it moves through the cell.")
    
    net = Network(height="400px", width="100%", bgcolor="#ffffff", directed=True)
    for i in range(len(steps)):
        net.add_node(steps[i], label=f"{steps[i]}\n{round(signal[i])}%", color="#ff4b4b" if i==0 else "#1c83e1")
        if i > 0: net.add_edge(steps[i-1], steps[i])
    net.save_graph("pathway.html")
    with open("pathway.html", 'r') as f: components.html(f.read(), height=450)
    st.info("### 🕸️ Flowchart Explanation: This is a **Signaling Cascade**. It maps how blocking the first protein (Red) ripples through the cell's internal communication network.")
    

# -------------------------------------------------
# 4. NETWORK PHARMACOLOGY
# -------------------------------------------------
elif module == "Network Pharmacology Explorer":
    st.header(f"🕸️ Polypharmacology of {st.session_state.selected_drug}")
    net = Network(height="500px", width="100%", bgcolor="#ffffff")
    net.add_node(st.session_state.selected_drug, label=st.session_state.selected_drug, color="#ff4b4b", size=30)
    for t in random.sample(all_proteins, 4):
        net.add_node(t, label=t, color="#1c83e1")
        net.add_edge(st.session_state.selected_drug, t)
    net.save_graph("network.html")
    with open("network.html", 'r') as f: components.html(f.read(), height=550)
    st.info("### 🕸️ Diagram Explanation: This shows that drugs aren't perfect. While targeting one protein, they often 'stick' to others, which can cause side effects or hidden benefits.")

# -------------------------------------------------
# 5. MOLECULAR DOCKING (THE ADDED PORTION)
# -------------------------------------------------
elif module == "Molecular Docking Simulator":
    st.header("🧩 Molecular Docking Analysis")
    st.write(f"Analyzing the geometric fit: **{st.session_state.selected_drug}** into the binding pocket of **{st.session_state.selected_target}**.")
    
    poses = [[i, round(st.session_state.selected_energy + random.uniform(-0.5, 0.5), 2), random.choice(["H-Bond", "Hydrophobic", "Ionic"])] for i in range(1, 6)]
    df_dock = pd.DataFrame(poses, columns=["Pose ID", "Binding Affinity (kcal/mol)", "Primary Interaction"])
    st.table(df_dock)
    
    st.info(f"### 🧩 Results Explanation: This table shows the **Thermodynamic Stability** of the drug inside the protein. **Pose 1** is the most stable. A more negative 'kcal/mol' value means the drug and protein fit together like a perfect lock and key.")
