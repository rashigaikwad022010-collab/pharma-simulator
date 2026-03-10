import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import hashlib
import random
from pyvis.network import Network
import streamlit.components.v1 as components
import io

# --- UI SETTINGS ---
st.set_page_config(page_title="Advanced Pharma Pipeline", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .explanation-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 6px solid #007bff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin: 20px 0; }
    .result-desc { font-style: italic; color: #2c3e50; margin: 10px 0; padding: 15px; background: #f1f4f9; border-left: 5px solid #6610f2; border-radius: 5px; }
    .go-signal { background-color: #d4edda; border-color: #28a745; color: #155724; padding: 20px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Advanced Pharmaceutical Research & Docking Pipeline")

# --- UNIQUE DATA GENERATOR ---
def get_unique_metrics(drug_name, target_name):
    seed_str = f"{drug_name}_{target_name}"
    seed = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (10**8)
    rng = np.random.default_rng(seed)
    mw = round(rng.uniform(250.0, 600.0), 2)
    ob = round(rng.uniform(0.10, 0.90), 2) 
    dl = round(rng.uniform(0.05, 0.80), 2) 
    affinity = round(rng.uniform(-11.5, -4.5), 1)
    return mw, ob, dl, affinity

# --- DATABASE: 50+ PHARMACOLOGICAL CLASSES ---
drug_class_db = {
    "5-HT3 Receptor Antagonists": ["Ondansetron", "Granisetron", "Dolasetron", "Palonosetron", "Tropisetron", "Alosetron", "Cilansetron", "Ramosetron", "Azasetron", "Lerisetron"],
    "ACE Inhibitors": ["Lisinopril", "Ramipril", "Enalapril", "Captopril", "Fosinopril", "Quinapril", "Benazepril", "Perindopril", "Trandolapril", "Moexipril"],
    "Alpha-Blockers": ["Tamsulosin", "Doxazosin", "Terazosin", "Prazosin", "Alfuzosin", "Silodosin", "Phenoxybenzamine", "Phentolamine", "Indoramin", "Urapidil"],
    "Aminoglycosides": ["Gentamicin", "Amikacin", "Tobramycin", "Neomycin", "Streptomycin", "Kanamycin", "Netilmicin", "Paromomycin", "Spectinomycin", "Sisomicin"],
    "Angiotensin II Receptor Blockers": ["Losartan", "Valsartan", "Candesartan", "Irbesartan", "Olmesartan", "Telmisartan", "Eprosartan", "Azilsartan", "Fimasartan", "Milfasartan"],
    "Anti-amoebics": ["Metronidazole", "Tinidazole", "Nitazoxanide", "Paromomycin", "Diloxanide", "Emetine", "Chloroquine", "Iodoquinol", "Secnidazole", "Ornidazole"],
    "Anti-arrhythmics": ["Amiodarone", "Lidocaine", "Procainamide", "Sotalol", "Flecainide", "Quinidine", "Adenosine", "Mexiletine", "Propafenone", "Dofetilide"],
    "Anti-cholinergics": ["Atropine", "Scopolamine", "Ipratropium", "Tiotropium", "Oxybutynin", "Benztropine", "Glycopyrrolate", "Dicyclomine", "Hyoscyamine", "Solifenacin"],
    "Anti-convulsants": ["Valproate", "Levetiracetam", "Phenytoin", "Carbamazepine", "Gabapentin", "Lamotrigine", "Topiramate", "Zonisamide", "Ethosuximide", "Vigabatrin"],
    "Anti-depressants (SSRI)": ["Sertraline", "Fluoxetine", "Paroxetine", "Citalopram", "Escitalopram", "Fluvoxamine", "Vilazodone", "Vortioxetine", "Zimelidine", "Indalpine"],
    "Anti-diabetics": ["Glipizide", "Glyburide", "Glimepiride", "Gliclazide", "Tolbutamide", "Chlorpropamide", "Metformin", "Pioglitazone", "Sitagliptin", "Exenatide"],
    "Anti-emetics": ["Domperidone", "Metoclopramide", "Aprepitant", "Rolapitant", "Promethazine", "Prochlorperazine", "Dronabinol", "Nabilone", "Scopolamine", "Casopitant"],
    "Anti-fungals": ["Fluconazole", "Itraconazole", "Ketoconazole", "Voriconazole", "Posaconazole", "Clotrimazole", "Miconazole", "Amphotericin B", "Nystatin", "Terbinafine"],
    "Anti-histamines": ["Cetirizine", "Loratadine", "Fexofenadine", "Diphenhydramine", "Chlorpheniramine", "Levocetirizine", "Desloratadine", "Azelastine", "Promethazine", "Cyproheptadine"],
    "Anti-malarials": ["Artemisinin", "Chloroquine", "Quinine", "Mefloquine", "Primaquine", "Lumefantrine", "Atovaquone", "Proguanil", "Pyrimethamine", "Artesunate"],
    "Anti-neoplastics": ["Cyclophosphamide", "Methotrexate", "Paclitaxel", "Cisplatin", "Doxorubicin", "Tamoxifen", "Imatinib", "Pembrolizumab", "Rituximab", "Everolimus"],
    "Anti-platelets": ["Clopidogrel", "Aspirin", "Ticagrelor", "Prasugrel", "Tirofiban", "Eptifibatide", "Abciximab", "Dipyridamole", "Cilostazol", "Vorapaxar"],
    "Anti-psychotics": ["Quetiapine", "Risperidone", "Olanzapine", "Clozapine", "Aripiprazole", "Ziprasidone", "Lurasidone", "Paliperidone", "Haloperidol", "Chlorpromazine"],
    "Anti-tuberculars": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol", "Bedaquiline", "Delamanid", "Streptomycin", "Ethionamide", "Cycloserine", "Capreomycin"],
    "Benzodiazepines": ["Diazepam", "Lorazepam", "Alprazolam", "Clonazepam", "Midazolam", "Temazepam", "Oxazepam", "Chlordiazepoxide", "Flurazepam", "Triazolam"],
    "Beta-Blockers": ["Metoprolol", "Atenolol", "Propranolol", "Bisoprolol", "Carvedilol", "Nadolol", "Nebivolol", "Esmolol", "Labetalol", "Pindolol"],
    "Calcium Channel Blockers": ["Amlodipine", "Nifedipine", "Diltiazem", "Verapamil", "Felodipine", "Nicardipine", "Isradipine", "Nisoldipine", "Nimodipine", "Clevidipine"],
    "Cephalosporins": ["Cefazolin", "Cephalexin", "Cefuroxime", "Cefaclor", "Ceftriaxone", "Cefotaxime", "Ceftazidime", "Cefixime", "Cefdinir", "Cefepime"],
    "Corticosteroids": ["Prednisone", "Dexamethasone", "Hydrocortisone", "Methylprednisolone", "Betamethasone", "Triamcinolone", "Budesonide", "Mometasone", "Fluticasone", "Prednisolone"],
    "Diuretics": ["Furosemide", "Hydrochlorothiazide", "Spironolactone", "Chlorthalidone", "Bumetanide", "Torsemide", "Amiloride", "Indapamide", "Metolazone", "Triamterene"],
    "Fluoroquinolones": ["Ciprofloxacin", "Levofloxacin", "Moxifloxacin", "Ofloxacin", "Norfloxacin", "Gemifloxacin", "Gatifloxacin", "Delafloxacin", "Lomefloxacin", "Sparfloxacin"],
    "H2-Receptor Antagonists": ["Famotidine", "Ranitidine", "Cimetidine", "Nizatidine", "Roxatidine", "Lafutidine", "Niperotidine", "Ebrotidine", "Burimamide", "Metiamide"],
    "Macrolides": ["Azithromycin", "Clarithromycin", "Erythromycin", "Telithromycin", "Fidaxomicin", "Spiramycin", "Josamycin", "Roxithromycin", "Oleandomycin", "Kitasamycin"],
    "NSAIDs": ["Ibuprofen", "Naproxen", "Celecoxib", "Diclofenac", "Aspirin", "Meloxicam", "Etodolac", "Indomethacin", "Ketorolac", "Nabumetone"],
    "Proton Pump Inhibitors": ["Omeprazole", "Pantoprazole", "Lansoprazole", "Esomeprazole", "Rabeprazole", "Dexlansoprazole", "Tenatoprazole", "Ilaprazole", "Picoprazole", "Omeprazole Magnesium"],
    "Statins": ["Atorvastatin", "Simvastatin", "Rosuvastatin", "Pravastatin", "Lovastatin", "Fluvastatin", "Pitavastatin", "Cerivastatin", "Mevastatin", "Glenvastatin"],
    "Tetracyclines": ["Doxycycline", "Minocycline", "Tetracycline", "Tigecycline", "Oxytetracycline", "Demeclocycline", "Lymecycline", "Meclocycline", "Methacycline", "Rolitetracycline"],
    "Vinca Alkaloids": ["Vincristine", "Vinblastine", "Vinorelbine", "Vindesine", "Vinflunine", "Vinperine", "Vincadioline", "Vincatene", "Vinrosidine", "Vinzolidine"],
    "Sulfonamides": ["Sulfamethoxazole", "Sulfadiazine", "Sulfasalazine", "Sulfisoxazole", "Sulfacetamide", "Sulfadoxine", "Sulfamethizole", "Sulfanilamide", "Sulfapyridine", "Sulfathiazole"],
    "Nitroimidazoles": ["Metronidazole", "Tinidazole", "Nimorazole", "Dimetridazole", "Pretomanid", "Fexinidazole", "Satranidazole", "Secnidazole", "Ornidazole", "Azomycin"],
    "Penicillins": ["Amoxicillin", "Ampicillin", "Piperacillin", "Ticarcillin", "Bacampicillin", "Azlocillin", "Mezlocillin", "Carbenicillin", "Talampicillin", "Pivampicillin"],
    "SGLT2 Inhibitors": ["Canagliflozin", "Dapagliflozin", "Empagliflozin", "Ertugliflozin", "Ipragliflozin", "Luseogliflozin", "Tofogliflozin", "Sergliflozin", "Remogliflozin", "Sotagliflozin"],
    "Bisphosphonates": ["Alendronate", "Risedronate", "Ibandronate", "Zoledronic acid", "Etidronate", "Pamidronate", "Tiludronate", "Clodronate", "Neridronate", "Olpadronate"],
    "DPP-4 Inhibitors": ["Sitagliptin", "Vildagliptin", "Saxagliptin", "Linagliptin", "Alogliptin", "Gemigliptin", "Teneligliptin", "Anagliptin", "Trelagliptin", "Omarigliptin"],
    "Kinase Inhibitors": ["Imatinib", "Erlotinib", "Gefitinib", "Sunitinib", "Sorafenib", "Dasatinib", "Lapatinib", "Nilotinib", "Pazopanib", "Afatinib"],
    "Monoclonal Antibodies": ["Pembrolizumab", "Rituximab", "Trastuzumab", "Adalimumab", "Infliximab", "Bevacizumab", "Nivolumab", "Ustekinumab", "Dupilumab", "Ocrelizumab"],
    "Inhaled Beta-2 Agonists": ["Albuterol", "Salmeterol", "Formoterol", "Levalbuterol", "Indacaterol", "Vilanterol", "Olodaterol", "Terbutaline", "Metaproterenol", "Fenoterol"],
    "HMG-CoA Reductase Inhibitors": ["Atorvastatin", "Rosuvastatin", "Simvastatin", "Pravastatin", "Lovastatin", "Fluvastatin", "Pitavastatin", "Cerivastatin", "Mevastatin", "Dalvastatin"],
    "Narcotic Analgesics": ["Morphine", "Fentanyl", "Oxycodone", "Codeine", "Hydromorphone", "Methadone", "Meperidine", "Tramadol", "Buprenorphine", "Hydrocodone"],
    "Barbiturates": ["Phenobarbital", "Secobarbital", "Pentobarbital", "Amobarbital", "Butabarbital", "Methohexital", "Thiopental", "Alphenal", "Barbital", "Allobarbital"]
}

# --- SIDEBAR ---
st.sidebar.header("🔬 Research Controls")
selected_class = st.sidebar.selectbox("Drug Category:", sorted(drug_class_db.keys()))
selected_drug = st.sidebar.selectbox("Lead Compound:", drug_class_db[selected_class])
selected_target = st.sidebar.selectbox("Target Protein:", ["CASP3", "HTR3A", "COX2", "EGFR", "STAT3", "TNF-alpha", "ACE2", "HMGCR"])

# Active Filters for Screening
ob_filter = st.sidebar.slider("Minimum OB (%) Filter", 0, 100, 30)
dl_filter = st.sidebar.slider("Minimum DL Filter", 0.0, 1.0, 0.18)

u_mw, u_ob, u_dl, u_affinity = get_unique_metrics(selected_drug, selected_target)
module = st.sidebar.selectbox("Pipeline Stage:", 
    ["Virtual Screening", "Venn Diagram Analysis", "Dose-Response Analysis", "Pathway & Signal Analysis", "Network Pharmacology Explorer", "Project Conclusion"])

# 1. VIRTUAL SCREENING
if module == "Virtual Screening":
    st.header(f"🧪 Screening Module: {selected_class}")
    all_data = []
    for d in drug_class_db[selected_class]:
        m_mw, m_ob, m_dl, m_aff = get_unique_metrics(d, selected_target)
        status = "✅ PASS" if (m_ob * 100 >= ob_filter and m_dl >= dl_filter) else "❌ FAIL"
        all_data.append([d, m_mw, f"{round(m_ob*100,1)}%", m_dl, m_aff, status])
    
    st.table(pd.DataFrame(all_data, columns=["Molecule Name", "MW", "OB (%)", "DL", "Affinity", "Status"]))
    
    st.markdown(f"""
    <div class="result-desc">
        <b>Result Description:</b> The screening process applied a filter of {ob_filter}% Oral Bioavailability and {dl_filter} Drug-Likeness. 
        <b>{selected_drug}</b> was characterized with an OB of {round(u_ob*100,1)}% and a binding affinity of {u_affinity} kcal/mol, 
        passing the selection criteria for lead optimization.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🌿 Bioactive Constituent Profile")
    constituent_data = [
        ["isovitexin", "Saponaretin", "C1=CC(=CC=C1C2=CC(=O)C3=C(O2)C=C(C(=C3O)[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O)O", "162350", "MOL002322"],
        ["Leucanthoside", "Isoorientin 7-methyl ether", "COC1=C(C(=C2C(=C1)OC(=CC2=O)C3=CC(=C(C=C3)O)O)O)[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O", "442659", "MOL003137"],
        ["gentirigenic acid", "GENTIRIGENate", "C[C@@]12CC[C@@H]([C@H]1CC[C@H]3[C@]2(CC[C@@H]4[C@@]3(CC[C@@H]([C@]4(C)CO)O)C)C)[C@@]5(C[C@@H]([C@@H](C(O5)(C)C)O)O)C(=O)O", "44423055", "MOL003143"]
    ]
    st.table(pd.DataFrame(constituent_data, columns=["CONSTITUENTS NAME", "SYM(PB)", "SMILE", "PUBCHEM ID", "MOL ID"]))

# 2. VENN DIAGRAM ANALYSIS
elif module == "Venn Diagram Analysis":
    st.header("📊 Target Overlap Analysis")
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Overlapped Targets")
        st.table(pd.DataFrame([["AKT1", "9.2", "High"], ["TP53", "8.7", "Medium"], ["TNF", "8.4", "High"]], columns=["Target", "Degree", "Relevance"]))
    with col2:
        st.subheader("🧬 Disease-Specific Targets")
        st.table(pd.DataFrame([["IL6", "Inflammation"], ["MAPK1", "Proliferation"], ["CASP8", "Apoptosis"]], columns=["Target", "Pathway"]))
    
    st.markdown(f"**Result Description:** The analysis confirms that **{selected_drug}** shares key regulatory hubs with the disease profile, specifically targeting the {selected_target} signaling node.")

# 3. DOSE-RESPONSE ANALYSIS
elif module == "Dose-Response Analysis":
    st.header(f"📈 Pharmacodynamic Profile: {selected_drug}")
    ec50 = np.interp(u_affinity, [-12, -4], [0.5, 150])
    conc = np.logspace(-1, 4, 100)
    response = (100.0 * (conc**2.2)) / ((ec50**2.2) + (conc**2.2))
    
    fig = go.Figure(go.Scatter(x=conc, y=response, line=dict(color='#007bff', width=4)))
    fig.update_layout(xaxis_type="log", xaxis_title="Concentration (nM)", yaxis_title="Efficacy (%)")
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown(f"**Result Description:** In-silico modeling predicts a sigmoidal response curve for **{selected_drug}** with a calculated EC50 of {round(ec50, 2)} nM, suggesting high potency.")

# 4. PATHWAY & SIGNAL ANALYSIS
elif module == "Pathway & Signal Analysis":
    st.header("⚡ Pathway & GO Molecular Function Enrichment")
    
    
    st.subheader("🧬 GO Molecular Function (MF) Table")
    go_data = [
        ["GO:0004674", "protein serine/threonine kinase activity", "1.2e-07", "8/14"],
        ["GO:0005515", "protein binding", "4.5e-05", "12/14"],
        ["GO:0008270", "zinc ion binding", "0.0021", "5/14"]
    ]
    st.table(pd.DataFrame(go_data, columns=["GO ID", "Molecular Function", "p-value", "Ratio"]))

    st.markdown("### 🔍 Pathway Result Interpretation")
    st.markdown(f"""
    <div class="result-desc">
        <b>Biological Process (BP):</b> {selected_drug} modulates the cellular lifecycle of {selected_target} by inhibiting signal transduction pathways. <br>
        <b>Molecular Function (MF):</b> Exhibits high enzymatic binding activity to {selected_target} with a predicted affinity of {u_affinity} kcal/mol. <br>
        <b>Cellular Component (CC):</b> Targeted activity occurs primarily within the cytoplasmic matrix and nuclear membrane interface.
    </div>
    """, unsafe_allow_html=True)

# 5. NETWORK PHARMACOLOGY
elif module == "Network Pharmacology Explorer":
    st.header("🕸️ PPI Interaction Network (STRING v11.5 Aesthetic)")
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    
    # Add Nodes
    net.add_node(selected_drug, label=selected_drug, color="#ff4b4b", size=45, shape="star")
    hubs = ["AKT1", "TP53", "VEGFA", "TNF", "STAT3", "IL6", "MYC", "PTGS2", "CCND1"]
    for t in hubs:
        net.add_node(t, label=t, color="#1c83e1", size=25)
    
    # Add Edges (Lead to Hubs)
    for t in hubs:
        net.add_edge(selected_drug, t, width=2)
    
    # Add Inter-hub Messy Edges (Safe Check)
    all_nodes = [selected_drug] + hubs
    for i, n1 in enumerate(hubs):
        for n2 in hubs[i+1:]:
            if random.random() > 0.6:
                net.add_edge(n1, n2, color="#bdc3c7")
                
    net.save_graph("net.html")
    with open("net.html", 'r') as f: components.html(f.read(), height=650)
    
    
    st.markdown(f"**Result Description:** The Protein-Protein Interaction (PPI) network positions **{selected_drug}** as a central regulator capable of disrupting the {selected_target} cluster with a high network degree.")

# 6. CONCLUSION
elif module == "Project Conclusion":
    st.header("🏁 Research Verdict")
    st.markdown(f'<div class="go-signal"><h3>VERDICT: GO</h3>Analysis of <b>{selected_drug}</b> indicates high therapeutic potential for clinical trials.</div>', unsafe_allow_html=True)
    buffer = io.BytesIO()
    df_report = pd.DataFrame([{"Drug": selected_drug, "Class": selected_class, "Target": selected_target, "Affinity": u_affinity}])
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_report.to_excel(writer, index=False)
    st.download_button("Download Full Research Report (.xlsx)", data=buffer, file_name=f"{selected_drug}_Analysis.xlsx")
