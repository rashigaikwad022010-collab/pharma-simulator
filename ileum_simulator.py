import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Drug Discovery Simulator", layout="wide")

st.title("🧬 Pharmaceutical Drug Discovery Simulator")

st.sidebar.title("Select Module")

module = st.sidebar.radio(
    "Modules",
    [
        "Network Pharmacology Explorer",
        "Molecular Docking Simulator"
    ]
)

# ------------------------------------------------
# NETWORK PHARMACOLOGY MODULE
# ------------------------------------------------

if module == "Network Pharmacology Explorer":

    st.header("Network Pharmacology Explorer")

    st.write("Explore how a drug interacts with multiple biological targets.")

    drug = st.selectbox(
        "Select Drug Compound",
        ["Curcumin", "Resveratrol", "Quercetin", "Aspirin"]
    )

    targets = {
        "Curcumin": ["NF-kB", "COX-2", "AKT1", "STAT3"],
        "Resveratrol": ["SIRT1", "AMPK", "NF-kB"],
        "Quercetin": ["PI3K", "MAPK", "TNF-alpha"],
        "Aspirin": ["COX-1", "COX-2", "NF-kB"]
    }

    selected_targets = targets[drug]

    st.subheader("Drug–Target Interaction Network")

    nodes = ["Drug"] + selected_targets

    x = np.linspace(0, 1, len(nodes))
    y = np.random.rand(len(nodes))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers+text",
            text=nodes,
            textposition="top center",
            marker=dict(size=20)
        )
    )

    fig.update_layout(
        title="Drug Target Network",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Target Proteins")

    df = pd.DataFrame({
        "Drug": [drug]*len(selected_targets),
        "Target Protein": selected_targets
    })

    st.table(df)


# ------------------------------------------------
# MOLECULAR DOCKING MODULE
# ------------------------------------------------

elif module == "Molecular Docking Simulator":

    st.header("Molecular Docking Simulator")

    st.write("Simulate ligand binding with target proteins.")

    ligand = st.selectbox(
        "Select Ligand",
        ["Curcumin", "Ibuprofen", "Quercetin", "Resveratrol"]
    )

    protein = st.selectbox(
        "Select Target Protein",
        ["COX-2", "EGFR", "TNF-alpha", "AKT1"]
    )

    if st.button("Run Docking Simulation"):

        np.random.seed(len(ligand)+len(protein))

        binding_energy = -np.random.uniform(5,10)

        interactions = [
            "Hydrogen Bonds",
            "Hydrophobic Interactions",
            "Van der Waals Forces",
            "Pi-Pi Stacking"
        ]

        st.subheader("Docking Results")

        st.success(f"Binding Energy: {round(binding_energy,2)} kcal/mol")

        st.write("Ligand:", ligand)
        st.write("Protein:", protein)

        st.subheader("Predicted Interactions")

        for i in interactions:
            st.write("-", i)

        residues = ["ARG120", "TYR355", "SER530", "GLY526"]

        df = pd.DataFrame({
            "Protein Residue": residues,
            "Interaction Type": ["Hydrogen Bond"]*4
        })

        st.table(df)
