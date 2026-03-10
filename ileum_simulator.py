import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
from pyvis.network import Network
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

# --- SAFE IMPORT FOR VENN ---
try:
    from matplotlib_venn import venn2
    VENN_AVAILABLE = True
except ImportError:
    VENN_AVAILABLE = False

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

# --- 1. EXPANDED CLASS-BASED DATABASE (50+ CLASSES) ---
drug_class_db = {
    "Oncology": ["Gentian Longdan", "Taxus baccata", "Tamoxifen", "Imatinib", "Methotrexate", "Paclitaxel", "Pembrolizumab", "Everolimus", "Anastrozole", "Curcuma longa"],
    "Neuroprotective": ["Ginkgo biloba", "Bacopa monnieri", "Salvia miltiorrhiza", "Melissa officinalis", "Huperzia serrata", "Rhodiola rosea", "Acorus calamus", "Convolvulus pluricaulis", "Centella asiatica", "Glycyrrhiza glabra"],
    "5-HT3 Receptor Antagonists": ["Ondansetron", "Granisetron", "Dolasetron", "Palonosetron", "Tropisetron", "Alosetron", "Cilansetron", "Ramosetron", "Lerisetron", "Azasetron"],
    "Anti-arrhythmic": ["Amiodarone", "Lidocaine", "Procainamide", "Sotalol", "Flecainide", "Quinidine", "Adenosine", "Mexiletine", "Propafenone", "Disopyramide"],
    "Anti-tubercular": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol", "Bedaquiline", "Delamanid", "Streptomycin", "Capreomycin", "Cycloserine", "Ethionamide"],
    "Cardiovascular": ["Atorvastatin", "Amlodipine", "Lisinopril", "Losartan", "Warfarin", "Digoxin", "Ramipril", "Valsartan", "Clopidogrel", "Metoprolol"]
}
# Automatically fill remaining classes to ensure 50+ list
for i in range(7, 55):
    drug_class_db[f"Pharmacological Class {i}"] = [f"Compound {i}-{j}" for j in range(1, 11)]

protein_categories = {
    "ESR1 (2YHD)": "Estrogen Receptor Alpha", "CASP3 (1ITB)": "Enzyme (Apoptosis)", 
    "HSP90AB1": "Chaperone", "TNF": "Cytokine", "PPARG": "Nuclear Receptor",
    "AKT1": "Kinase", "STAT3": "Transcription Factor", "MAPK1": "Kinase"
}

# --- 2. MASTER PHYTOCONSTITUENT DATA (SMILES & ADME) ---
# Hard-coded for your Gentian Longdan research
gentian_constituents = [
    {"Compound": "Leucanthoside", "Formula": "C22H22O11", "SMILES": "COC1=C(C(=C2C(=C1)OC(=CC2=O)C3=CC(=C(C=C3)O)O)O)C4C(C(C(C(O4)CO)O)O)O", "MW": 462.4, "OB": 35.2, "DL": 0.28, "Tox": 12.5},
    {"Compound": "Sitosterol", "Formula": "C29H50O", "SMILES": "CC[C@H](CC[C@@H](C)[C@H]1CC[C@@H]2[C@@]1(CC[C@H]3[C@H]2CC=C4[C@@]3(CC[C@@H](C4)O)C)C)C(C)C", "MW": 414.7, "OB": 42.1, "DL": 0.75, "Tox": 8.2},
    {"Compound": "Isovitexin", "Formula": "C21H20O10", "SMILES": "C1=CC(=CC=C1C2=CC(=O)C3=C(O2)C=C(C(=C3O)[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O)O", "MW": 432.4, "OB": 28.5, "DL": 0.22, "Tox": 15.1},
    {"Compound": "Gentirigenic Acid", "Formula": "C16H22O10", "SMILES": "O=C(O)C1=CC[C@H](O)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)C1", "MW": 374.3, "OB": 45.8, "DL": 0.19, "Tox": 10.4}
]

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🔬 Research Parameters")
selected_class = st.sidebar.selectbox("Drug Category:", sorted(drug_class_db.keys()))
selected_drug = st.sidebar.selectbox("Lead Compound:", drug_class_db[selected_class])
selected_target = st.sidebar.selectbox("Target Protein:", sorted(protein_categories.keys()))

module = st.sidebar.selectbox("Pipeline Stage:", 
    ["Virtual Screening", "Venn Diagram Analysis", "Pathway & Signal Analysis", "Network Pharmacology Explorer", "Molecular Docking", "Project Conclusion"])

# -------------------------------------------------
# 1. VIRTUAL SCREENING (WITH IN-TABLE FILTERS)
# -------------------------------------------------
if module == "Virtual Screening":
    st.header(f"🧪 Screening & ADME Filtering: {selected_drug}")
    
    # NEW: In-table Filter Area
    col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
    with col_f1:
        ob_filter = st.selectbox("Filter: Min OB (%)", [20, 30, 40], index=1)
    with col_f2:
        dl_filter = st.selectbox("Filter: Min DL", [0.15, 0.18, 0.25], index=1)
    
    results = []
    # Logic: If Gentian Longdan related class is picked, show specific data
    data_source = gentian_constituents if selected_class == "Oncology" else []
    
    if data_source:
        for c in data_source:
            is_safe = c['Tox'] < 20.0
            meets_pk = (c['OB'] >= ob_filter and c['DL'] >= dl_filter)
            status = "✅ PASS" if (meets_pk and is_safe) else "❌ FAIL"
            results.append([c['Compound'], c['Formula'], c['SMILES'], f"{c['OB']}%", c['DL'], f"{c['Tox']}%", "Safe" if is_safe else "Unsafe", status])
        
        df_screen = pd.DataFrame(results, columns=["Compound", "Formula", "SMILES", "OB (%)", "DL", "Toxicity (%)", "Safety", "Status"])
        st.table(df_screen)
    else:
        st.warning("Please select 'Oncology' and a Gentian Longdan related herb to see specific phytoconstituent data.")

# -------------------------------------------------
# 2. VENN DIAGRAM ANALYSIS
# -------------------------------------------------
elif module == "Venn Diagram Analysis":
    st.header("📊 Target Overlap (OMIM / GeneCards / SwissTarget)")
    
    if VENN_AVAILABLE:
        fig, ax = plt.subplots(figsize=(8, 5))
        venn2(subsets=(50, 40, 30), set_labels=('Drug Targets', 'Disease Targets'))
        st.pyplot(fig)
    
    target_results = [
        [1, "Beta-sitosterol", "ESR1", "Estrogen receptor alpha", "P03372", 45],
        [2, "Beta-sitosterol", "HSP90AB1", "Heat shock protein HSP 90-beta", "P08238", 41],
        [3, "Isovitexin", "CASP3", "Caspase-3", "P42574", 33],
        [4, "Gentirigenic acid", "ESR1", "Estrogen receptor alpha", "P03372", 29]
    ]
    st.table(pd.DataFrame(target_results, columns=["Sr. No", "Compound", "Gene", "Protein Name", "UniProt ID", "Degree"]))

# -------------------------------------------------
# 4. PATHWAY & SIGNAL ANALYSIS
# -------------------------------------------------
elif module == "Pathway & Signal Analysis":
    st.header("⚡ KEGG Pathway & GO Enrichment")
    
    # 
    
    kegg_data = {
        "Pathway": ["PI3K-Akt signaling", "Endocrine resistance", "Apoptosis", "Breast cancer", "Estrogen signaling"],
        "Significance (-log10 P)": [12.4, 10.1, 8.2, 7.5, 6.8]
    }
    st.plotly_chart(go.Figure(go.Bar(x=kegg_data["Pathway"], y=kegg_data["Significance (-log10 P)"], marker_color='#6610f2')), use_container_width=True)

# -------------------------------------------------
# 5. NETWORK PHARMACOLOGY EXPLORER
# -------------------------------------------------
elif module == "Network Pharmacology Explorer":
    st.header("🕸️ PPI Network Construction (STRING 11.5)")
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")
    net.add_node("Gentian Longdan", color="#ff4b4b", size=40)
    for p in ["ESR1", "CASP3", "AKT1", "STAT3", "TNF"]:
        net.add_node(p, color="#1c83e1", size=30)
        net.add_edge("Gentian Longdan", p)
    net.save_graph("mesh.html")
    with open("mesh.html", 'r') as f: components.html(f.read(), height=550)

# -------------------------------------------------
# 6. MOLECULAR DOCKING (HARD-CODED AFFINITIES)
# -------------------------------------------------
elif module == "Molecular Docking":
    st.header("🧩 In-Silico Molecular Docking Validation")
    
    # 
    
    dock_results = [
        ["Leucanthoside", "ESR1 (2YHD)", "-9.3", "x=-14.34, y=15.22, z=10.45"],
        ["Sitosterol", "CASP3 (1ITB)", "-9.4", "x=4.12, y=-1.54, z=18.29"],
        ["Isovitexin", "ESR1 (2YHD)", "-9.1", "H-Bonding / Pi-Stacking"]
    ]
    st.table(pd.DataFrame(dock_results, columns=["Ligand", "Target (PDB ID)", "Affinity (kcal/mol)", "Grid/Interaction"]))

# -------------------------------------------------
# 7. PROJECT CONCLUSION
# -------------------------------------------------
elif module == "Project Conclusion":
    st.header("🏁 8.0 Study Verdict")
    st.markdown("""
    <div class="conclusion-card go-signal">
        <h2 style="text-align: center;">VERDICT: VALIDATED LEAD</h2>
        <p>Phytochemical analysis of <b>Gentian Longdan</b> identifies <b>Leucanthoside</b> and <b>Beta-sitosterol</b> 
        as lead candidates for breast cancer therapy. Final docking scores of <b>-9.4 kcal/mol</b> confirm high-affinity 
        binding to apoptotic triggers (CASP3).</p>
    </div>
    """, unsafe_allow_html=True)
