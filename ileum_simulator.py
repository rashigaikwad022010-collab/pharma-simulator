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

# -----------------------------------------------------
# LARGE DRUG DATABASE
# -----------------------------------------------------

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

# -----------------------------------------------------
# PROTEIN DATABASE (30+ PROTEINS)
# -----------------------------------------------------

protein_list = [
"COX2","AKT1","MAPK1","PI3K","mTOR","EGFR","JAK2","STAT3","NFkB",
"TNF","IL6","BRAF","MEK1","ERK2","SRC","VEGFA","HIF1A","TP53",
"CDK2","CDK4","GSK3B","PTEN","FOXO3","MYC","CASP3","CASP9",
"MMP9","NOS3","CXCL8","TGFb1"
]

# -----------------------------------------------------
# NETWORK PHARMACOLOGY MODULE
# -----------------------------------------------------

if module == "Network Pharmacology Explorer":

    st.header("Network Pharmacology Explorer")

    drug = st.selectbox("Select Drug", drug_list)

    # choose 20 proteins
    selected_proteins = random.sample(protein_list, 20)

    nodes = ["Drug"] + selected_proteins

    x = np.random.rand(len(nodes))
    y = np.random.rand(len(nodes))

    fig = go.Figure()

    # Drug → protein connections
    for i in range(1, len(nodes)):
        fig.add_trace(go.Scatter(
            x=[x[0], x[i]],
            y=[y[0], y[i]],
            mode="lines",
            line=dict(width=2, color="gray"),
            showlegend=False
        ))

    # protein–protein interactions
    for i in range(1, len(nodes)):
        for j in range(i+1, len(nodes)):
            if random.random() < 0.15:
                fig.add_trace(go.Scatter(
                    x=[x[i], x[j]],
                    y=[y[i], y[j]],
                    mode="lines",
                    line=dict(width=1, color="lightgray"),
                    showlegend=False
                ))

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers+text",
        text=nodes,
        textposition="top center",
        marker=dict(size=20,color="blue")
    ))

    fig.update_layout(
        title="Complex Drug–Protein Interaction Network",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Predicted Target Proteins")

    df = pd.DataFrame({
        "Drug":[drug]*len(selected_proteins),
        "Protein":selected_proteins
    })

    st.table(df)

# -----------------------------------------------------
# MOLECULAR DOCKING MODULE
# -----------------------------------------------------

elif module == "Molecular Docking Simulator":

    st.header("Molecular Docking Simulator")

    ligand = st.selectbox("Select Ligand", drug_list)

    protein = st.selectbox("Select Target Protein", protein_list)

    if st.button("Run Docking Simulation"):

        np.random.seed(len(ligand)+len(protein))

        poses = 8

        energies = -np.sort(np.random.uniform(5,12,poses))

        docking_df = pd.DataFrame({
            "Pose":range(1,poses+1),
            "Binding Energy (kcal/mol)":energies
        })

        st.subheader("Docking Poses")

        st.table(docking_df)

        # realistic residue list
        residues = [
        "ARG120","TYR355","SER530","GLY526","LEU352","VAL349",
        "ALA527","TRP387","HIS90","LYS83"
        ]

        interaction_types = [
        "Hydrogen Bond",
        "Hydrophobic Interaction",
        "Van der Waals",
        "Pi-Pi Stacking",
        "Salt Bridge",
        "Pi-Cation Interaction"
        ]

        interaction_data = []

        for r in residues:

            interaction_data.append({
                "Residue": r,
                "Interaction": random.choice(interaction_types)
            })

        interaction_df = pd.DataFrame(interaction_data)

        st.subheader("Key Binding Residues")

        st.table(interaction_df)
