import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# --- UI SETTINGS ---
st.set_page_config(page_title="Pharma Research Simulator Pro", layout="wide", page_icon="🧬")

# Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 8px; background-color: #007bff; color: white; font-weight: bold; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #eee; }
    .explanation-box { background-color: #e9ecef; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Pharmaceutical Research Simulator Pro")

# --- INITIALIZE SESSION STATE ---
if 'selected_energy' not in st.session_state:
    st.session_state.selected_energy = -7.0
if 'selected_drug' not in st.session_state:
    st.session_state.selected_drug = "Experimental Lead"
if 'selected_target' not in st.session_state:
    st.session_state.selected_target = "COX2"
if 'selected_tox' not in st.session_state:
    st.session_state.selected_tox = 15.0

# --- DATABASE ---
drug_list = ["Aspirin","Ibuprofen","Metformin","Atorvastatin","Amlodipine","Omeprazole","Sertraline","Paracetamol","Diclofenac","Naproxen"]
protein_categories = {
    "COX2": "Enzyme", "AKT1": "Kinase", "EGFR": "Receptor", 
    "STAT3": "Transcription Factor", "TNF": "Cytokine", "VEGFA": "Growth Factor",
    "PI3K": "Enzyme", "mTOR": "Enzyme", "JAK2": "Kinase", "NFkB": "Transcription Factor"
}
protein_list = list(protein_categories.keys())

# --- SIDEBAR ---
module = st.sidebar.selectbox("Select Simulator Module", 
    ["Virtual Drug Screening", "Dose Response Simulator", "Protein Pathway Simulator", "Network Pharmacology Explorer", "Molecular Docking Simulator"])

# -------------------------------------------------
# 1. VIRTUAL DRUG SCREENING
# -------------------------------------------------
if module == "Virtual Drug Screening":
    st.header("🧪 Step 1: High-Throughput Screening")
    
    if st.button("🚀 Run New Screen"):
        results = []
        for d in random.sample(drug_list, 8):
            target = random.choice(protein_list)
            energy = round(random.uniform(-11.0, -4.0), 2)
            tox = round(random.uniform(5.0, 85.0), 1) 
            # Lipinski simple check
            logp = round(random.uniform(1.0, 6.0), 1)
            results.append([d, target, energy, tox, logp])
        st.session_state.screening_results = pd.DataFrame(results, columns=["Drug", "Target", "Energy", "Toxicity (%)", "LogP"])

    if 'screening_results' in st.session_state:
        st.dataframe(st.session_state.screening_results.style.background_gradient(subset=['Toxicity (%)'], cmap='RdYlGn_r'))
        
        selection = st.selectbox("Select a Lead to Link:", st.session_state.screening_results['Drug'])
        if st.button("Link Lead to Pipeline"):
            row = st.session_state.screening_results[st.session_state.screening_results['Drug'] == selection].iloc[0]
            st.session_state.selected_drug = row['Drug']
            st.session_state.selected_energy = row['Energy']
            st.session_state.selected_target = row['Target']
            st.session_state.selected_tox = row['Toxicity (%)']
            st.success(f"Linked {selection}!")

    st.markdown("---")
    st.subheader("📖 Parameter Definitions")
    colA, colB = st.columns(2)
    with colA:
        st.write("**Binding Energy (kcal/mol):** Measures the stability of the drug-protein complex. A **more negative** value means the drug sticks better to the target.")
        st.write("**Toxicity (%):** Predictive score of cellular damage. High toxicity often leads to clinical trial failure.")
    with colB:
        st.write("**LogP (Lipophilicity):** Measures how 'oily' a drug is. Ideally between 1 and 5. If it's too high, the drug won't dissolve in blood; if too low, it can't cross cell membranes.")

# -------------------------------------------------
# 2. DOSE RESPONSE SIMULATOR
# -------------------------------------------------
elif module == "Dose Response Simulator":
    st.header("📈 Advanced Pharmacodynamics Model")
    
    target = st.session_state.selected_target
    energy = st.session_state.selected_energy
    tox_val = st.session_state.selected_tox
    p_type = protein_categories.get(target, "Enzyme")
    
    calc_ec50 = np.interp(energy, [-12, -4], [0.5, 200])
    calc_emax = np.interp(energy, [-12, -4], [100, 45])
    auto_hill = 2.5 if p_type in ["Receptor", "Transcription Factor"] else 1.2

    col1, col2, col3 = st.columns(3)
    col1.metric("EC50 (Potency)", f"{round(calc_ec50, 1)} nM")
    col2.metric("Emax (Efficacy)", f"{round(calc_emax)}%")
    col3.metric("Safety Limit", f"{tox_val}%")

    conc = np.logspace(-1, 4, 100)
    response = (calc_emax * (conc**auto_hill)) / ( (calc_ec50**auto_hill) + (conc**auto_hill) )
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=conc, y=response, line=dict(color='#00CC96', width=4), name='Predicted Response'))
    fig.add_hline(y=tox_val, line_dash="dot", line_color="red", annotation_text="Toxicity Threshold")

    fig.update_layout(xaxis_type="log", yaxis_title="Effect %", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="explanation-box">', unsafe_allow_html=True)
    st.write(f"### 🧪 Analysis for {st.session_state.selected_drug}")
    st.write(f"**EC50:** This is the concentration required to reach 50% effect. Since your drug has an energy of {energy}, it is quite potent.")
    st.write(f"**Hill Coefficient ({auto_hill}):** Since {target} is a {p_type}, we used a slope of {auto_hill}. This describes how steeply the drug's effect increases as you add more dose.")
    st.write(f"**Therapeutic Window:** If the green curve stays below the red dotted line (**{tox_val}%**), the drug is safe to use at that dose.")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# 3. PROTEIN PATHWAY SIMULATOR
# -------------------------------------------------
elif module == "Protein Pathway Simulator":
    st.header("⚡ Pathway Impact Analysis")
    energy = st.session_state.selected_energy
    target = st.session_state.selected_target
    inhibition = np.interp(energy, [-12, -4], [100, 20])
    p_type = protein_categories.get(target, "Enzyme")
    depth = 5 if p_type in ["Receptor", "Transcription Factor"] else 3

    steps = [f"Step {i+1}" for i in range(depth)]
    signal = [inhibition * (0.8**i) for i in range(depth)]
    st.plotly_chart(go.Figure(go.Bar(x=steps, y=signal, marker_color='firebrick')), use_container_width=True)

    net = Network(height="400px", width="100%", bgcolor="#ffffff", directed=True)
    chain = [target] + random.sample([p for p in protein_list if p != target], depth - 1)
    for i in range(len(chain)):
        s_val = inhibition * (0.8**i)
        net.add_node(chain[i], label=f"{chain[i]}\n{round(s_val)}%", color="#ff4b4b" if i==0 else "#1c83e1")
        if i > 0: net.add_edge(chain[i-1], chain[i], width=3)
    
    net.save_graph("map.html")
    with open("map.html", 'r') as f: components.html(f.read(), height=400)

    st.markdown('<div class="explanation-box">', unsafe_allow_html=True)
    st.write("### 🔗 Why does the signal drop?")
    st.write(f"This represents **Signal Transduction**. When {st.session_state.selected_drug} blocks **{target}**, the message to the rest of the cell is weakened.")
    st.write(f"**The 20% Rule:** Every step in the chain loses 20% efficiency. If the pathway is too long (like in Receptors), the drug might not have enough power to reach the final goal.")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# 4. NETWORK & 5. DOCKING (SIMPLIFIED FOR SPACE)
# -------------------------------------------------
elif module == "Network Pharmacology Explorer":
    st.header("🕸️ Network Explorer")
    st.write("Shows how one drug hits multiple targets, causing both 'Therapeutic Effects' and 'Side Effects'.")
    # Network code here...

elif module == "Molecular Docking Simulator":
    st.header("🧩 Docking Simulator")
    st.write(f"Detailed view of **{st.session_state.selected_drug}** fitting into the pocket of **{st.session_state.selected_target}**.")
    # Docking code here...
