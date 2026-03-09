import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Pharmaceutical Drug Discovery Simulator", layout="wide")

st.title("🧬 Pharmaceutical Drug Discovery Simulator")

st.sidebar.title("Modules")

module = st.sidebar.radio(
    "Select Module",
    [
        "Network Pharmacology Explorer",
        "Molecular Docking Simulator"
    ]
)

# ----------------------------------------------------------------
# DRUG DATABASE (80 COMMON DRUGS)
# ----------------------------------------------------------------

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

# ----------------------------------------------------------------
# NETWORK PHARMACOLOGY MODULE
# ----------------------------------------------------------------

if module == "Network Pharmacology Explorer":

    st.header("Network Pharmacology Explorer")

    st.write("Select a drug to explore its predicted biological targets.")

    drug = st.selectbox(
        "Select Drug",
        drug_list
    )

    targets = [
        "COX-2","NF-kB","AKT1","STAT3",
        "MAPK1","EGFR","TNF-alpha",
        "PI3K","mTOR","JAK2"
    ]

    selected_targets = random.sample(targets, 4)

    nodes = ["Drug"] + selected_targets

    x_positions = [0] + [1]*len(selected_targets)
    y_positions = [0] + list(np.linspace(-1,1,len(selected_targets)))

    fig = go.Figure()

    # draw edges
    for i in range(1,len(nodes)):

        fig.add_trace(go.Scatter(
            x=[x_positions[0], x_positions[i]],
            y=[y_positions[0], y_positions[i]],
            mode="lines",
            line=dict(width=2,color="gray"),
            showlegend=False
        ))

    # draw nodes
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=y_positions,
        mode="markers+text",
        text=nodes,
        textposition="top center",
        marker=dict(size=25,color="blue")
    ))

    fig.update_layout(
        title="Drug–Target Interaction Network",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Predicted Target Proteins")

    df = pd.DataFrame({
        "Drug":[drug]*len(selected_targets),
        "Target Protein":selected_targets
    })

    st.table(df)

# ----------------------------------------------------------------
# MOLECULAR DOCKING MODULE
# ----------------------------------------------------------------

elif module == "Molecular Docking Simulator":

    st.header("Molecular Docking Simulator")

    ligand = st.selectbox(
        "Select Ligand (Drug Molecule)",
        drug_list
    )

    proteins = [
        "COX-2","EGFR","TNF-alpha","AKT1",
        "MAPK1","PI3K","JAK2","mTOR"
    ]

    protein = st.selectbox(
        "Select Target Protein",
        proteins
    )

    if st.button("Run Docking Simulation"):

        np.random.seed(len(ligand)+len(protein))

        poses = 5

        energies = -np.sort(np.random.uniform(5,10,poses))

        docking_df = pd.DataFrame({
            "Pose":range(1,poses+1),
            "Binding Energy (kcal/mol)":energies
        })

        st.subheader("Docking Results")

        st.write("Ligand:", ligand)
        st.write("Target Protein:", protein)

        st.table(docking_df)

        interactions = [
            "Hydrogen Bonds",
            "Hydrophobic Interactions",
            "Van der Waals Forces",
            "Pi-Pi Stacking"
        ]

        st.subheader("Predicted Interaction Types")

        for i in interactions:
            st.write("-", i)

        residues = ["ARG120","TYR355","SER530","GLY526","LEU352"]

        interaction_df = pd.DataFrame({
            "Residue":residues,
            "Interaction Type":"Hydrogen Bond"
        })

        st.subheader("Key Binding Residues")

        st.table(interaction_df)
