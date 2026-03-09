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
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    .explanation-box { background-color: #f1f3f5; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Pharmaceutical Research Simulator Pro")

# --- INITIALIZE SESSION STATE ---
if 'selected_energy' not in st.session_state:
    st.session_state.selected_energy = -7.0
if 'selected_drug' not in st.session_state:
    st.session_state.selected_drug = "No Lead Selected"
if 'selected_target' not in st.session_state:
    st.session_state.selected_target = "COX2"
if 'selected_tox' not in st.session_state:
    st.session_state.selected_tox = 20.0

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
            logp = round(random.uniform(1.0, 6.0), 1)
            results.append([d, target, energy, tox, logp])
        # Save to session state
        st.session_state.screening_results = pd.DataFrame(results, columns=["Drug", "Target", "Energy", "Toxicity (%)", "LogP"])

    # FIXED: Only show and style if data exists
    if 'screening_results' in st.session_state:
        df = st.session_state.screening_results
        # Style with a color gradient (Green for safe, Red for toxic)
        st.dataframe(df.style.background_gradient(subset=['Toxicity (%)'], cmap='RdYlGn_r'))
        
        selection = st.selectbox("Select a Lead to Promte to Pipeline:", df['Drug'])
        if st.button("Link Lead to Pipeline"):
            row = df[df['Drug'] == selection].iloc[0]
            st.session_state.selected_drug = row['Drug']
            st.session_state.selected_energy = row['Energy']
            st.session_state.selected_target = row['Target']
            st.session_state.selected_tox = row['Toxicity (%)']
            st.success(f"Linked {selection}! Data sent to Dose-Response & Pathway modules.")

    st.markdown("---")
    st.subheader("📖 Understanding the Parameters")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Binding Energy:** How 'sticky' the drug is. Lower (more negative) is better!")
        st.write("**Toxicity (%):** Higher numbers mean the drug might harm healthy cells.")
    with c2:
        st.write("**LogP:** Tells us if the drug is too oily. Ideally, this should be between 1 and 5.")

# -------------------------------------------------
# 2. DOSE RESPONSE SIMULATOR (ADVANCED)
# -------------------------------------------------
elif module == "Dose Response Simulator":
    st.header("📈 Advanced Pharmacodynamics Model")
    
    # Auto-Calculations
    energy = st.session_state.selected_energy
    target = st.session_state.selected_target
    tox_val = st.session_state.selected_tox
    p_type = protein_categories.get(target, "Enzyme")
    
    # Mathematical Logic
    calc_ec50 = np.interp(energy, [-12, -4], [0.5, 200])
    calc_emax = np.interp(energy, [-12, -4], [100, 40])
    auto_hill = 2.5 if p_type in ["Receptor", "Transcription Factor"] else 1.2

    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("EC50 (Potency)", f"{round(calc_ec50, 1)} nM")
    col2.metric("Emax (Efficacy)", f"{round(calc_emax)}%")
    col3.metric("Toxicity Threshold", f"{tox_val}%")

    # Generate Chart with Confidence Interval
    conc = np.logspace(-1, 4, 100)
    response = (calc_emax * (conc**auto_hill)) / ( (calc_ec50**auto_hill) + (conc**auto_hill) )
    
    fig = go.Figure()
    # Shaded Confidence Interval
    fig.add_trace(go.Scatter(x=np.concatenate([conc, conc[::-1]]), y=np.concatenate([response*1.1, (response*0.9)[::-1]]),
                             fill='toself', fillcolor='rgba(0,204,150,0.2)', line=dict(color='rgba(255,255,255,0)'), name='95% CI'))
    # Main Line
    fig.add_trace(go.Scatter(x=conc, y=response, line=dict(color='#00CC96', width=4), name='Predicted Response'))
    # Toxicity Line
    fig.add_hline(y=tox_val, line_dash="dot", line_color="red", annotation_text="Safety Limit")

    fig.update_layout(xaxis_type="log", yaxis_title="Effect (%)", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="explanation-box">
    <h3>🔍 Scientist's Analysis</h3>
    <ul>
        <li><b>EC50:</b> At {round(calc_ec50, 1)} nM, we reach half of the maximum effect. A lower number means you need less medicine to help the patient.</li>
        <li><b>Hill Coefficient ({auto_hill}):</b> This is the slope. Since {target} is a {p_type}, the response is <b>{"steep (switch-like)" if auto_hill > 2 else "gradual"}</b>.</li>
        <li><b>Safety Gap:</b> If the green line is higher than the red dotted line, the drug is <b>Toxic</b> at that dose.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

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
    
    st.plotly_chart(go.Figure(go.Bar(x=steps, y=signal, marker_color='firebrick', text=[f"{round(s)}%" for s in signal])), use_container_width=True)

    st.markdown(f"""
    <div class="explanation-box">
    <h3>🛡️ Biological Signal Loss</h3>
    Because biology isn't perfect, the signal from <b>{target}</b> loses 20% of its power at every step. 
    The final bar shows the <b>Real Impact</b> on the cell. If it's too low, the drug fails in clinical trials.
    </div>
    """, unsafe_allow_html=True)

    # Pathway map code...
    net = Network(height="400px", width="100%", bgcolor="#ffffff", directed=True)
    chain = [target] + random.sample([p for p in protein_list if p != target], depth - 1)
    for i in range(len(chain)):
        s_val = inhibition * (0.8**i)
        net.add_node(chain[i], label=f"{chain[i]}\n{round(s_val)}%", color="#ff4b4b" if i==0 else "#1c83e1")
        if i > 0: net.add_edge(chain[i-1], chain[i], width=3)
    net.save_graph("map.html")
    with open("map.html", 'r') as f: components.html(f.read(), height=400)
