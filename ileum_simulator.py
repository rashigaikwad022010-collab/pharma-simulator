import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
from pyvis.network import Network
import streamlit.components.v1 as components

# --- UI SETTINGS ---
st.set_page_config(page_title="Advanced Pharma Pipeline", layout="wide", page_icon="🧬")

# Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 8px; background-color: #007bff; color: white; font-weight: bold; }
    .explanation-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 6px solid #007bff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin: 20px 0; }
    .conclusion-card { padding: 30px; border-radius: 15px; border: 2px solid #eee; margin-top: 30px; }
    .go-signal { background-color: #d4edda; border-color: #28a745; color: #155724; }
    .nogo-signal { background-color: #f8d7da; border-color: #dc3545; color: #721c24; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Advanced Pharmaceutical Research & Docking Pipeline")

# --- DATABASE ---
drug_db = {
    "Statins": ["Atorvastatin", "Simvastatin", "Rosuvastatin"],
    "Antihistamines": ["Loratadine", "Cetirizine", "Diphenhydramine"],
    "NSAIDs": ["Aspirin", "Ibuprofen", "Naproxen"],
    "Antidiabetics": ["Metformin", "Glipizide"],
}
protein_categories = {
    "CASP3": "Enzyme (Apoptosis)", "H1-Receptor": "Receptor", 
    "HMG-CoA": "Enzyme", "COX2": "Enzyme", "EGFR": "Receptor", 
}
all_drugs = [d for sub in drug_db.values() for d in sub]
all_proteins = list(protein_categories.keys())

# --- INITIALIZE SESSION STATE ---
if 'selected_energy' not in st.session_state: st.session_state.selected_energy = -7.5
if 'selected_drug' not in st.session_state: st.session_state.selected_drug = "Atorvastatin"
if 'selected_target' not in st.session_state: st.session_state.selected_target = "CASP3"

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🔬 Research Parameters")
st.session_state.selected_drug = st.sidebar.selectbox("Lead Compound:", all_drugs, index=all_drugs.index(st.session_state.selected_drug))
st.session_state.selected_target = st.sidebar.selectbox("Target Protein:", all_proteins, index=all_proteins.index(st.session_state.selected_target))
st.session_state.selected_energy = st.sidebar.slider("Binding Affinity (kcal/mol)", -12.0, -4.0, st.session_state.selected_energy)

# DYNAMIC TOXICITY THRESHOLD
# Stronger binding increases potency but narrows the safety window.
dynamic_tox = round(abs(st.session_state.selected_energy) * 8.5, 1)

module = st.sidebar.selectbox("Pipeline Stage:", 
    ["Virtual Screening", "Dose-Response Analysis", "Pathway & Signal Analysis", "Molecular Docking", "Project Conclusion"])

# -------------------------------------------------
# 1. VIRTUAL SCREENING
# -------------------------------------------------
if module == "Virtual Screening":
    st.header("🧪 High-Throughput Screening (HTS)")
    if st.button("🚀 Execute Library Screen"):
        results = []
        for d in all_drugs:
            energy = round(random.uniform(-11, -4), 2)
            tox = round(abs(energy) * random.uniform(5, 10), 1)
            status = "✅ SAFE" if tox < 65 else "⚠️ UNSAFE"
            results.append([d, st.session_state.selected_target, energy, tox, status])
        st.session_state.screen_df = pd.DataFrame(results, columns=["Drug", "Target", "Energy", "Toxicity %", "Status"])
    
    if 'screen_df' in st.session_state:
        st.table(st.session_state.screen_df)

# -------------------------------------------------
# 2. DOSE-RESPONSE SIMULATOR
# -------------------------------------------------
elif module == "Dose-Response Analysis":
    st.header(f"📈 Pharmacodynamic Profile: {st.session_state.selected_drug}")
    
    ec50 = np.interp(st.session_state.selected_energy, [-12, -4], [0.5, 150])
    hill_coeff = 2.4 if protein_categories[st.session_state.selected_target] == "Receptor" else 1.2
    
    conc = np.logspace(-1, 4, 100)
    response = (100 * (conc**hill_coeff)) / ( (ec50**hill_coeff) + (conc**hill_coeff) )
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=conc, y=response, name="Efficacy Curve", line=dict(color='#007bff', width=4)))
    fig.add_hline(y=dynamic_tox, line_dash="dash", line_color="red", annotation_text="Toxicity Threshold")
    fig.update_layout(xaxis_type="log", title="Log-Dose Response Graph", xaxis_title="Concentration (nM)", yaxis_title="Biological Response (%)")
    st.plotly_chart(fig, use_container_width=True)
    

    st.markdown(f"""
    <div class="explanation-box">
        <h3>📊 Professional Result Interpretation</h3>
        This graph models the <b>Therapeutic Window</b>. 
        <ul>
            <li><b>Hill Coefficient ({hill_coeff}):</b> Quantifies the steepness of the curve. At {hill_coeff}, the drug displays {'cooperative binding' if hill_coeff > 1 else 'Michaelis-Menten kinetics'}.</li>
            <li><b>EC50 ({round(ec50, 2)} nM):</b> The concentration required to reach half-maximal efficacy. A lower EC50 relative to the Toxicity Threshold is critical for safety.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 3. PATHWAY & BAR CHART
# -------------------------------------------------
elif module == "Pathway & Signal Analysis":
    st.header("⚡ Cellular Signaling & Signal Decay")
    
    inhibition = np.interp(st.session_state.selected_energy, [-12, -4], [98, 15])
    steps = [st.session_state.selected_target, "Relay Protein", "Kinase Cascade", "Transcription", "Cell Fate"]
    decay = [round(inhibition * (0.8**i), 1) for i in range(len(steps))]
    
    st.subheader("Signal Attenuation (Bar Chart)")
    st.plotly_chart(go.Figure(go.Bar(x=steps, y=decay, marker_color='#6610f2', text=decay, textposition='auto')), use_container_width=True)
    
    st.markdown(f"""
    <div class="explanation-box">
        <h3>📉 Bar Chart Analysis</h3>
        <b>Signal Attenuation</b> represents the loss of pharmacological "momentum." As the inhibition of <b>{st.session_state.selected_target}</b> propagates through the cell, internal feedback loops and resistance reduce the net effect. 
        A final impact of <b>{decay[-1]}%</b> is observed at the 'Cell Fate' stage.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Biological Flowchart (Pathway)")
    net = Network(height="400px", width="100%", bgcolor="#ffffff", directed=True)
    for i, step in enumerate(steps):
        net.add_node(step, label=f"{step}\n{decay[i]}%", color="#ff4b4b" if i==0 else "#1c83e1")
        if i > 0: net.add_edge(steps[i-1], steps[i])
    net.save_graph("path.html")
    with open("path.html", 'r') as f: components.html(f.read(), height=450)
    

    st.markdown("""
    <div class="explanation-box">
        <h3>🕸️ Flowchart Logic</h3>
        The flowchart visualizes the <b>Signal Transduction Pathway</b>. In drug discovery, we must ensure the drug doesn't just bind to the surface, but effectively communicates its message to the downstream executors of cellular function.
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 4. MOLECULAR DOCKING
# -------------------------------------------------
elif module == "Molecular Docking":
    st.header("🧩 In-Silico Molecular Docking")
    poses = [[i, round(st.session_state.selected_energy + random.uniform(-0.3, 0.3), 2), random.choice(["H-Bond", "Van der Waals", "Pi-Stacking"])] for i in range(1, 6)]
    df_dock = pd.DataFrame(poses, columns=["Pose", "Affinity (kcal/mol)", "Interaction Type"])
    st.table(df_dock)
    

# -------------------------------------------------
# 5. PROJECT CONCLUSION (NEW SECTION)
# -------------------------------------------------
elif module == "Project Conclusion":
    st.header("🏁 Clinical Trial Readiness Verdict")
    
    # Logic for Verdict
    inhibition = np.interp(st.session_state.selected_energy, [-12, -4], [98, 15])
    final_signal = inhibition * (0.8**4)
    potency_score = abs(st.session_state.selected_energy)
    
    # Decision Criteria
    is_potent = potency_score > 7.0
    is_safe = dynamic_tox < 75.0
    is_effective = final_signal > 30.0
    
    verdict = "GO" if (is_potent and is_safe and is_effective) else "NO-GO"
    v_class = "go-signal" if verdict == "GO" else "nogo-signal"
    
    st.markdown(f"""
    <div class="conclusion-card {v_class}">
        <h2 style="text-align: center;">VERDICT: {verdict}</h2>
        <p style="text-align: center; font-size: 1.2em;">
            Project Status for <b>{st.session_state.selected_drug}</b> targeting <b>{st.session_state.selected_target}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Potency Level", "HIGH" if is_potent else "LOW", delta=f"{potency_score} kcal/mol")
    col2.metric("Safety Rating", "PASS" if is_safe else "FAIL", delta=f"{dynamic_tox}% Tox", delta_color="inverse")
    col3.metric("Pathway Impact", "STRONG" if is_effective else "WEAK", delta=f"{round(final_signal,1)}% Final")

    st.markdown(f"""
    <div class="explanation-box">
        <h3>📝 Detailed Clinical Rationale</h3>
        Based on the integrated data from the <b>Molecular Docking</b> and <b>Signal Decay</b> modules:
        <ul>
            <li><b>Binding Profile:</b> A binding energy of {st.session_state.selected_energy} kcal/mol suggests a {'strong' if is_potent else 'weak'} affinity for the active site.</li>
            <li><b>Therapeutic Index:</b> The dynamic toxicity threshold of {dynamic_tox}% {'is within' if is_safe else 'exceeds'} acceptable clinical safety margins.</li>
            <li><b>Pathway Conclusion:</b> A final signal strength of {round(final_signal,1)}% indicates that the drug {'will likely' if is_effective else 'will likely NOT'} result in a significant physiological change in a living subject.</li>
        </ul>
        <b>Final Recommendation:</b> { 'Proceed to Phase I Clinical Trials.' if verdict == 'GO' else 'Return to Lead Optimization for chemical structure modification.'}
    </div>
    """, unsafe_allow_html=True)
