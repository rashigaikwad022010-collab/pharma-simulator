import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# --- UI SETTINGS ---
st.set_page_config(page_title="Pharmaceutical Research Simulator", layout="wide", page_icon="🧬")

# Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #007bff; color: white; }
    .stTable { border-radius: 10px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Pharmaceutical Research Simulator")

# --- INITIALIZE SESSION STATE ---
# This is the "Memory" that allows the Screening module to talk to the others
if 'selected_energy' not in st.session_state:
    st.session_state.selected_energy = -7.0
if 'selected_drug' not in st.session_state:
    st.session_state.selected_drug = "No Lead Selected"
if 'selected_target' not in st.session_state:
    st.session_state.selected_target = "COX2"

# -------------------------------------------------
# SIDEBAR MODULE SELECTOR
# -------------------------------------------------
module = st.sidebar.selectbox(
    "Select Simulator Module",
    [
        "Virtual Drug Screening",
        "Dose Response Simulator",
        "Protein Pathway Simulator",
        "Network Pharmacology Explorer",
        "Molecular Docking Simulator",
        "Custom Docking Simulator"
    ]
)

# -------------------------------------------------
# DRUG & PROTEIN DATABASE
# -------------------------------------------------
drug_list = [
    "Aspirin","Ibuprofen","Paracetamol","Diclofenac","Naproxen",
    "Metformin","Glibenclamide","Insulin","Atorvastatin","Simvastatin",
    "Amlodipine","Losartan","Valsartan","Omeprazole","Pantoprazole",
    "Cetirizine","Loratadine","Salbutamol","Sertraline","Diazepam"
]

protein_categories = {
    "COX2": "Enzyme", "AKT1": "Kinase", "MAPK1": "Kinase", "PI3K": "Enzyme",
    "mTOR": "Enzyme", "EGFR": "Receptor", "JAK2": "Kinase", "STAT3": "Transcription Factor",
    "NFkB": "Transcription Factor", "TNF": "Cytokine", "IL6": "Cytokine", "BRAF": "Kinase",
    "MEK1": "Kinase", "ERK2": "Kinase", "SRC": "Kinase", "VEGFA": "Growth Factor",
    "HIF1A": "Transcription Factor", "TP53": "Tumor Suppressor", "CDK2": "Kinase",
    "CDK4": "Kinase", "GSK3B": "Kinase", "PTEN": "Enzyme", "FOXO3": "Transcription Factor",
    "MYC": "Transcription Factor", "CASP3": "Protease", "CASP9": "Protease",
    "MMP9": "Enzyme", "NOS3": "Enzyme", "CXCL8": "Cytokine", "TGFb1": "Growth Factor"
}
protein_list = list(protein_categories.keys())

# -------------------------------------------------
# 1. VIRTUAL DRUG SCREENING (THE DISCOVERY)
# -------------------------------------------------
if module == "Virtual Drug Screening":
    st.header("🧪 Step 1: High-Throughput Screening")
    st.write("Screen for Binding Affinity + Drug-Likeness (Lipinski's Rules)")
    
    if st.button("🚀 Run High-Throughput Screen"):
        test_drugs = random.sample(drug_list, 10)
        target = random.choice(protein_list)
        results = []
        for d in test_drugs:
            energy = round(random.uniform(-11.0, -4.0), 2)
            mw = random.randint(200, 600)
            logp = round(random.uniform(1, 6), 1)
            pass_rules = "✅ Pass" if mw < 500 and logp < 5 else "❌ Fail"
            results.append([d, target, energy, mw, logp, pass_rules])
        st.session_state.screening_results = pd.DataFrame(results, columns=["Drug", "Target", "Energy", "MW", "LogP", "Lipinski"])

    if 'screening_results' in st.session_state:
        df = st.session_state.screening_results
        st.dataframe(df.style.apply(lambda x: ['background-color: #d4edda' if x['Lipinski'] == "✅ Pass" and x['Energy'] < -8 else '' for i in x], axis=1))
        
        st.subheader("Connect to Research Pipeline")
        selection = st.selectbox("Pick a Lead Compound to test in other modules:", df['Drug'])
        if st.button("Set as Active Lead"):
            row = df[df['Drug'] == selection].iloc[0]
            st.session_state.selected_drug = row['Drug']
            st.session_state.selected_energy = row['Energy']
            st.session_state.selected_target = row['Target']
            st.success(f"Linked {selection} to Dose-Response and Pathway Simulators!")

# -------------------------------------------------
# 2. DOSE RESPONSE (CONNECTED LOGIC)
# -------------------------------------------------
elif module == "Dose Response Simulator":
    st.header("📈 Connected Pharmacodynamics Model")
    
    # Automatic pull from Screening
    drug_name = st.session_state.selected_drug
    target_protein = st.session_state.selected_target
    user_energy = st.session_state.selected_energy
    
    st.info(f"Currently Testing: **{drug_name}** | Target: **{target_protein}**")

    col1, col2 = st.columns(2)
    with col1:
        energy_input = st.number_input("Binding Energy (kcal/mol)", value=float(user_energy), step=0.1)
        calc_ec50 = np.interp(energy_input, [-12, -5], [1, 150])
        calc_emax = np.interp(energy_input, [-12, -5], [100, 70])
        st.metric("Predicted EC50", f"{round(calc_ec50, 2)} nM")
        st.metric("Predicted Emax", f"{round(calc_emax, 1)} %")

    with col2:
        p_type = protein_categories.get(target_protein, "Enzyme")
        auto_hill = 2.5 if p_type in ["Receptor", "Transcription Factor"] else 1.0
        st.write(f"**Target Analysis:** {target_protein} is a **{p_type}**.")
        hill_coeff = st.slider("Hill Coefficient (nH)", 0.5, 4.0, float(auto_hill))

    conc = np.logspace(-1, 3, 100) 
    response = (calc_emax * (conc**hill_coeff)) / ( (calc_ec50**hill_coeff) + (conc**hill_coeff) )

    fig = go.Figure(go.Scatter(x=conc, y=response, mode='lines', line=dict(color='#00CC96', width=4)))
    fig.update_layout(title=f"Dose-Response: {drug_name}", xaxis=dict(title="Conc (nM)", type="log"), yaxis=dict(title="Response (%)"))
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 3. PROTEIN PATHWAY SIMULATOR (CONNECTED & ATTRACTIVE)
# -------------------------------------------------
elif module == "Protein Pathway Simulator":
    st.header("⚡ Pathway Impact Analysis")
    
    energy = st.session_state.selected_energy
    target = st.session_state.selected_target
    drug_name = st.session_state.selected_drug

    st.info(f"🔬 **Analyzing Lead:** {drug_name} | **Target:** {target}")

    inhibition = np.interp(energy, [-12, -4], [100, 20])
    p_type = protein_categories.get(target, "Enzyme")
    depth = 5 if p_type in ["Receptor", "Transcription Factor", "Growth Factor"] else 3

    st.subheader("📊 Signal Decay Graph")
    steps = [f"Step {i+1}" for i in range(depth)]
    signal_values = [inhibition * (0.8**i) for i in range(depth)]

    fig_bar = go.Figure(go.Bar(x=steps, y=signal_values, marker_color='firebrick', text=[f"{round(s)}%" for s in signal_values], textposition='auto'))
    fig_bar.update_layout(yaxis=dict(title="Remaining Signal (%)", range=[0, 100]), template="plotly_white", height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("🔗 Biological Chain Interaction")
    path_net = Network(height="400px", width="100%", bgcolor="#ffffff", font_color="black", directed=True)
    chain = [target] + random.sample([p for p in protein_list if p != target], depth - 1)
    
    for i in range(len(chain)):
        strength = inhibition * (0.8**i)
        n_color = "#ff4b4b" if i == 0 else "#1c83e1"
        path_net.add_node(chain[i], label=f"{chain[i]}\n{round(strength)}%", color=n_color, size=25 if i==0 else 18)
        if i > 0: path_net.add_edge(chain[i-1], chain[i], width=3, color="#848484", arrows="to")

    path_net.toggle_physics(True)
    path_net.save_graph("pathway_map.html")
    with open("pathway_map.html", 'r', encoding='utf-8') as f:
        components.html(f.read(), height=450)

    st.divider()
    final_impact = signal_values[-1]
    st.write(f"### Verdict: This drug achieves a **{round(final_impact)}%** final biological impact.")

# -------------------------------------------------
# 4. NETWORK PHARMACOLOGY
# -------------------------------------------------
elif module == "Network Pharmacology Explorer":
    st.header("Network Pharmacology Explorer")
    drug = st.selectbox("Select Drug", drug_list)
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")
    net.add_node(drug, label=drug, color="#ff4b4b", size=25)
    targets = random.sample(protein_list, 15)
    for t in targets:
        net.add_node(t, label=t, color="#1c83e1")
        net.add_edge(drug, t)
    net.toggle_physics(True)
    net.save_graph("network.html")
    with open("network.html", 'r', encoding='utf-8') as f:
        components.html(f.read(), height=550)

# -------------------------------------------------
# 5. MOLECULAR DOCKING
# -------------------------------------------------
elif module == "Molecular Docking Simulator":
    st.header("Molecular Docking Simulator")
    col1, col2 = st.columns([1, 2])
    with col1:
        ligand = st.selectbox("Select Ligand", drug_list)
        protein = st.selectbox("Target Protein", protein_list)
        if st.button("Run Docking"):
            energies = -np.sort(np.random.uniform(5, 12, 8))
            df = pd.DataFrame({"Pose": range(1, 9), "Binding Energy (kcal/mol)": energies})
            with col2:
                st.subheader("Docking Poses")
                st.table(df)

# -------------------------------------------------
# 6. CUSTOM DOCKING
# -------------------------------------------------
elif module == "Custom Docking Simulator":
    st.header("Custom Docking Simulator")
    drug = st.text_input("Drug Name")
    protein = st.text_input("Target Protein")
    energy = st.number_input("Binding Energy", value=-7.5)
    if st.button("Simulate"):
        st.dataframe(pd.DataFrame({"Drug":[drug], "Protein":[protein], "Energy":[energy]}))
