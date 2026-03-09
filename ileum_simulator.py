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

# --- EXPANDED DATABASE (~80+ Drugs) ---
drug_db = {
    "Cardiovascular": ["Atorvastatin", "Amlodipine", "Lisinopril", "Metoprolol", "Warfarin", "Digoxin", "Clopidogrel", "Losartan", "Simvastatin", "Valsartan", "Ezetimibe", "Spironolactone", "Furosemide", "Ramipril", "Hydralazine", "Carvedilol", "Nifedipine"],
    "Analgesics/NSAIDs": ["Aspirin", "Ibuprofen", "Naproxen", "Celecoxib", "Diclofenac", "Ketorolac", "Indomethacin", "Morphine", "Oxycodone", "Tramadol", "Acetaminophen", "Etodolac", "Meloxicam", "Fentanyl", "Piroxicam"],
    "Antidiabetics": ["Metformin", "Glipizide", "Glyburide", "Sitagliptin", "Pioglitazone", "Empagliflozin", "Liraglutide", "Insulin Glargine", "Acarbose", "Repaglinide", "Canagliflozin", "Linagliptin"],
    "Neurological": ["Sertraline", "Escitalopram", "Fluoxetine", "Donepezil", "Levodopa", "Gabapentin", "Pregabalin", "Diazepam", "Alprazolam", "Zolpidem", "Quetiapine", "Risperidone", "Lithium", "Venlafaxine", "Amitriptyline", "Haloperidol"],
    "Antibiotics/Antivirals": ["Amoxicillin", "Azithromycin", "Ciprofloxacin", "Doxycycline", "Cephalexin", "Acyclovir", "Oseltamivir", "Ritonavir", "Remdesivir", "Metronidazole", "Clarithromycin", "Levofloxacin", "Vancomycin"],
    "Respiratory/Allergy": ["Albuterol", "Fluticasone", "Montelukast", "Loratadine", "Cetirizine", "Diphenhydramine", "Fexofenadine", "Prednisone", "Budesonide", "Tiotropium", "Salmeterol"],
    "Gastrointestinal": ["Omeprazole", "Ranitidine", "Famotidine", "Esomeprazole", "Pantoprazole", "Lansoprazole", "Ondansetron", "Metoclopramide", "Loperamide", "Sucralfate"],
    "Oncology/Immunology": ["Methotrexate", "Tamoxifen", "Imatinib", "Pembrolizumab", "Cyclosporine", "Adalimumab", "Infliximab", "Rituximab", "Trastuzumab", "Anastrozole", "Everolimus", "Paclitaxel"]
}

protein_categories = {
    "CASP3": "Enzyme (Apoptosis)", "H1-Receptor": "Receptor", 
    "HMG-CoA": "Enzyme", "COX2": "Enzyme", "EGFR": "Receptor", 
    "HER2": "Receptor", "ACE": "Enzyme", "PDE5": "Enzyme", "TNF-alpha": "Cytokine"
}

all_drugs = sorted([d for sub in drug_db.values() for d in sub])
all_proteins = list(protein_categories.keys())

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🔬 Research Parameters")
selected_drug = st.sidebar.selectbox("Lead Compound:", all_drugs)
selected_target = st.sidebar.selectbox("Target Protein:", all_proteins)

# --- DYNAMIC CALCULATION SEED ---
# This ensures that changing the drug resets all the math below
random.seed(selected_drug + selected_target)

binding_energy = round(random.uniform(-11.5, -4.5), 1)
overlap_val = random.randint(35, 75)
exclusive_drug = random.randint(40, 90)
exclusive_disease = random.randint(15, 40)
dynamic_tox = round(abs(binding_energy) * random.uniform(7.0, 9.5), 1)

st.sidebar.info(f"Natural Affinity: {binding_energy} kcal/mol")

module = st.sidebar.selectbox("Pipeline Stage:", 
    ["Virtual Screening", "Venn Diagram Analysis", "Dose-Response Analysis", "Pathway & Signal Analysis", "Network Pharmacology Explorer", "Molecular Docking", "Project Conclusion"])

# -------------------------------------------------
# 1. VIRTUAL SCREENING
# -------------------------------------------------
if module == "Virtual Screening":
    st.header("🧪 High-Throughput Screening (HTS)")
    if st.button("🚀 Execute Library Screen"):
        results = []
        screen_list = random.sample(all_drugs, 15)
        for d in screen_list:
            energy = round(random.uniform(-11, -4), 2)
            tox = round(abs(energy) * random.uniform(5, 10), 1)
            status = "✅ SAFE" if tox < 65 else "⚠️ UNSAFE"
            results.append([d, selected_target, energy, tox, status])
        st.session_state.screen_df = pd.DataFrame(results, columns=["Drug", "Target", "Energy", "Toxicity %", "Status"])
    
    if 'screen_df' in st.session_state:
        st.table(st.session_state.screen_df)

# -------------------------------------------------
# 2. VENN DIAGRAM ANALYSIS
# -------------------------------------------------
# -------------------------------------------------
# 2. VENN DIAGRAM ANALYSIS (WITH DYNAMIC TABLE)
# -------------------------------------------------

       # -------------------------------------------------
# 2. VENN DIAGRAM ANALYSIS (WITH TARGET NAMES)
# -------------------------------------------------
elif module == "Venn Diagram Analysis":
    st.header(f"📊 Target Overlap Analysis: {selected_drug}")
    
    if VENN_AVAILABLE:
        fig, ax = plt.subplots(figsize=(8, 5))
        venn2(subsets=(exclusive_drug, exclusive_disease, overlap_val), 
              set_labels=(f'Predicted Targets\nof {selected_drug}', 'Disease-Associated\nProteins'))
        st.pyplot(fig)
        
    else:
        st.error("Error: 'matplotlib-venn' library not found.")

    st.markdown("### 📋 Protein Identification Table")
    
    # Generate mock protein names based on the drug's seed for consistency
    overlap_list = random.sample(["AKT1", "TNF", "MAPK1", "IL6", "VEGFA", "PTGS2", "TP53", "STAT3", "MTOR", "EGFR"], min(5, overlap_val))
    predicted_list = random.sample(["CYP3A4", "ALB", "ABCB1", "SLC22A1", "SULT1A1", "UGT1A1", "HMGCR", "ESR1"], 5)
    disease_list = random.sample(["BRCA1", "APOE", "LDLR", "INS", "CRP", "IL1B", "CASP3", "NOD2"], 5)

    # Create the table using your exact headings
    target_data = {
        "Category": ["🎯 Predicted Targets", "🏥 Disease-Associated Proteins", "🧬 Overlapped Area"],
        "Count": [exclusive_drug + overlap_val, exclusive_disease + overlap_val, overlap_val],
        "Protein Names (Sample)": [", ".join(predicted_list), ", ".join(disease_list), ", ".join(overlap_list)]
    }
    
    st.table(pd.DataFrame(target_data))

    st.markdown(f"""
    <div class="explanation-box">
        <h3>🔍 Venn Result Interpretation</h3>
        This diagram identifies the <b>Therapeutic Bioactives</b> for your research:
        <ul>
            <li><b>Total Overlap ({overlap_val}):</b> These are the high-priority targets. They represent proteins that are both predicted to bind with {selected_drug} and are scientifically proven to be involved in the disease.</li>
            <li><b>Predicted Targets:</b> The total number of proteins {selected_drug} is expected to interact with.</li>
            <li><b>Disease-Associated Proteins:</b> The proteins known to be part of the disease pathology.</li>
            <li><b>Relevance:</b> Finding {overlap_val} common targets is a statistically significant result, suggesting this drug has strong multi-target potential.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
   

# -------------------------------------------------
# 3. DOSE-RESPONSE ANALYSIS
# -------------------------------------------------
elif module == "Dose-Response Analysis":
    st.header(f"📈 Pharmacodynamic Profile: {selected_drug}")
    
    ec50 = np.interp(binding_energy, [-12, -4], [0.5, 150])
    hill_coeff = 2.4 if "Receptor" in protein_categories[selected_target] else 1.2
    
    conc = np.logspace(-1, 4, 100)
    response = (100.0 * (conc**hill_coeff)) / ((ec50**hill_coeff) + (conc**hill_coeff))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=conc, y=response, name="Response Curve", line=dict(color='#007bff', width=4)))
    fig.add_hline(y=dynamic_tox, line_dash="dash", line_color="red", annotation_text="Toxicity Threshold")
    fig.update_layout(xaxis_type="log", title=f"Log-Dose Response: {selected_drug}", xaxis_title="Concentration (nM)", yaxis_title="Response (%)")
    st.plotly_chart(fig, use_container_width=True)
    

    st.subheader("📊 Dose-Response Calculation Table")
    metrics = {
        "Parameter": ["Calculated EC50", "Hill Slope (n)", "Max Efficacy (Emax)", "Toxicity Limit"],
        "Value": [f"{round(ec50, 2)} nM", hill_coeff, "100%", f"{dynamic_tox}%"],
        "Interpretation": [
            "Potency: Concentration needed for 50% effect. Smaller is better.",
            "Cooperativity: Steepness of the curve. Higher values mean a sharp 'on/off' effect.",
            "Capacity: The highest level of biological effect the drug can achieve.",
            "Safety Ceiling: The response level where adverse events are predicted."
        ]
    }
    st.table(pd.DataFrame(metrics))

# -------------------------------------------------
# 4. PATHWAY & BAR CHART
# -------------------------------------------------
elif module == "Pathway & Signal Analysis":
    st.header("⚡ Cellular Signaling & Signal Decay")
    
    # Recalculate inhibition based on the dynamic energy of the chosen drug
    inhibition = np.interp(binding_energy, [-12, -4], [98, 15])
    steps = [selected_target, "Relay Protein", "Kinase Cascade", "Transcription", "Cell Fate"]
    decay = [round(inhibition * (0.8**i), 1) for i in range(len(steps))]
    
    st.subheader("Signal Attenuation (Bar Chart)")
    st.plotly_chart(go.Figure(go.Bar(x=steps, y=decay, marker_color='#6610f2', text=decay, textposition='auto')), use_container_width=True)
    
    st.markdown(f"""
    <div class="explanation-box">
        <h3>📉 Bar Chart Result Interpretation</h3>
        This chart displays <b>Pharmacological Momentum</b> across five biological stages:
        <ul>
            <li><b>Initial Binding:</b> At the start, <b>{selected_drug}</b> blocks <b>{decay[0]}%</b> of the <b>{selected_target}</b>.</li>
            <li><b>Intermediate Decay:</b> By the <b>{steps[2]}</b> stage, only <b>{decay[2]}%</b> of that inhibitory signal remains.</li>
            <li><b>Net Physiological Impact:</b> The final <b>{decay[4]}%</b> shows the actual change in the patient's cell fate.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Biological Flowchart (Pathway)")
    net = Network(height="400px", width="100%", bgcolor="#ffffff", directed=True)
    for i, step in enumerate(steps):
        net.add_node(step, label=f"{step}\n{decay[i]}%", color="#ff4b4b" if decay[i] > 50 else "#1c83e1")
        if i > 0: net.add_edge(steps[i-1], steps[i])
    net.save_graph("path.html")
    with open("path.html", 'r') as f: components.html(f.read(), height=450)
    

# -------------------------------------------------
# 5. NETWORK PHARMACOLOGY EXPLORER
# -------------------------------------------------
elif module == "Network Pharmacology Explorer":
    st.header(f"🕸️ STRING Mesh: Functional Protein Associations")
    net = Network(height="550px", width="100%", bgcolor="#ffffff", font_color="black")
    net.add_node(selected_drug, label=selected_drug, color="#ff4b4b", size=40)
    
    mesh_targets = random.sample(["AKT1", "STAT3", "TNF", "MAPK", "IL-6", "PTGS2", "VEGFA", "NFKB1", "MTOR", "TP53"], 8)
    for p in mesh_targets:
        is_intersection = random.choice([True, False])
        net.add_node(p, label=p, color="#ff4b4b" if is_intersection else "#1c83e1", size=30 if is_intersection else 20)
        net.add_edge(selected_drug, p, width=2)
    
    for i in range(len(mesh_targets)):
        t_a, t_b = mesh_targets[i], mesh_targets[(i + 1) % len(mesh_targets)]
        net.add_edge(t_a, t_b, color="#dddddd", width=1)

    net.toggle_physics(True)
    net.save_graph("mesh.html")
    with open("mesh.html", 'r') as f: components.html(f.read(), height=600)
    

    st.markdown("""
    <div class="explanation-box">
        <h3>🕸️ STRING Network Result Interpretation</h3>
        This "Mesh of Strings" mimics your <b>STRING Database</b> results:
        <ul>
            <li><b>Node Colors:</b> Red nodes represent <b>Intersection Targets</b> (Bioactive Hubs). Blue are associated secondary targets.</li>
            <li><b>String Connectivity:</b> Density of strings shows <b>Functional Association</b>. High connectivity indicates disruption of an entire disease pathway.</li>
            <li><b>Biological Hubs:</b> Proteins with the most strings are "Hubs," making them powerful treatment sites.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 6. MOLECULAR DOCKING
# -------------------------------------------------
elif module == "Molecular Docking":
    st.header("🧩 In-Silico Molecular Docking")
    inter_types = ["H-Bond", "Van der Waals", "Pi-Stacking", "Ionic Interaction"]
    poses = [[i, round(binding_energy + random.uniform(-0.4, 0.4), 2), random.choice(inter_types)] for i in range(1, 6)]
    st.table(pd.DataFrame(poses, columns=["Pose ID", "Affinity (kcal/mol)", "Interaction Type"]))
    

    st.markdown(f"""
    <div class="explanation-box">
        <h3>🧩 Docking Result Interpretation</h3>
        <ul>
            <li><b>Pose 1:</b> Most stable conformation at <b>{poses[0][1]} kcal/mol</b>.</li>
            <li><b>Interaction:</b> {poses[0][2]} is the dominant force. H-bonding indicates high specificity.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# 7. PROJECT CONCLUSION
# -------------------------------------------------
elif module == "Project Conclusion":
    st.header("🏁 Clinical Trial Readiness Verdict")
    inhibition = np.interp(binding_energy, [-12, -4], [98, 15])
    final_signal = inhibition * (0.8**4)
    
    is_potent, is_safe, is_effective = abs(binding_energy) > 7.5, dynamic_tox < 75.0, final_signal > 30.0
    verdict = "GO" if (is_potent and is_safe and is_effective) else "NO-GO"
    
    st.markdown(f"""
    <div class="conclusion-card {'go-signal' if verdict == 'GO' else 'nogo-signal'}">
        <h2 style="text-align: center;">VERDICT: {verdict}</h2>
        <p style="text-align: center;">Drug Analysis Summary for <b>{selected_drug}</b></p>
    </div>
    <div class="explanation-box">
        <h3>📝 Detailed Clinical Rationale</h3>
        <ul>
            <li><b>Binding Profile:</b> {binding_energy} kcal/mol ({'Potent' if is_potent else 'Weak'}).</li>
            <li><b>Safety Rating:</b> Toxicity threshold {dynamic_tox}% ({'Safe' if is_safe else 'Unsafe'}).</li>
            <li><b>Efficacy:</b> Final signal {round(final_signal,1)}% ({'Effective' if is_effective else 'Low Impact'}).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
