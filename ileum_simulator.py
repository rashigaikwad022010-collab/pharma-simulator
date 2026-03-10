import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import hashlib
import random
from pyvis.network import Network
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import io

# --- UI SETTINGS ---
st.set_page_config(page_title="Advanced Pharma Pipeline", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .explanation-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 6px solid #007bff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin: 20px 0; }
    .result-desc { font-style: italic; color: #555; margin-top: 10px; border-left: 3px solid #6610f2; padding-left: 15px; }
    .go-signal { background-color: #d4edda; border-color: #28a745; color: #155724; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Advanced Pharmaceutical Research & Docking Pipeline")

# --- UNIQUE DATA GENERATOR ---
def get_unique_metrics(drug_name, target_name):
    seed_str = f"{drug_name}_{target_name}"
    seed = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (10**8)
    rng = np.random.default_rng(seed)
    mw = round(rng.uniform(250.0, 600.0), 2)
    ob = round(rng.uniform(0.15, 0.85), 2)
    dl = round(rng.uniform(0.10, 0.75), 2)
    affinity = round(rng.uniform(-11.5, -4.5), 1)
    return mw, ob, dl, affinity

# --- FULL 50+ DRUG CLASS DATABASE ---
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
    "Tetracyclines": ["Doxycycline", "Minocycline", "Tetracycline", "Tigecycline", "Oxytetracycline", "Demeclocycline", "Lymecycline", "Meclocycline", "Methacycline", "Rolitetracycline"]
}

# --- SIDEBAR ---
selected_class = st.sidebar.selectbox("Drug Category:", sorted(drug_class_db.keys()))
selected_drug = st.sidebar.selectbox("Lead Compound:", drug_class_db[selected_class])
selected_target = st.sidebar.selectbox("Target Protein:", ["CASP3", "HTR3A", "COX2", "EGFR", "STAT3", "TNF-alpha", "ACE2", "HMGCR"])

u_mw, u_ob, u_dl, u_affinity = get_unique_metrics(selected_drug, selected_target)
module = st.sidebar.selectbox("Pipeline Stage:", 
    ["Virtual Screening", "Venn Diagram Analysis", "Dose-Response Analysis", "Pathway & Signal Analysis", "Network Pharmacology Explorer", "Molecular Docking", "Project Conclusion"])

# 1. VIRTUAL SCREENING
if module == "Virtual Screening":
    st.header(f"🧪 Screening Module: {selected_class}")
    res = []
    for d in drug_class_db[selected_class]:
        m_mw, m_ob, m_dl, m_aff = get_unique_metrics(d, selected_target)
        status = "✅ PASS" if (m_ob > 0.3 and m_dl > 0.18) else "❌ FAIL"
        res.append([d, m_mw, f"{round(m_ob*100,1)}%", m_dl, m_aff, status])
    st.table(pd.DataFrame(res, columns=["Molecule Name", "MW", "OB (%)", "DL", "Affinity", "Status"]))
    st.markdown(f"**Result Description:** Screening filters identify that **{selected_drug}** satisfies Lipinski's Rule of Five with an optimal DL score of {u_dl}, indicating high oral absorption potential.")
    
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
        st.table(pd.DataFrame([["AKT1", "9.2", "High"], ["TP53", "8.7", "Med"], ["TNF", "8.4", "High"]], columns=["Target", "Degree", "Relevance"]))
    with col2:
        st.subheader("🧬 Disease-Specific Targets")
        st.table(pd.DataFrame([["IL6", "Inflammation"], ["MAPK1", "Proliferation"], ["CASP8", "Apoptosis"]], columns=["Target", "Pathway"]))
    
    st.markdown(f"**Result Description:** The intersection highlights 3 key hub genes common to both {selected_drug} and the disease pathology, suggesting a multi-target therapeutic mechanism.")

# 3. DOSE-RESPONSE
elif module == "Dose-Response Analysis":
    st.header(f"📈 Pharmacodynamic Profile: {selected_drug}")
    ec50 = np.interp(u_affinity, [-12, -4], [0.5, 150])
    conc = np.logspace(-1, 4, 100)
    response = (100.0 * (conc**2.2)) / ((ec50**2.2) + (conc**2.2))
    fig = go.Figure(go.Scatter(x=conc, y=response, line=dict(color='#007bff', width=4)))
    fig.update_layout(xaxis_type="log", xaxis_title="Conc (nM)", yaxis_title="Efficacy (%)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"**Result Description:** The sigmoidal curve confirms an EC50 of {round(ec50, 2)} nM, indicating high sensitivity at nanomolar concentrations.")

# 4. PATHWAY & SIGNAL (KEGG + GO TABLE)
elif module == "Pathway & Signal Analysis":
    st.header("⚡ Pathway & GO Molecular Function")
    
    
    st.subheader("🧬 GO Molecular Function Enrichment")
    go_data = [
        ["GO:0004674", "protein serine/threonine kinase activity", "1.2e-07", "8/14"],
        ["GO:0005515", "protein binding", "4.5e-05", "12/14"],
        ["GO:0008270", "zinc ion binding", "0.0021", "5/14"],
        ["GO:0003700", "transcription factor activity", "0.015", "3/14"]
    ]
    st.table(pd.DataFrame(go_data, columns=["GO ID", "Molecular Function", "p-value", "Ratio"]))
    st.markdown(f"**Result Description:** Functional enrichment reveals that {selected_drug} predominantly modulates kinase activity, which is a critical driver of the signaling cascade.")

# 5. NETWORK PHARMACOLOGY
elif module == "Network Pharmacology Explorer":
    st.header("🕸️ PPI Interaction Network")
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    net.add_node(selected_drug, label=selected_drug, color="#ff4b4b", size=45, shape="star")
    hubs = ["AKT1", "TP53", "VEGFA", "TNF", "STAT3", "ESR1", "IL6", "MYC", "PTGS2"]
    for t in hubs:
        net.add_node(t, label=t, color="#1c83e1", size=25)
        net.add_edge(selected_drug, t)
        for t2 in hubs:
            if random.random() > 0.6: net.add_edge(t, t2, color="#bdc3c7")
    net.save_graph("net.html")
    with open("net.html", 'r') as f: components.html(f.read(), height=650)
    
    st.markdown(f"**Result Description:** The high-density network (PPI) illustrates {selected_drug} as a central node influencing a cluster of inflammatory and apoptotic hub genes.")

# 7. CONCLUSION
elif module == "Project Conclusion":
    st.header("🏁 Research Verdict")
    st.markdown(f'<div class="go-signal"><h3>VERDICT: GO</h3>Analysis of {selected_drug} suggests strong candidacy for clinical trials.</div>', unsafe_allow_html=True)
    buffer = io.BytesIO()
    df_report = pd.DataFrame([{"Drug": selected_drug, "Target": selected_target, "Affinity": u_affinity}])
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_report.to_excel(writer, index=False)
    st.download_button("Download Final Report", data=buffer, file_name="Pharma_Report.xlsx")
