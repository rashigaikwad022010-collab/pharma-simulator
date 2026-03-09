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
dynamic_tox = round(abs(st.session_state.selected_energy) * 8.5, 1)

module = st.sidebar.selectbox("Pipeline Stage:", 
    ["Virtual Screening", "Dose-Response Analysis", "Pathway & Signal Analysis", "Network Pharmacology Explorer", "Molecular Docking", "Project Conclusion"])

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
        <h3>📊 Result Analysis: The Dose-Response Graph</h3>
        This graph illustrates the <b>relationship between drug concentration and biological effect</b>. 
        <ul>
            <li><b>Sigmoidal Curve:</b> The "S" shape shows that the drug effect is dose-dependent. Low doses have no effect, while high doses reach a saturation point (Emax).</li>
            <li><b>EC50 ({round(ec50, 2)} nM):</b> This is the "Half Maximal Effective Concentration." It measures <b>Potency</b>. The lower the EC50, the less drug you need to achieve a result.</li>
            <li><b>Therapeutic Index:</b> The distance between the blue curve and the red line represents the <b>Safety Margin</b>. If the blue line crosses the red line at a low dose, the drug is dangerous.</li>
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
        <h3>📉 Result Analysis: Signal Attenuation</h3>
        This chart measures <b>Pharmacological Momentum</b>. 
        <ul>
            <li><b>Initial Inhibition ({decay[0]}%):</b> This is how strongly the drug stops the first protein.</li>
            <li><b>Signal Decay:</b> Biological systems are not perfect. Messages weaken as they travel through the cell. We simulate a 20% loss at every junction.</li>
            <li><b>Biological Relevance:</b> If the last bar (Cell Fate) is too low, the drug is "biologically silent"—it binds the target but fails to change the cell's behavior.</li>
        </ul>
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
        <h3>🕸️ Result Analysis: The Signaling Flowchart</h3>
        This represents the <b>Signaling Cascade</b> (the domino effect). 
        <ul>
            <li><b>Red Node:</b> The primary receptor where the drug binds.</li>
            <li><b>Arrows:</b> Represent the flow of information. By "locking" the red node, we stop the signal from reaching the nucleus, effectively turning off a disease process.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 4. NETWORK PHARMACOLOGY (MESH OF STRINGS)
# -------------------------------------------------
elif module == "Network Pharmacology Explorer":
    st.header(f"🕸️ Polypharmacology Mesh: {st.session_state.selected_drug}")
    
    net = Network(height="550px", width="100%", bgcolor="#ffffff", font_color="black")
    net.add_node(st.session_state.selected_drug, label=st.session_state.selected_drug, color="#ff4b4b", size=40)
    
    # Generate a mesh of connected protein targets
    other_proteins = ["AKT1", "STAT3", "TNF", "MAPK", "IL-6", "NF-kB", "mTOR"]
    for p in other_proteins:
        net.add_node(p, label=p, color="#1c83e1", size=20)
        net.add_edge(st.session_state.selected_drug, p, width=random.uniform(1, 5))
        
        # Add secondary connections (The Mesh)
        secondary = random.sample(other_proteins, 2)
        for s in secondary:
            if s != p:
                net.add_edge(p, s, color="#dddddd", width=1)
                
    net.toggle_physics(True)
    net.save_graph("mesh.html")
    with open("mesh.html", 'r') as f: components.html(f.read(), height=600)
    

    st.markdown("""
    <div class="explanation-box">
        <h3>🕸️ Result Analysis: Polypharmacology Mesh</h3>
        This "Mesh of Strings" represents <b>Network Pharmacology</b>. 
        <ul>
            <li><b>Primary Drug (Red):</b> Shows all proteins the drug interacts with. </li>
            <li><b>Mesh Connections (Grey):</b> These are protein-protein interactions. It proves that the cell is an interconnected web. </li>
            <li><b>Off-Target Effects:</b> If the drug binds to many proteins (high connectivity), it might have more side effects but could be more effective for complex diseases like cancer.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 5. MOLECULAR DOCKING (DETAILED INTERACTIONS)
# -------------------------------------------------
elif module == "Molecular Docking":
    st.header("🧩 In-Silico Molecular Docking")
    
    inter_types = ["H-Bond (Hydrogen Bonding)", "Van der Waals Force", "Pi-Stacking (Hydrophobic)", "Ionic Interaction"]
    poses = [[i, round(st.session_state.selected_energy + random.uniform(-0.3, 0.3), 2), random.choice(inter_types)] for i in range(1, 6)]
    df_dock = pd.DataFrame(poses, columns=["Pose ID", "Affinity (kcal/mol)", "Interaction Type"])
    st.table(df_dock)
    

    st.markdown(f"""
    <div class="explanation-box">
        <h3>🧩 Result Analysis: Molecular Docking</h3>
        This table displays the <b>Binding Modes</b>. 
        <ul>
            <li><b>H-Bonding:</b> This is the strongest type of "handshake" between a drug and a protein. It provides high specificity.</li>
            <li><b>Affinity:</b> The -{abs(st.session_state.selected_energy)} kcal/mol score tells us how much energy is released when the drug binds. A lower (more negative) number means a more stable and powerful drug.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 6. PROJECT CONCLUSION
# -------------------------------------------------
elif module == "Project Conclusion":
    st.header("🏁 Clinical Trial Readiness Verdict")
    inhibition = np.interp(st.session_state.selected_energy, [-12, -4], [98, 15])
    final_signal = inhibition * (0.8**4)
    potency_score = abs(st.session_state.selected_energy)
    
    is_potent = potency_score > 7.0
    is_safe = dynamic_tox < 75.0
    is_effective = final_signal > 30.0
    
    verdict = "GO" if (is_potent and is_safe and is_effective) else "NO-GO"
    v_class = "go-signal" if verdict == "GO" else "nogo-signal"
    
    st.markdown(f"""
    <div class="conclusion-card {v_class}">
        <h2 style="text-align: center;">VERDICT: {verdict}</h2>
        <p style="text-align: center; font-size: 1.2em;">Project Status for <b>{st.session_state.selected_drug}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="explanation-box">
        <h3>📝 Detailed Clinical Rationale</h3>
        <ul>
            <li><b>Binding Profile:</b> Energy of {st.session_state.selected_energy} kcal/mol suggests {'strong' if is_potent else 'weak'} affinity.</li>
            <li><b>Safety Rating:</b> Toxicity threshold of {dynamic_tox}% is {'within' if is_safe else 'outside'} acceptable limits.</li>
            <li><b>Efficacy Conclusion:</b> A final signal of {round(final_signal,1)}% proves the drug {'can' if is_effective else 'cannot'} effectively alter the cell's fate.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
