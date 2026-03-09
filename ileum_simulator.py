import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(page_title="Pharmaceutical Research Simulator", layout="wide")

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
# DRUG DATABASE
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

protein_list = [
"COX2","AKT1","MAPK1","PI3K","mTOR","EGFR","JAK2","STAT3","NFkB",
"TNF","IL6","BRAF","MEK1","ERK2","SRC","VEGFA","HIF1A","TP53",
"CDK2","CDK4","GSK3B","PTEN","FOXO3","MYC","CASP3","CASP9",
"MMP9","NOS3","CXCL8","TGFb1"
]

# -------------------------------------------------
# NETWORK PHARMACOLOGY
# -------------------------------------------------

if module == "Network Pharmacology Explorer":

    st.header("Network Pharmacology Explorer")

    drug = st.selectbox("Select Drug", drug_list)

    proteins = random.sample(protein_list, 20)

    nodes = ["Drug"] + proteins

    x = np.random.rand(len(nodes))
    y = np.random.rand(len(nodes))

    fig = go.Figure()

    # drug-target edges
    for i in range(1,len(nodes)):
        fig.add_trace(go.Scatter(
            x=[x[0],x[i]],
            y=[y[0],y[i]],
            mode="lines",
            line=dict(color="gray"),
            showlegend=False
        ))

    # protein interactions
    for i in range(1,len(nodes)):
        for j in range(i+1,len(nodes)):
            if random.random() < 0.2:
                fig.add_trace(go.Scatter(
                    x=[x[i],x[j]],
                    y=[y[i],y[j]],
                    mode="lines",
                    line=dict(color="lightgray"),
                    showlegend=False
                ))

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers+text",
        text=nodes,
        textposition="top center",
        marker=dict(size=18,color="blue")
    ))

    fig.update_layout(
        title="Drug–Protein Interaction Network",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=600
    )

    st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------
# MOLECULAR DOCKING
# -------------------------------------------------

elif module == "Molecular Docking Simulator":

    st.header("Molecular Docking Simulator")

    ligand = st.selectbox("Select Ligand",drug_list)
    protein = st.selectbox("Target Protein",protein_list)

    if st.button("Run Docking"):

        poses = 8

        energies = -np.sort(np.random.uniform(5,12,poses))

        df = pd.DataFrame({
            "Pose":range(1,poses+1),
            "Binding Energy (kcal/mol)":energies
        })

        st.subheader("Docking Poses")
        st.table(df)

        residues = [
        "ARG120","TYR355","SER530","GLY526",
        "LEU352","VAL349","TRP387","HIS90"
        ]

        interaction_types = [
        "Hydrogen Bond",
        "Hydrophobic Interaction",
        "Van der Waals",
        "Pi-Pi Stacking",
        "Salt Bridge",
        "Pi-Cation Interaction"
        ]

        data=[]

        for r in residues:
            data.append({
                "Residue":r,
                "Interaction":random.choice(interaction_types)
            })

        res_df = pd.DataFrame(data)

        st.subheader("Key Binding Residues")
        st.table(res_df)

# -------------------------------------------------
# CUSTOM DOCKING
# -------------------------------------------------

elif module == "Custom Docking Simulator":

    st.header("Custom Docking Simulator")

    drug = st.text_input("Drug Name")
    protein = st.text_input("Target Protein")
    energy = st.number_input("Binding Energy",value=-7.5)

    residues = st.text_input("Residues (comma separated)")
    interaction = st.selectbox(
        "Interaction Type",
        ["Hydrogen Bond","Hydrophobic","Electrostatic","Pi-Pi Stacking"]
    )

    if st.button("Simulate"):

        df = pd.DataFrame({
            "Drug":[drug],
            "Protein":[protein],
            "Energy":[energy],
            "Interaction":[interaction],
            "Residues":[residues]
        })

        st.dataframe(df)

# -------------------------------------------------
# DOSE RESPONSE
# -------------------------------------------------

elif module == "Dose Response Simulator":

    st.header("Dose Response Simulator")

    drug = st.text_input("Drug")

    ec50 = st.slider("EC50",1,100,50)
    max_effect = st.slider("Max Effect (%)",10,100,90)

    concentration = np.linspace(0.1,100,100)

    effect = (max_effect*concentration)/(ec50+concentration)

    fig, ax = plt.subplots()

    ax.plot(concentration,effect)

    ax.set_xlabel("Concentration")
    ax.set_ylabel("Effect %")
    ax.set_title(f"Dose Response Curve for {drug}")

    st.pyplot(fig)

# -------------------------------------------------
# PATHWAY NETWORK
# -------------------------------------------------

elif module == "Protein Pathway Simulator":

    st.header("Protein Pathway Network")

    drug = st.text_input("Drug")

    proteins = st.multiselect(
        "Select Proteins",
        protein_list
    )

    if st.button("Generate Network"):

        G = nx.Graph()

        G.add_node(drug)

        for p in proteins:
            G.add_node(p)
            G.add_edge(drug,p)

        pos = nx.spring_layout(G)

        fig, ax = plt.subplots()

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=2000
        )

        st.pyplot(fig)

# -------------------------------------------------
# VIRTUAL SCREENING
# -------------------------------------------------

elif module == "Virtual Drug Screening":

    st.header("Virtual Drug Screening")

    drugs = random.sample(drug_list,10)
    proteins = random.sample(protein_list,5)

    results=[]

    for d in drugs:
        for p in proteins:
            energy=round(random.uniform(-10,-4),2)
            results.append([d,p,energy])

    df = pd.DataFrame(
        results,
        columns=["Drug","Protein","Binding Energy"]
    )

    st.dataframe(df)

    best=df.sort_values("Binding Energy").head(5)

    st.subheader("Top Binding Results")

    st.dataframe(best)
