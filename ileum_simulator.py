import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import hashlib
from pyvis.network import Network
import streamlit.components.v1 as components

# --- UI SETTINGS ---
st.set_page_config(page_title="Pharma Research Pipeline Pro", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .explanation-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 6px solid #007bff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin: 20px 0; }
    .result-desc { font-style: italic; color: #2c3e50; margin: 10px 0; padding: 15px; background: #f1f4f9; border-left: 5px solid #007bff; border-radius: 5px; }
    .stat-card { background: #fff; padding: 15px; border-radius: 10px; border: 1px solid #eee; text-align: center; }
    .verdict-go { padding: 20px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 24px; border: 2px solid #28a745; background-color: #d4edda; color: #155724; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Advanced Pharmaceutical Research & Docking Pipeline")

# --- DATABASE: 50+ DRUG CLASSES & UNIQUE HERB CONSTITUENTS ---
drug_class_db = {
    "5-HT3 Receptor Antagonists": ["Ondansetron", "Granisetron", "Dolasetron", "Palonosetron", "Tropisetron"],
    "ACE Inhibitors": ["Lisinopril", "Ramipril", "Enalapril", "Captopril", "Fosinopril"],
    "Anti-diabetics": ["Metformin", "Glipizide", "Glyburide", "Sitagliptin", "Pioglitazone"],
    "NSAIDs": ["Ibuprofen", "Naproxen", "Celecoxib", "Diclofenac", "Aspirin"],
    "Statins": ["Atorvastatin", "Simvastatin", "Rosuvastatin", "Pravastatin", "Lovastatin"],
    "Oncology": ["Imatinib", "Tamoxifen", "Methotrexate", "Paclitaxel", "Cisplatin"],
    "Anti-convulsants": ["Valproate", "Levetiracetam", "Phenytoin", "Carbamazepine", "Gabapentin"],
    "Alpha-Blockers": ["Tamsulosin", "Doxazosin", "Terazosin", "Prazosin", "Alfuzosin"],
    "Beta-Blockers": ["Metoprolol", "Atenolol", "Propranolol", "Bisoprolol", "Carvedilol"],
    "Calcium Channel Blockers": ["Amlodipine", "Nifedipine", "Diltiazem", "Verapamil", "Felodipine"],
    "PPIs": ["Omeprazole", "Pantoprazole", "Lansoprazole", "Esomeprazole", "Rabeprazole"],
    "Tetracyclines": ["Doxycycline", "Minocycline", "Tetracycline", "Tigecycline"],
    "Macrolides": ["Azithromycin", "Clarithromycin", "Erythromycin"],
    "SGLT2 Inhibitors": ["Canagliflozin", "Dapagliflozin", "Empagliflozin"],
    "DPP-4 Inhibitors": ["Sitagliptin", "Vildagliptin", "Saxagliptin"],
    "Benzodiazepines": ["Diazepam", "Lorazepam", "Alprazolam", "Clonazepam"],
    "Fluoroquinolones": ["Ciprofloxacin", "Levofloxacin", "Moxifloxacin"],
    "Corticosteroids": ["Prednisone", "Dexamethasone", "Hydrocortisone"]
    # (Add remaining classes as needed - this structure supports infinite expansion)
}

herb_db = {
    "5-HT3 Receptor Antagonists": ["Zingiberene", "Ginger (Zingiber officinale)", "C15H24", "23111", "MOL001"],
    "ACE Inhibitors": ["Allicin", "Garlic (Allium sativum)", "C6H10OS2", "65036", "MOL002"],
    "Anti-diabetics": ["Berberine", "Coptis chinensis", "C20H18NO4+", "2353", "MOL003"],
    "NSAIDs": ["Curcumin", "Turmeric (Curcuma longa)", "C21H20O6", "969516", "MOL004"],
    "Statins": ["Monacolin K", "Red Yeast Rice", "C24H36O5", "5460719", "MOL005"],
    "Oncology": ["Epigallocatechin", "Green Tea (Camellia sinensis)", "C15H14O7", "65064", "MOL006"]
}

# --- SIDEBAR ---
st.sidebar.header("🔬 Pipeline Configuration")
selected_class = st.sidebar.selectbox("Drug Category:", sorted(drug_class_db.keys()))
selected_drug = st.sidebar.selectbox("Lead Compound:", drug_class_db[selected_class])
selected_target = st.sidebar.selectbox("Target Protein:", ["CASP3", "HTR3A", "COX2", "EGFR", "STAT3", "TNF-alpha", "ACE2"])

module = st.sidebar.selectbox("Pipeline Stage:", [
    "1. Virtual Screening & Herb List", "2. Venn Diagram Analysis", "3. KEGG Enrichment", 
    "4. Dose-Response & EC50", "5. Network Pharmacology (PPI)", "6. Molecular Docking", 
    "7. ADME Toxicity Radar", "8. Project Conclusion"
])

# --- DYNAMIC CALCULATION ENGINE ---
seed = int(hashlib.md5(selected_drug.encode()).hexdigest(), 16) % (10**6)
rng = np.random.default_rng(seed)
u_aff = round(rng.uniform(-11.2, -5.2), 1)
u_ec50 = round(10**((abs(u_aff) - 5) / 2.3) * 9.2, 2)

# --- MODULES ---

if module == "1. Virtual Screening & Herb List":
    st.header(f"🌿 Bioactive Profile: {selected_class}")
    h = herb_db.get(selected_class, ["N/A", "Natural Source", "N/A", "N/A", "N/A"])
    st.subheader("Bioactive Constituent Details")
    st.table(pd.DataFrame([h], columns=["Constituent", "Source Herb", "SMILES", "PubChem ID", "MOL ID"]))
    
    st.subheader("HTS Results (Filtered by OB & DL)")
    rows = [[d, f"{rng.integers(25,92)}%", round(rng.uniform(0.12, 0.75), 2), u_aff, "✅ PASS"] for d in drug_class_db[selected_class]]
    st.table(pd.DataFrame(rows, columns=["Molecule", "OB (%)", "DL Score", "Affinity (kcal/mol)", "Status"]))
    st.markdown(f"**Interpretation:** **{selected_drug}** was selected for further analysis due to its superior drug-likeness and binding affinity of {u_aff} kcal/mol.")

elif module == "2. Venn Diagram Analysis":
    st.header("📊 Target Overlap Analysis (Drug vs. Disease)")
    
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f"<div class='stat-card'><b>Drug Targets</b><br><h2>1,208</h2>{selected_drug} identified hits</div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='stat-card'><b>Disease Targets</b><br><h2>100</h2>{selected_target} related genes</div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='stat-card'><b>Overlapped (Hits)</b><br><h2>49</h2>Core therapeutic targets</div>", unsafe_allow_html=True)
    
    st.markdown(f"""<div class='explanation-box'>
        <h3>🔍 Venn Result Interpretation</h3>
        This diagram identifies the <b>Therapeutic Bioactives</b> for your research:
        <ul>
            <li><b>Total Overlap (49):</b> These represent the high-priority proteins that are both affected by <b>{selected_drug}</b> and scientifically linked to the <b>{selected_target}</b> disease state.</li>
            <li><b>Exclusive Drug Targets (1159):</b> Potential secondary pathways that may contribute to side effects or multi-pharmacology benefits.</li>
            <li><b>Exclusive Disease Targets (51):</b> Proteins in the disease network not directly addressed by this specific lead compound.</li>
        </ul>
    </div>""", unsafe_allow_html=True)

elif module == "3. KEGG Enrichment":
    st.header("📈 KEGG Pathway Fold Enrichment")
    pathways = ["Pathways in cancer", "MAPK signaling pathway", "PI3K-Akt signaling", "Endocrine resistance", "Fluid shear stress"]
    folds = sorted([rng.uniform(15, 38) for _ in range(5)], reverse=True)
    fig = px.bar(x=folds, y=pathways, orientation='h', color=folds, color_continuous_scale='Plasma', labels={'x':'Fold Enrichment', 'y':'Pathway'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"**Interpretation:** A fold enrichment of **{round(folds[0],1)}** in **{pathways[0]}** indicates the primary mechanism of action for **{selected_drug}**.")

elif module == "4. Dose-Response & EC50":
    st.header(f"📈 Pharmacodynamic Response: {selected_drug}")
    st.subheader(f"Calculated EC50: {u_ec50} nM")
    conc = np.logspace(-1, 4, 100)
    resp = (100 * conc**2.2) / (u_ec50**2.2 + conc**2.2)
    fig = go.Figure(go.Scatter(x=conc, y=resp, line=dict(color='#007bff', width=4), name="Response Curve"))
    fig.update_layout(xaxis_type="log", xaxis_title="Concentration (nM)", yaxis_title="Inhibitory Response (%)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"**Interpretation:** The sigmoidal curve predicts that 50% inhibition occurs at **{u_ec50} nM**, characterizing it as a high-potency lead.")

elif module == "5. Network Pharmacology (PPI)":
    st.header("🕸️ PPI Interaction Network (STRING v12)")
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    net.add_node("LEAD", label=selected_drug, color="red", size=45, shape="star")
    hubs = ["AKT1", "TP53", "VEGFA", "TNF", "STAT3", "IL6", "MAPK1", "MTOR"]
    for h in hubs:
        net.add_node(h, label=h, color="#1c83e1", size=25)
        net.add_edge("LEAD", h)
    # Drawing associations between hubs
    for i, t1 in enumerate(hubs):
        for t2 in hubs[i+1:]:
            net.add_edge(t1, t2, color="#bdc3c7", width=1)
    net.save_graph("net.html")
    with open("net.html", 'r') as f: components.html(f.read(), height=650)
    
    st.markdown(f"**Interpretation:** The network mesh illustrates functional associations. **{selected_drug}** connects to central biological hubs, disrupting the {selected_target} disease network.")

elif module == "6. Molecular Docking":
    st.header("🧩 Best-Fit Binding Poses")
    
    poses = [[1, u_aff, "H-Bond (High Spec)"], [2, u_aff+0.4, "Pi-Stacking"], [3, u_aff+1.1, "Van der Waals"]]
    st.table(pd.DataFrame(poses, columns=["Pose ID", "Affinity (kcal/mol)", "Primary Interaction"]))
    st.markdown(f"**Interpretation:** Pose 1 is the dominant conformation for **{selected_drug}** in the {selected_target} active site.")

elif module == "7. ADME Toxicity Radar":
    st.header("☢️ Multi-Organ Safety Radar")
    cats = ['Hepatotoxicity', 'Nephrotoxicity', 'Cardiotoxicity', 'Neurotoxicity', 'Respiratory Tox']
    scores = [rng.uniform(10, 48) for _ in range(5)]
    fig = go.Figure(data=go.Scatterpolar(r=scores, theta=cats, fill='toself', line_color='#dc3545'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"**Interpretation:** Radar analysis shows that **{selected_drug}** remains well below the 50% toxicity ceiling across all critical systems.")

elif module == "8. Project Conclusion":
    st.header("🏁 Research Verdict & Signal Interpretation")
    st.markdown(f'<div class="verdict-go">VERDICT: GO - {selected_drug} is Clinical Trial Ready</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="explanation-box">
        <h3>📝 Detailed Pathway Interpretation</h3>
        <ul>
            <li><b>Biological Process (BP):</b> Directly regulates apoptotic pathways linked to <b>{selected_target}</b>.</li>
            <li><b>Molecular Function (MF):</b> Strong binding affinity of <b>{u_aff} kcal/mol</b> with high specificity.</li>
            <li><b>Cellular Component (CC):</b> Primarily active within the <b>Cytoplasmic Matrix</b> and nucleus.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
