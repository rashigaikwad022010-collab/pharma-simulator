import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# --- UI SETTINGS ---
st.set_page_config(page_title="Integrated Pharma Simulator", layout="wide", page_icon="🧬")

# --- INITIALIZE SESSION STATE ---
if 'selected_energy' not in st.session_state:
    st.session_state.selected_energy = -7.0
if 'selected_drug' not in st.session_state:
    st.session_state.selected_drug = "None Selected"
if 'selected_target' not in st.session_state:
    st.session_state.selected_target = "COX2"

# --- DATABASE ---
drug_list = ["Aspirin","Ibuprofen","Metformin","Atorvastatin","Amlodipine","Omeprazole","Sertraline"]
protein_categories = {
    "COX2": "Enzyme", "AKT1": "Kinase", "EGFR": "Receptor", 
    "STAT3": "Transcription Factor", "TNF": "Cytokine", "VEGFA": "Growth Factor"
}
protein_list = list(protein_categories.keys())

# --- SIDEBAR ---
module = st.sidebar.selectbox("Select Module", ["Virtual Drug Screening", "Dose Response Simulator", "Protein Pathway Simulator"])

# -------------------------------------------------
# 1. VIRTUAL DRUG SCREENING
# -------------------------------------------------
if module == "Virtual Drug Screening":
    st.header("🧪 Step 1: High-Throughput Screening")
    if st.button("🚀 Run New Screen"):
        results = []
        for d in random.sample(drug_list, 5):
            target = random.choice(protein_list)
            energy = round(random.uniform(-11.0, -4.0), 2)
            results.append([d, target, energy, "✅ Pass" if energy < -7 else "⚠️ Weak"])
        st.session_state.screening_results = pd.DataFrame(results, columns=["Drug", "Target", "Energy", "Status"])

    if 'screening_results' in st.session_state:
        st.dataframe(st.session_state.screening_results)
        selection = st.selectbox("Select Lead:", st.session_state.screening_results['Drug'])
        if st.button("Set as Active Lead"):
            row = st.session_state.screening_results[st.session_state.screening_results['Drug'] == selection].iloc[0]
            # AUTOMATICALLY SETTING EVERYTHING HERE
            st.session_state.selected_drug = row['Drug']
            st.session_state.selected_energy = row['Energy']
            st.session_state.selected_target = row['Target']
            st.success(f"Linked {selection}! Target & Hill Coefficient are now auto-set.")

# -------------------------------------------------
# 2. DOSE RESPONSE (AUTO-SET)
# -------------------------------------------------
elif module == "Dose Response Simulator":
    st.header("📈 Step 2: Dose-Response Modeling")
    
    # Auto-Targeting
    target = st.session_state.selected_target
    energy = st.session_state.selected_energy
    p_type = protein_categories.get(target, "Enzyme")
    
    # Auto-Hill Coefficient Logic
    # Receptors/Transcription Factors have steep curves (high Hill); Enzymes have standard curves.
    auto_hill = 2.5 if p_type in ["Receptor", "Transcription Factor"] else 1.0
    
    st.info(f"Target: **{target}** ({p_type}) | Auto-Hill Coefficient: **{auto_hill}**")

    calc_ec50 = np.interp(energy, [-12, -4], [1, 150])
    calc_emax = np.interp(energy, [-12, -4], [100, 50])
    
    conc = np.logspace(-1, 3, 100)
    response = (calc_emax * (conc**auto_hill)) / ( (calc_ec50**auto_hill) + (conc**auto_hill) )

    fig = go.Figure(go.Scatter(x=conc, y=response, line=dict(color='#00CC96', width=4)))
    fig.update_layout(title=f"Curve for {st.session_state.selected_drug}", xaxis_type="log")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 3. PROTEIN PATHWAY (AUTO-SET & EXPLAINED)
# -------------------------------------------------
elif module == "Protein Pathway Simulator":
    st.header("⚡ Step 3: Pathway Impact Analysis")
    
    energy = st.session_state.selected_energy
    target = st.session_state.selected_target
    inhibition = np.interp(energy, [-12, -4], [100, 20])
    p_type = protein_categories.get(target, "Enzyme")
    depth = 5 if p_type in ["Receptor", "Transcription Factor"] else 3

    # Bar Graph
    steps = [f"Step {i+1}" for i in range(depth)]
    signal = [inhibition * (0.8**i) for i in range(depth)]
    st.plotly_chart(go.Figure(go.Bar(x=steps, y=signal, marker_color='firebrick', text=[f"{round(s)}%" for s in signal])), use_container_width=True)

    # Pathway Map
    net = Network(height="400px", width="100%", bgcolor="#ffffff", directed=True)
    chain = [target] + random.sample([p for p in protein_list if p != target], depth - 1)
    for i in range(len(chain)):
        s_val = inhibition * (0.8**i)
        net.add_node(chain[i], label=f"{chain[i]}\n{round(s_val)}%", color="#ff4b4b" if i==0 else "#1c83e1")
        if i > 0: net.add_edge(chain[i-1], chain[i], width=3)
    
    net.save_graph("map.html")
    with open("map.html", 'r') as f: components.html(f.read(), height=400)

    # --- THE EXPLANATION ---
    st.divider()
    st.subheader("📚 Understanding your Results")
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown(f"""
        ### What the Bar Graph Says:
        * **Starting Bar:** This is the direct effect of **{st.session_state.selected_drug}** on **{target}**. Since your binding energy was {energy}, the inhibition starts at **{round(inhibition)}%**.
        * **The Decay:** Notice how each bar is smaller? This represents **Biological Signal Loss**. In a real cell, energy is lost as one protein tries to activate the next.
        """)

    with colB:
        st.markdown(f"""
        ### What the Pathway Map Says:
        * **Red Node:** This is your **Primary Target**. This is the only protein the drug actually touches.
        * **Blue Nodes:** These are **Downstream Proteins**. They are affected indirectly. If the Red node is blocked, the Blue nodes "starve" of signals.
        * **Final Step:** The last node represents the actual goal (like stopping inflammation). Your drug achieves a final impact of **{round(signal[-1])}%**.
        """)
