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
# -------------------------------------------------
# 5. PROTEIN PATHWAY SIMULATOR (THE IMPACT)
# -------------------------------------------------
elif module == "Protein Pathway Simulator":
    st.header("⚡ Advanced Signal Cascade & Impact Analysis")
    
    # --- 1. AUTOMATED INPUTS ---
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Configuration")
        energy_input = st.number_input("Enter Binding Energy (kcal/mol)", value=-7.0, max_value=0.0, step=0.1)
        target_p = st.selectbox("Select Primary Target", protein_list)
        
        # LOGIC: Convert Energy to Inhibition %
        # -12 kcal/mol (Very Strong) -> 100%, -4 kcal/mol (Weak) -> 20%
        auto_inhibition = np.interp(energy_input, [-12, -4], [100, 20])
        p_type = protein_categories.get(target_p, "Enzyme")
        # Receptors trigger long cascades (5 steps), Enzymes are usually direct (3 steps)
        auto_depth = 5 if p_type in ["Receptor", "Transcription Factor", "Growth Factor"] else 3
        
        st.info(f"**Target Class:** {p_type}\n\n**Calculated Hit:** {round(auto_inhibition)}% inhibition at source.")

    # --- 2. INTERACTIVE VISUALIZATION ---
    with col2:
        st.subheader("Molecular Chain Interaction")
        path_net = Network(height="400px", width="100%", bgcolor="#ffffff", font_color="black", directed=True)
        
        # Create a logical chain of proteins
        chain = [target_p] + random.sample([p for p in protein_list if p != target_p], auto_depth - 1)
        
        for i in range(len(chain)):
            strength = auto_inhibition * (0.8**i) # 20% decay per step
            
            # Color logic: Red for target, Blue for downstream
            n_color = "#ff4b4b" if i == 0 else "#1c83e1"
            n_size = 30 if i == 0 else 20
            
            path_net.add_node(
                chain[i], 
                label=f"{chain[i]}\n{round(strength)}%", 
                title=f"Protein: {chain[i]} | Signal: {round(strength)}%",
                color=n_color,
                size=n_size,
                shape="dot"
            )
            
            if i > 0:
                path_net.add_edge(chain[i-1], chain[i], width=3, color="#848484", arrows="to")

        path_net.toggle_physics(True)
        path_net.save_graph("pathway_map.html")
        HtmlFile = open("pathway_map.html", 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=450)

    # --- 3. THE "WHAT DOES THIS MEAN?" SECTION ---
    st.divider()
    st.subheader("📊 Results Interpretation")
    
    final_impact = auto_inhibition * (0.8**(auto_depth-1))
    
    detail_col1, detail_col2 = st.columns(2)
    
    with detail_col1:
        st.markdown(f"""
        ### What the Graph Says:
        * **The Red Node ({target_p}):** This is where your drug binds. At **{energy_input} kcal/mol**, it successfully shuts down **{round(auto_inhibition)}%** of this protein's activity.
        * **The Blue Nodes:** These are 'downstream' proteins. They don't touch the drug, but they lose power because the first protein is blocked.
        * **Signal Decay:** Every arrow represents a loss of biological signal. Your model assumes a **20% loss** of efficiency at every step in the chain.
        """)

    with detail_col2:
        st.markdown(f"""
        ### The Pathway Verdict:
        * **Final Physiological Impact:** {round(final_impact)}%
        * **Clinical Outlook:** """)
        if final_impact > 60:
            st.success("✅ **High Efficacy:** The drug is strong enough to trigger a major biological change even through a long pathway.")
        elif final_impact > 30:
            st.warning("⚠️ **Moderate Efficacy:** The effect is significantly weakened. Consider a higher dose or a stronger binding lead.")
        else:
            st.error("❌ **Low Efficacy:** The signal 'dies' before reaching the end of the pathway. This drug may fail in clinical trials.")
 
      
       

# -------------------------------------------------
# 6. VIRTUAL DRUG SCREENING (THE DISCOVERY)
# -------------------------------------------------
elif module == "Virtual Drug Screening":
    st.header("🧪 Advanced Virtual Screening & ADME")
    st.write("Screening for Binding Affinity + Drug-Likeness (Lipinski's Rules)")

    if st.button("🚀 Run High-Throughput Screen"):
        test_drugs = random.sample(drug_list, 10)
        target = random.choice(protein_list)
        
        results = []
        for d in test_drugs:
            energy = round(random.uniform(-11.0, -4.0), 2)
            # Creative Approach: Add "Drug-Likeness" scores
            mw = random.randint(200, 600) # Molecular Weight
            logp = round(random.uniform(1, 6), 1) # Lipophilicity
            
            # Check Lipinski's Rule (Simplified)
            pass_rules = "✅ Pass" if mw < 500 and logp < 5 else "❌ Fail"
            
            results.append([d, target, energy, mw, logp, pass_rules])

        df = pd.DataFrame(results, columns=["Drug", "Target", "Energy", "Mol. Weight", "LogP", "Lipinski Status"])
        
        # Highlight the best candidates that also pass the rules
        st.subheader(f"Screening Results for {target}")
        st.dataframe(df.style.apply(lambda x: ['background-color: lightgreen' if x['Lipinski Status'] == "✅ Pass" and x['Energy'] < -8 else '' for i in x], axis=1))
        
        st.success("Analysis Complete: Green rows represent 'Strong Binders' that are also safe for human absorption.")
