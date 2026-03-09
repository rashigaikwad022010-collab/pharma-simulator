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
# Initialize session state so modules can talk to each other
if 'selected_energy' not in st.session_state:
    st.session_state.selected_energy = -7.0
if 'selected_drug' not in st.session_state:
    st.session_state.selected_drug = "None"
if 'selected_target' not in st.session_state:
    st.session_state.selected_target = "COX2"

# -------------------------------------------------
# SIDEBAR MODULE SELECTOR
# -------------------------------------------------
module = st.sidebar.selectbox(
    "Select Simulator Module",
    [
        "Network Pharmacology Explorer",
        "Molecular Docking Simulator",
        "Custom Docking Simulator",
        "Dose Response Simulator",
        "Protein Pathway Simulator",
        "Virtual Drug Screening"
    ]
)

# -------------------------------------------------
# DRUG & PROTEIN DATABASE
# -------------------------------------------------
drug_list = [
"Aspirin","Ibuprofen","Paracetamol","Diclofenac","Naproxen",
"Ketorolac","Indomethacin","Celecoxib","Etoricoxib","Meloxicam",
"Amoxicillin","Ampicillin","Ciprofloxacin","Levofloxacin","Azithromycin",
"Clarithromycin","Doxycycline","Tetracycline","Metronidazole","Vancomycin",
"Metformin","Glibenclamide","Glimepiride","Insulin","Sitagliptin",
"Atorvastatin","Simvastatin","Rosuvastatin","Pravastatin","Lovastatin",
"Amlodipine","Losartan","Valsartan","Enalapril","Lisinopril",
"Hydrochlorothiazide","Furosemide","Spironolactone","Propranolol","Atenolol",
"Warfarin","Clopidogrel","Heparin","Rivaroxaban","Apixaban",
"Omeprazole","Pantoprazole","Esomeprazole","Lansoprazole","Rabeprazole",
"Ranitidine","Famotidine","Cimetidine",
"Cetirizine","Loratadine","Fexofenadine",
"Salbutamol","Formoterol","Budesonide","Montelukast",
"Prednisolone","Hydrocortisone","Dexamethasone",
"Fluoxetine","Sertraline","Paroxetine","Escitalopram",
"Diazepam","Alprazolam","Clonazepam",
"Morphine","Codeine","Tramadol",
"Ondansetron","Domperidone","Metoclopramide"
]

# Mapping Proteins to biological categories to drive the Hill Coefficient logic
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
# 1. NETWORK PHARMACOLOGY
# -------------------------------------------------
if module == "Network Pharmacology Explorer":
    st.header("Network Pharmacology Explorer")
    drug = st.selectbox("Select Drug", drug_list)
    
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")
    net.add_node(drug, label=drug, color="#ff4b4b", size=25)
    
    targets = random.sample(protein_list, 15)
    for t in targets:
        net.add_node(t, label=t, color="#1c83e1")
    
    for t in targets:
        net.add_edge(drug, t)
        if random.random() > 0.8:
            other_p = random.choice(targets)
            if other_p != t:
                net.add_edge(t, other_p)

    net.toggle_physics(True)
    net.save_graph("network.html")
    HtmlFile = open("network.html", 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=550)

# -------------------------------------------------
# 2. MOLECULAR DOCKING
# -------------------------------------------------
elif module == "Molecular Docking Simulator":
    st.header("Molecular Docking Simulator")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        ligand = st.selectbox("Select Ligand", drug_list)
        protein = st.selectbox("Target Protein", protein_list)
        run_btn = st.button("Run Docking")

    if run_btn:
        poses = 8
        energies = -np.sort(np.random.uniform(5, 12, poses))
        df = pd.DataFrame({"Pose": range(1, poses+1), "Binding Energy (kcal/mol)": energies})
        
        with col2:
            st.subheader("Docking Poses")
            st.table(df)
            residues = ["ARG120","TYR355","SER530","GLY526","LEU352","VAL349","TRP387","HIS90"]
            interaction_types = ["Hydrogen Bond", "Hydrophobic", "Van der Waals", "Pi-Pi Stacking"]
            res_df = pd.DataFrame([{"Residue": r, "Interaction": random.choice(interaction_types)} for r in residues])
            st.subheader("Key Binding Residues")
            st.table(res_df)

# -------------------------------------------------
# 3. CUSTOM DOCKING
# -------------------------------------------------
elif module == "Custom Docking Simulator":
    st.header("Custom Docking Simulator")
    drug = st.text_input("Drug Name")
    protein = st.text_input("Target Protein")
    energy = st.number_input("Binding Energy", value=-7.5)
    residues = st.text_input("Residues (comma separated)")
    interaction = st.selectbox("Interaction Type", ["Hydrogen Bond","Hydrophobic","Electrostatic","Pi-Pi Stacking"])

    if st.button("Simulate"):
        df = pd.DataFrame({"Drug":[drug], "Protein":[protein], "Energy":[energy], "Interaction":[interaction], "Residues":[residues]})
        st.dataframe(df)

# -------------------------------------------------
# 4. DOSE RESPONSE (CONNECTED LOGIC)
# -------------------------------------------------
elif module == "Dose Response Simulator":
    st.header("📈 Connected Pharmacodynamics Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_name = st.text_input("Compound Name", "Experimental Lead")
        target_protein = st.selectbox("Select Target Protein", protein_list)
        user_energy = st.number_input("Enter Binding Energy (kcal/mol)", value=-9.0, step=0.1)
        
        # Potency and Efficacy calculation based on Energy
        calc_ec50 = np.interp(user_energy, [-12, -5], [1, 150])
        calc_emax = np.interp(user_energy, [-12, -5], [100, 70])
        
        st.metric("Predicted EC50", f"{round(calc_ec50, 2)} nM")
        st.metric("Predicted Emax", f"{round(calc_emax, 1)} %")

    with col2:
        # Determine Hill Coefficient based on Protein Type
        p_type = protein_categories.get(target_protein, "Enzyme")
        
        if p_type in ["Receptor", "Transcription Factor"]:
            auto_hill = 2.5
        elif p_type == "Kinase":
            auto_hill = 1.5
        else:
            auto_hill = 1.0
            
        st.write(f"**Target Analysis:** {target_protein} is a **{p_type}**.")
        hill_coeff = st.slider("Hill Coefficient (nH)", 0.5, 4.0, float(auto_hill))
        st.write("---")
        st.info(f"The Hill Coefficient was auto-set to {auto_hill} because {target_protein} is a {p_type}.")

    # Generate Hill Equation Curve
    conc = np.logspace(-1, 3, 100) 
    response = (calc_emax * (conc**hill_coeff)) / ( (calc_ec50**hill_coeff) + (conc**hill_coeff) )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=conc, y=response, mode='lines', line=dict(color='#00CC96', width=4)))
    fig.update_layout(
        title=f"Dose-Response: {drug_name} acting on {target_protein}",
        xaxis=dict(title="Concentration (nM) [Log Scale]", type="log"),
        yaxis=dict(title="Response (%)", range=[0, 110]),
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# -------------------------------------------------
# 5. PROTEIN PATHWAY SIMULATOR (THE IMPACT)
# -------------------------------------------------
elif module == "Protein Pathway Simulator":
    st.header("⚡ Step 3: Pathway Impact Analysis")
    
    # 1. DATA PULL (Connecting to the Screening result)
    energy = st.session_state.selected_energy
    target = st.session_state.selected_target
    drug_name = st.session_state.selected_drug

    st.info(f"🔬 **Analyzing Lead:** {drug_name} | **Primary Target:** {target}")

    # 2. AUTOMATION LOGIC
    # Map Energy to Inhibition (Stronger energy = Higher starting bar)
    inhibition = np.interp(energy, [-12, -4], [100, 20])
    p_type = protein_categories.get(target, "Enzyme")
    # Complexity of the chain depends on protein type
    depth = 5 if p_type in ["Receptor", "Transcription Factor", "Growth Factor"] else 3

    # 3. THE BAR GRAPH (Scientific View)
    st.subheader("📊 Signal Decay Graph")
    steps = [f"Step {i+1}" for i in range(depth)]
    signal_values = [inhibition * (0.8**i) for i in range(depth)]

    fig_bar = go.Figure(go.Bar(
        x=steps, 
        y=signal_values, 
        marker_color='firebrick',
        text=[f"{round(s)}%" for s in signal_values],
        textposition='auto'
    ))
    fig_bar.update_layout(
        title=f"Inhibition Strength: {drug_name} Cascade",
        yaxis=dict(title="Remaining Signal (%)", range=[0, 100]),
        template="plotly_white",
        height=350
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 4. THE INTERACTIVE MAP (Visual View)
    st.subheader("🔗 Biological Chain Interaction")
    path_net = Network(height="400px", width="100%", bgcolor="#ffffff", font_color="black", directed=True)
    
    # Create a unique chain based on the selected target
    chain = [target] + random.sample([p for p in protein_list if p != target], depth - 1)
    
    for i in range(len(chain)):
        strength = inhibition * (0.8**i)
        n_color = "#ff4b4b" if i == 0 else "#1c83e1" # Red for target, Blue for others
        path_net.add_node(chain[i], label=f"{chain[i]}\n{round(strength)}%", color=n_color, size=25 if i==0 else 18)
        if i > 0:
            path_net.add_edge(chain[i-1], chain[i], width=3, color="#848484", arrows="to")

    path_net.toggle_physics(True)
    path_net.save_graph("pathway_map.html")
    with open("pathway_map.html", 'r', encoding='utf-8') as f:
        components.html(f.read(), height=450)

    # 5. AUTOMATED INTERPRETATION
    st.divider()
    final_impact = signal_values[-1]
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        ### 🧐 Understanding the Graph
        * **The Drop:** Your drug starts at **{round(inhibition)}%** inhibition. Because biology isn't perfect, the signal drops **20%** at every step.
        * **The Logic:** In a **{p_type}** pathway, there are **{depth} steps** before the final biological effect is achieved.
        """)
    with col_b:
        st.markdown(f"### 🧪 The Verdict")
        if final_impact > 50:
            st.success(f"**POTENT:** {drug_name} is strong enough to maintain a **{round(final_impact)}%** effect at the end of the chain.")
        else:
            st.warning(f"**WEAK:** The effect drops to **{round(final_impact)}%**. This lead may need further chemical optimization.")
# -------------------------------------------------
# 6. VIRTUAL DRUG SCREENING (THE DISCOVERY)
# -------------------------------------------------

           elif module == "Virtual Drug Screening":
    st.header("🧪 Advanced Screening & Lead Selection")
    
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
        
        # NEW: The connection point
        st.subheader("Connect to Research Pipeline")
        selection = st.selectbox("Pick a Lead Compound to test in other modules:", df['Drug'])
        if st.button("Set as Active Lead"):
            row = df[df['Drug'] == selection].iloc[0]
            st.session_state.selected_drug = row['Drug']
            st.session_state.selected_energy = row['Energy']
            st.session_state.selected_target = row['Target']
            st.success(f"Linked {selection} to Dose-Response and Pathway Simulators!")
