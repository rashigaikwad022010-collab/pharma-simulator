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
# 5. PROTEIN PATHWAY
# -------------------------------------------------
elif module == "Protein Pathway Simulator":
    st.header("Protein Pathway Network")
    drug = st.text_input("Drug", "Aspirin")
    proteins = st.multiselect("Select Proteins", protein_list, default=["COX2", "TNF"])

    if st.button("Generate Network"):
        G = nx.Graph()
        G.add_node(drug)
        for p in proteins:
            G.add_node(p)
            G.add_edge(drug, p)
        fig, ax = plt.subplots()
        nx.draw(G, with_labels=True, node_color="lightblue", node_size=2500, font_weight='bold')
        st.pyplot(fig)

# -------------------------------------------------
# 6. VIRTUAL SCREENING
# -------------------------------------------------
elif module == "Virtual Drug Screening":
    st.header("Virtual Drug Screening")
    if st.button("Start Screening"):
        drugs = random.sample(drug_list, 10)
        prots = random.sample(protein_list, 5)
        results = []
        for d in drugs:
            for p in prots:
                energy = round(random.uniform(-10.5, -4.0), 2)
                results.append([d, p, energy])
        df = pd.DataFrame(results, columns=["Drug", "Protein", "Binding Energy"])
        st.dataframe(df.style.background_gradient(subset=['Binding Energy'], cmap='RdYlGn_r'))
        best = df.sort_values("Binding Energy").head(5)
        st.subheader("Top Binding Results (Leads)")
        st.dataframe(best)
