import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# --- UI SETTINGS ---
st.set_page_config(page_title="Pharma Research Simulator Pro", layout="wide", page_icon="🧬")

# Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 8px; background-color: #007bff; color: white; font-weight: bold; }
    .explanation-box { background-color: #f1f3f5; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin: 15px 0; }
    .description-text { font-size: 14px; color: #444; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Integrated Pharmaceutical Research Pipeline")

# --- INITIALIZE SESSION STATE ---
# This ensures that even if you don't run a screen, the other pages have data.
if 'selected_energy' not in st.session_state:
    st.session_state.selected_energy = -7.5
if 'selected_drug' not in st.session_state:
    st.session_state.selected_drug = "Lead-001"
if 'selected_target' not in st.session_state:
    st.session_state.selected_target = "EGFR"
if 'selected_tox' not in st.session_state:
    st.session_state.selected_tox = 18.0

# --- DATABASE ---
protein_categories = {
    "COX2": "Enzyme", "AKT1": "Kinase", "EGFR": "Receptor", 
    "STAT3": "Transcription Factor", "TNF": "Cytokine", "VEGFA": "Growth Factor"
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
        for i in range(8):
            d = f"Compound-{100+i}"
            target = random.choice(protein_list)
            energy = round(random.uniform(-11.0, -4.0), 2)
            tox = round(random.uniform(5.0, 85.0), 1) 
            results.append([d, target, energy, tox])
        st.session_state.screening_results = pd.DataFrame(results, columns=["Drug", "Target", "Energy", "Toxicity (%)"])

    if 'screening_results' in st.session_state:
        df = st.session_state.screening_results
        st.dataframe(df.style.background_gradient(subset=['Toxicity (%)'], cmap='RdYlGn_r'))
        selection = st.selectbox("Select a Lead to Promote:", df['Drug'])
        if st.button("Link Lead to Pipeline"):
            row = df[df['Drug'] == selection].iloc[0]
            st.session_state.selected_drug = row['Drug']
            st.session_state.selected_energy = row['Energy']
            st.session_state.selected_target = row['Target']
            st.session_state.selected_tox = row['Toxicity (%)']
            st.success(f"Linked {selection} to all modules!")

# -------------------------------------------------
# 2. DOSE RESPONSE SIMULATOR
# -------------------------------------------------
elif module == "Dose Response Simulator":
    st.header("📈 Advanced Pharmacodynamics")
    target = st.session_state.selected_target
    energy = st.session_state.selected_energy
    tox_val = st.session_state.selected_tox
    p_type = protein_categories.get(target, "Enzyme")
    
    # Math logic for Curve
    calc_ec50 = np.interp(energy, [-12, -4], [0.5, 200])
    calc_emax = np.interp(energy, [-12, -4], [100, 40])
    auto_hill = 2.5 if p_type in ["Receptor", "Transcription Factor"] else 1.2

    conc = np.logspace(-1, 4, 100)
    response = (calc_emax * (conc**auto_hill)) / ( (calc_ec50**auto_hill) + (conc**auto_hill) )
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=conc, y=response, line=dict(color='#00CC96', width=4), name="Response"))
    fig.add_hline(y=tox_val, line_dash="dot", line_color="red", annotation_text="Toxicity Threshold")
    fig.update_layout(xaxis_type="log", template="plotly_white", yaxis_title="Biological Effect %", xaxis_title="Dose (nM)")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 3. PROTEIN PATHWAY (WITH DESCRIPTIONS)
# -------------------------------------------------
elif module == "Protein Pathway Simulator":
    st.header("⚡ Pathway Impact Analysis")
    energy = st.session_state.selected_energy
    target = st.session_state.selected_target
    inhibition = np.interp(energy, [-12, -4], [100, 20])
    p_type = protein_categories.get(target, "Enzyme")
    depth = 5 if p_type in ["Receptor", "Transcription Factor"] else 3

    # Bar Chart
    steps = [f"Protein {i+1}" for i in range(depth)]
    # Each step loses 20% of the previous step's signal
    signal = [inhibition * (0.8**i) for i in range(depth)]
    
    st.plotly_chart(go.Figure(go.Bar(x=steps, y=signal, marker_color='firebrick', text=[f"{round(s)}%" for s in signal])), use_container_width=True)
    
    with st.expander("📊 What does this Bar Chart represent?"):
        st.markdown(f"""
        <div class="description-text">
        The Bar Chart visualizes <b>Signal Decay</b>. In a cell, proteins pass messages like a relay race. 
        <ul>
            <li><b>First Bar:</b> This is <b>{st.session_state.selected_drug}'s</b> direct effect on <b>{target}</b>.</li>
            <li><b>Subsequent Bars:</b> These show how much of that original "message" reaches further into the cell. </li>
            <li><b>Scientific Reality:</b> No biological signal is 100% efficient. We simulate a 20% loss at every step. If the final bar is too low, the drug won't actually change the patient's health.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # Pathway Map
    net = Network(height="400px", width="100%", bgcolor="#ffffff", directed=True)
    chain = [target] + random.sample([p for p in protein_list if p != target], depth - 1)
    for i in range(len(chain)):
        s_val = inhibition * (0.8**i)
        net.add_node(chain[i], label=f"{chain[i]}\n{round(s_val)}%", color="#ff4b4b" if i==0 else "#1c83e1")
        if i > 0: net.add_edge(chain[i-1], chain[i], width=3)
    
    path = "pathway.html"
    net.save_graph(path)
    with open(path, 'r', encoding='utf-8') as f:
        components.html(f.read(), height=450)
    
    with st.expander("🕸️ What does this Pathway Map represent?"):
        st.markdown(f"""
        <div class="description-text">
        The Network Map shows the <b>Chain Reaction</b> triggered by your drug.
        <ul>
            <li><b>Red Node:</b> Your primary drug target. This is where the chemistry happens.</li>
            <li><b>Blue Nodes:</b> Downstream proteins. They don't touch the drug directly, but their behavior changes because the Red Node was blocked.</li>
            <li><b>The Goal:</b> To see if your drug can influence the "Inner Circle" of the cell's signaling network.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------
# 4. NETWORK PHARMACOLOGY EXPLORER
# -------------------------------------------------
elif module == "Network Pharmacology Explorer":
    st.header("🕸️ Network Pharmacology Explorer")
    drug = st.session_state.selected_drug
    st.write(f"Mapping Polypharmacology for **{drug}**")
    
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")
    net.add_node(drug, label=drug, color="#ff4b4b", size=35)
    
    # Simulate multi-target binding
    for t in random.sample(protein_list, 5):
        net.add_node(t, label=t, color="#1c83e1")
        net.add_edge(drug, t)
    
    net.toggle_physics(True)
    path = "network_map.html"
    net.save_graph(path)
    with open(path, 'r', encoding='utf-8') as f:
        components.html(f.read(), height=550)

# -------------------------------------------------
# 5. MOLECULAR DOCKING SIMULATOR
# -------------------------------------------------
elif module == "Molecular Docking Simulator":
    st.header("🧩 Molecular Docking Simulator")
    drug = st.session_state.selected_drug
    target = st.session_state.selected_target
    energy = st.session_state.selected_energy

    st.write(f"Calculating atomic fit: **{drug}** into **{target}**")
    
    poses = []
    for i in range(1, 6):
        # Center the poses around our screened energy
        poses.append([i, round(energy + random.uniform(-0.4, 0.4), 2), random.choice(["H-Bond", "Hydrophobic"])])
    
    df_dock = pd.DataFrame(poses, columns=["Pose", "Energy (kcal/mol)", "Key Interaction"])
    st.table(df_dock)
    st.info("Pose 1 represents the most energetically favorable binding mode.")
