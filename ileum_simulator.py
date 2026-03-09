import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
from pyvis.network import Network
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

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
    ["Virtual Screening", "Venn Diagram Analysis", "Dose-Response Analysis", "Pathway & Signal Analysis", "Network Pharmacology Explorer", "Molecular Docking", "Project Conclusion"])

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
# 2. VENN DIAGRAM ANALYSIS
# -------------------------------------------------
elif module == "Venn Diagram Analysis":
    st.header(f"📊 Target Overlap Analysis: {st.session_state.selected_drug}")
    
    # Values based on your uploaded images (62 exclusive, 49 intersection, 33 exclusive)
    fig, ax = plt.subplots(figsize=(8, 5))
    v = venn2(subsets=(62, 33, 49), set_labels=(f'Predicted Targets\nof {st.session_state.selected_drug}', 'Disease-Associated\nProteins'))
    st.pyplot(fig)
    

    st.markdown(f"""
    <div class="explanation-box">
        <h3>🔍 Venn Result Interpretation</h3>
        This diagram identifies the <b>Therapeutic Bioactives</b>:
        <ul>
            <li><b>Total Overlap (49):</b> These are the high-priority targets. They represent proteins that are both predicted to bind with {st.session_state.selected_drug} and are scientifically proven to be involved in the disease.</li>
            <li><b>Exclusive Drug Targets (62):</b> These represent potential "off-target" interactions which might cause secondary side effects.</li>
            <li><b>Relevance:</b> Finding 49 common targets is a statistically significant result, suggesting this drug has strong multi-target potential for treating the condition.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 3. DOSE-RESPONSE ANALYSIS
# -------------------------------------------------
elif module == "Dose-Response Analysis":
    st.header(f"📈 Pharmacodynamic Profile: {st.session_state.selected_drug}")
    
    ec50 = np.interp(st.session_state.selected_energy, [-12, -4], [0.5, 150])
    hill_coeff = 2.4 if protein_categories[st.session_state.selected_target] == "Receptor" else 1.2
    emax = 100.0
    
    conc = np.logspace(-1, 4, 100)
    response = (emax * (conc**hill_coeff)) / ( (ec50**hill_coeff) + (conc**hill_coeff) )
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=conc, y=response, name="Response Curve", line=dict(color='#007bff', width=4)))
    fig.add_hline(y=dynamic_tox, line_dash="dash", line_color="red", annotation_text="Toxicity Threshold")
    fig.update_layout(xaxis_type="log", title="Log-Dose Response Graph", xaxis_title="Concentration (nM)", yaxis_title="Response (%)")
    st.plotly_chart(fig, use_container_width=True)
    

    st.subheader("📊 Dose-Response Calculation Table")
    metrics = {
        "Parameter": ["Calculated EC50", "Hill Slope (n)", "Max Efficacy (Emax)", "Toxicity Limit"],
        "Value": [f"{round(ec50, 2)} nM", hill_coeff, f"{emax}%", f"{dynamic_tox}%"],
        "Interpretation": [
            "Potency: Concentration needed for 50% effect. Smaller is better.",
            "Cooperativity: Steepness of the curve. Higher values mean a sharp 'on/off' effect.",
            "Capacity: The highest level of biological effect the drug can achieve.",
            "Safety Ceiling: The response level where adverse events are predicted."
        ]
    }
    st.table(pd.DataFrame(metrics))

# -------------------------------------------------
# 4. PATHWAY & BAR CHART
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
        <h3>📉 Bar Chart Result Interpretation</h3>
        This chart displays <b>Pharmacological Momentum</b> across five biological stages:
        <ul>
            <li><b>Initial Binding:</b> At the start, <b>{st.session_state.selected_drug}</b> blocks <b>{decay[0]}%</b> of the <b>{st.session_state.selected_target}</b> enzyme.</li>
            <li><b>Intermediate Decay:</b> By the <b>{steps[2]}</b> stage, only <b>{decay[2]}%</b> of that inhibitory signal remains.</li>
            <li><b>Net Physiological Impact:</b> The final <b>{decay[4]}%</b> shows the actual change in the patient's cell fate. A value below 30% indicates the drug's effect is lost before it can treat the disease.</li>
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
    

    st.markdown(f"""
    <div class="explanation-box">
        <h3>🕸️ Flowchart Result Interpretation</h3>
        This diagram maps the <b>Signaling Chain Reaction</b> within the cell:
        <ul>
            <li><b>Red Master Node ({decay[0]}%):</b> This represents the direct docking site. Because it is turned off at {decay[0]}%, the biological 'highway' is blocked.</li>
            <li><b>Information Flow:</b> The arrows show how the signal travels. The Blue nodes show the <b>domino effect</b>; because the first node is inhibited, the subsequent proteins are 'starved' of their activating signal.</li>
            <li><b>Outcome:</b> The final node at <b>{decay[4]}%</b> is the successful prevention of a disease response.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 5. NETWORK PHARMACOLOGY EXPLORER
# -------------------------------------------------
elif module == "Network Pharmacology Explorer":
    st.header(f"🕸️ STRING Mesh: Functional Protein Associations")
    net = Network(height="550px", width="100%", bgcolor="#ffffff", font_color="black")
    
    # Core Drug Node
    net.add_node(st.session_state.selected_drug, label=st.session_state.selected_drug, color="#ff4b4b", size=40)
    
    # Primary Targets (Emphasizing the 49 Intersection Targets)
    mesh_targets = ["AKT1", "STAT3", "TNF", "MAPK", "IL-6", "PTGS2", "VEGFA", "NFKB1"]
    for p in mesh_targets:
        # Highlighting core intersection targets
        is_intersection = p in ["TNF", "IL-6", "PTGS2"]
        net.add_node(p, label=p, color="#ff4b4b" if is_intersection else "#1c83e1", size=30 if is_intersection else 20)
        net.add_edge(st.session_state.selected_drug, p, width=2)
    
    # Functional Association "Strings" (STRING Database Logic)
    for i in range(len(mesh_targets)):
        target_a = mesh_targets[i]
        # Create a mesh by connecting neighbors
        target_b = mesh_targets[(i + 1) % len(mesh_targets)]
        target_c = mesh_targets[(i + 2) % len(mesh_targets)]
        net.add_edge(target_a, target_b, color="#dddddd", width=1)
        net.add_edge(target_a, target_c, color="#666666", width=1) # Darker strings for higher confidence
                
    net.toggle_physics(True)
    net.save_graph("mesh.html")
    with open("mesh.html", 'r') as f: components.html(f.read(), height=600)
    

    st.markdown("""
    <div class="explanation-box">
        <h3>🕸️ STRING Network Result Interpretation</h3>
        This "Mesh of Strings" mimics your <b>STRING Database</b> results:
        <ul>
            <li><b>Node Colors:</b> The Red nodes represent the <b>Intersection Targets</b> (Bioactive Hubs). The Blue nodes are associated secondary targets.</li>
            <li><b>String Connectivity:</b> The density of strings between nodes (e.g., TNF and IL-6) shows <b>Functional Association</b>. In your results, high connectivity indicates that the drug disrupts an entire disease pathway, not just a single protein.</li>
            <li><b>Biological Hubs:</b> Proteins with the most strings are "Hubs." If your drug hits a hub, the treatment is more powerful but must be monitored for safety.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 6. MOLECULAR DOCKING
# -------------------------------------------------
elif module == "Molecular Docking":
    st.header("🧩 In-Silico Molecular Docking")
    
    inter_types = ["H-Bond (Hydrogen Bonding)", "Van der Waals Force", "Pi-Stacking (Hydrophobic)", "Ionic Interaction"]
    poses = [[i, round(st.session_state.selected_energy + random.uniform(-0.3, 0.3), 2), random.choice(inter_types)] for i in range(1, 6)]
    df_dock = pd.DataFrame(poses, columns=["Pose ID", "Affinity (kcal/mol)", "Interaction Type"])
    st.table(df_dock)
    

    st.markdown(f"""
    <div class="explanation-box">
        <h3>🧩 Docking Result Interpretation</h3>
        This data predicts the <b>Lock-and-Key fit</b>:
        <ul>
            <li><b>Pose 1:</b> The most stable conformation. The affinity of <b>{poses[0][1]} kcal/mol</b> indicates a high likelihood of spontaneous binding.</li>
            <li><b>Interaction Type:</b> {poses[0][2]} is the dominant force holding the drug in the protein pocket. H-bonding is usually the sign of a very specific and effective drug.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 7. PROJECT CONCLUSION
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
        <p style="text-align: center; font-size: 1.2em;">Based on potency, safety, and signaling efficacy for <b>{st.session_state.selected_drug}</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="explanation-box">
        <h3>📝 Detailed Clinical Rationale</h3>
        <ul>
            <li><b>Binding Profile:</b> Energy of {st.session_state.selected_energy} kcal/mol shows {'strong' if is_potent else 'weak'} affinity.</li>
            <li><b>Safety Rating:</b> Toxicity threshold of {dynamic_tox}% is {'within' if is_safe else 'outside'} acceptable limits.</li>
            <li><b>Efficacy Conclusion:</b> A final signal of {round(final_signal,1)}% proves the drug {'can' if is_effective else 'cannot'} effectively alter the cellular outcome.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
