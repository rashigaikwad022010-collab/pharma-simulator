import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
from pyvis.network import Network
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import io

# --- SAFE IMPORT FOR VENN ---
try:
    from matplotlib_venn import venn2
    VENN_AVAILABLE = True
except ImportError:
    VENN_AVAILABLE = False

# --- UI SETTINGS ---
st.set_page_config(page_title="Advanced Pharma Pipeline", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .explanation-box { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #007bff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin: 20px 0; }
    .conclusion-card { padding: 30px; border-radius: 15px; border: 2px solid #eee; margin-top: 30px; }
    .go-signal { background-color: #d4edda; border-color: #28a745; color: #155724; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Advanced Pharmaceutical Research & Docking Pipeline")

# --- FULL DATABASE: 50+ CLASSES x 10 DRUGS ---
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
    "Anti-diabetics (Sulfonylureas)": ["Glipizide", "Glyburide", "Glimepiride", "Gliclazide", "Tolbutamide", "Chlorpropamide", "Acetohexamide", "Tolazamide", "Glibenclamide", "Glipentide"],
    "Anti-emetics": ["Domperidone", "Metoclopramide", "Aprepitant", "Rolapitant", "Promethazine", "Prochlorperazine", "Dronabinol", "Nabilone", "Scopolamine", "Casopitant"],
    "Anti-fungals (Azoles)": ["Fluconazole", "Itraconazole", "Ketoconazole", "Voriconazole", "Posaconazole", "Clotrimazole", "Miconazole", "Econazole", "Sertaconazole", "Isavuconazole"],
    "Anti-histamines (H1)": ["Cetirizine", "Loratadine", "Fexofenadine", "Diphenhydramine", "Chlorpheniramine", "Levocetirizine", "Desloratadine", "Azelastine", "Promethazine", "Cyproheptadine"],
    "Anti-malarials": ["Artemisinin", "Chloroquine", "Quinine", "Mefloquine", "Primaquine", "Lumefantrine", "Atovaquone", "Proguanil", "Pyrimethamine", "Artesunate"],
    "Anti-mycotics (Polyenes)": ["Amphotericin B", "Nystatin", "Natamycin", "Rimocidin", "Filipin", "Hamycin", "Perimycin", "Griseofulvin", "Flucytosine", "Caspofungin"],
    "Anti-neoplastics (Alkylating)": ["Cyclophosphamide", "Ifosfamide", "Melphalan", "Chlorambucil", "Busulfan", "Thiotepa", "Carmustine", "Lomustine", "Dacarbazine", "Temozolomide"],
    "Anti-platelets": ["Clopidogrel", "Aspirin", "Ticagrelor", "Prasugrel", "Tirofiban", "Eptifibatide", "Abciximab", "Dipyridamole", "Cilostazol", "Vorapaxar"],
    "Anti-psychotics (Atypical)": ["Quetiapine", "Risperidone", "Olanzapine", "Clozapine", "Aripiprazole", "Ziprasidone", "Lurasidone", "Paliperidone", "Asenapine", "Iloperidone"],
    "Anti-retrovirals (NRTI)": ["Zidovudine", "Lamivudine", "Abacavir", "Tenofovir", "Emtricitabine", "Didanosine", "Stavudine", "Zalcitabine", "Entecavir", "Telbivudine"],
    "Anti-tuberculars": ["Isoniazid", "Rifampicin", "Pyrazinamide", "Ethambutol", "Bedaquiline", "Delamanid", "Streptomycin", "Ethionamide", "Cycloserine", "Capreomycin"],
    "Barbiturates": ["Phenobarbital", "Secobarbital", "Pentobarbital", "Amobarbital", "Butabarbital", "Methohexital", "Thiopental", "Alphenal", "Barbital", "Allobarbital"],
    "Benzodiazepines": ["Diazepam", "Lorazepam", "Alprazolam", "Clonazepam", "Midazolam", "Temazepam", "Oxazepam", "Chlordiazepoxide", "Flurazepam", "Triazolam"],
    "Beta-Blockers": ["Metoprolol", "Atenolol", "Propranolol", "Bisoprolol", "Carvedilol", "Nadolol", "Nebivolol", "Esmolol", "Labetalol", "Pindolol"],
    "Bisphosphonates": ["Alendronate", "Risedronate", "Ibandronate", "Zoledronic acid", "Etidronate", "Pamidronate", "Tiludronate", "Clodronate", "Neridronate", "Olpadronate"],
    "Calcium Channel Blockers": ["Amlodipine", "Nifedipine", "Diltiazem", "Verapamil", "Felodipine", "Nicardipine", "Isradipine", "Nisoldipine", "Nimodipine", "Clevidipine"],
    "Cephalosporins (1st Gen)": ["Cefazolin", "Cephalexin", "Cefadroxil", "Cephradine", "Cephalothin", "Cephapirin", "Cefezet", "Cefazaflur", "Cefalonium", "Cefaloridine"],
    "Cephalosporins (2nd Gen)": ["Cefuroxime", "Cefaclor", "Cefoxitin", "Cefotetan", "Cefprozil", "Cefonicid", "Cefmetazole", "Ceforanide", "Cefuzonam", "Loracarbef"],
    "Cephalosporins (3rd Gen)": ["Ceftriaxone", "Cefotaxime", "Ceftazidime", "Cefixime", "Cefpodoxime", "Cefdinir", "Ceftibuten", "Cefoperazone", "Ceftizoxime", "Cefditoren"],
    "Corticosteroids": ["Prednisone", "Dexamethasone", "Hydrocortisone", "Methylprednisolone", "Betamethasone", "Fludrocortisone", "Triamcinolone", "Budesonide", "Mometasone", "Fluticasone"],
    "DPP-4 Inhibitors": ["Sitagliptin", "Vildagliptin", "Saxagliptin", "Linagliptin", "Alogliptin", "Gemigliptin", "Teneligliptin", "Anagliptin", "Trelagliptin", "Omarigliptin"],
    "Diuretics (Loop)": ["Furosemide", "Bumetanide", "Torsemide", "Ethacrynic acid", "Azosemide", "Muzolimine", "Piretanide", "Tripamide", "Etozolin", "Ozolinone"],
    "Diuretics (Thiazide)": ["Hydrochlorothiazide", "Chlorthalidone", "Indapamide", "Metolazone", "Chlorothiazide", "Methyclothiazide", "Bendroflumethiazide", "Polythiazide", "Cyclothiazide", "Quinethazone"],
    "Fluoroquinolones": ["Ciprofloxacin", "Levofloxacin", "Moxifloxacin", "Ofloxacin", "Norfloxacin", "Gemifloxacin", "Gatifloxacin", "Delafloxacin", "Lomefloxacin", "Sparfloxacin"],
    "H2-Receptor Antagonists": ["Famotidine", "Ranitidine", "Cimetidine", "Nizatidine", "Roxatidine", "Lafutidine", "Niperotidine", "Ebrotidine", "Burimamide", "Metiamide"],
    "HMG-CoA Reductase Inhibitors": ["Atorvastatin", "Rosuvastatin", "Simvastatin", "Pravastatin", "Lovastatin", "Fluvastatin", "Pitavastatin", "Cerivastatin", "Mevastatin", "Dalvastatin"],
    "Inhaled Beta-2 Agonists": ["Albuterol", "Salmeterol", "Formoterol", "Levalbuterol", "Indacaterol", "Vilanterol", "Olodaterol", "Terbutaline", "Metaproterenol", "Fenoterol"],
    "Kinase Inhibitors": ["Imatinib", "Erlotinib", "Gefitinib", "Sunitinib", "Sorafenib", "Dasatinib", "Lapatinib", "Nilotinib", "Pazopanib", "Afatinib"],
    "Macrolides": ["Azithromycin", "Clarithromycin", "Erythromycin", "Telithromycin", "Fidaxomicin", "Spiramycin", "Josamycin", "Roxithromycin", "Oleandomycin", "Kitasamycin"],
    "Monoclonal Antibodies": ["Pembrolizumab", "Rituximab", "Trastuzumab", "Adalimumab", "Infliximab", "Bevacizumab", "Nivolumab", "Ustekinumab", "Dupilumab", "Ocrelizumab"],
    "NSAIDs": ["Ibuprofen", "Naproxen", "Celecoxib", "Diclofenac", "Aspirin", "Meloxicam", "Etodolac", "Indomethacin", "Ketorolac", "Nabumetone"],
    "Narcotic Analgesics": ["Morphine", "Fentanyl", "Oxycodone", "Codeine", "Hydromorphone", "Methadone", "Meperidine", "Tramadol", "Buprenorphine", "Hydrocodone"],
    "Nitroimidazoles": ["Metronidazole", "Tinidazole", "Nimorazole", "Dimetridazole", "Pretomanid", "Fexinidazole", "Satranidazole", "Secnidazole", "Ornidazole", "Azomycin"],
    "Penicillins (Broad Spectrum)": ["Amoxicillin", "Ampicillin", "Piperacillin", "Ticarcillin", "Bacampicillin", "Azlocillin", "Mezlocillin", "Carbenicillin", "Talampicillin", "Pivampicillin"],
    "Proton Pump Inhibitors": ["Omeprazole", "Pantoprazole", "Lansoprazole", "Esomeprazole", "Rabeprazole", "Dexlansoprazole", "Tenatoprazole", "Ilaprazole", "Picoprazole", "Omeprazole Magnesium"],
    "SGLT2 Inhibitors": ["Canagliflozin", "Dapagliflozin", "Empagliflozin", "Ertugliflozin", "Ipragliflozin", "Luseogliflozin", "Tofogliflozin", "Sergliflozin", "Remogliflozin", "Sotagliflozin"],
    "Statins": ["Atorvastatin", "Simvastatin", "Rosuvastatin", "Pravastatin", "Lovastatin", "Fluvastatin", "Pitavastatin", "Cerivastatin", "Mevastatin", "Glenvastatin"],
    "Sulfonamides": ["Sulfamethoxazole", "Sulfadiazine", "Sulfasalazine", "Sulfisoxazole", "Sulfacetamide", "Sulfadoxine", "Sulfamethizole", "Sulfanilamide", "Sulfapyridine", "Sulfathiazole"],
    "Tetracyclines": ["Doxycycline", "Minocycline", "Tetracycline", "Tigecycline", "Oxytetracycline", "Demeclocycline", "Lymecycline", "Meclocycline", "Methacycline", "Rolitetracycline"],
    "Vinca Alkaloids": ["Vincristine", "Vinblastine", "Vinorelbine", "Vindesine", "Vinflunine", "Vinperine", "Vincadioline", "Vincatene", "Vinrosidine", "Vinzolidine"]
}

# --- SIDEBAR ---
st.sidebar.header("🔬 Research Controls")
selected_class = st.sidebar.selectbox("Drug Category:", sorted(drug_class_db.keys()))
selected_drug = st.sidebar.selectbox("Lead Compound:", drug_class_db[selected_class])
selected_target = st.sidebar.selectbox("Target Protein:", ["CASP3", "HTR3A", "COX2", "EGFR", "STAT3", "TNF-alpha", "ACE2", "HMGCR"])

random.seed(selected_drug + selected_target)
binding_energy = round(random.uniform(-11.5, -4.5), 1)

module = st.sidebar.selectbox("Pipeline Stage:", 
    ["Virtual Screening", "Venn Diagram Analysis", "Network Pharmacology Explorer", "Molecular Docking", "Project Conclusion"])

# -------------------------------------------------
# 1. VIRTUAL SCREENING
# -------------------------------------------------
if module == "Virtual Screening":
    st.header(f"🧪 Screening Module: {selected_class}")
    
    # Selection Menus for Filtering
    c1, c2 = st.columns(2)
    with c1: ob_filter = st.selectbox("Select Minimum OB (%) Filter:", [15, 20, 30, 40, 50], index=2)
    with c2: dl_filter = st.selectbox("Select Minimum DL Filter:", [0.10, 0.15, 0.18, 0.25, 0.35], index=2)

    # Table 1: ADME Screening
    res = []
    for d in drug_class_db[selected_class][:5]:
        ob_val = random.randint(18, 75)
        dl_val = round(random.uniform(0.12, 0.80), 2)
        status = "✅ PASS" if (ob_val >= ob_filter and dl_val >= dl_filter) else "❌ FAIL"
        res.append([d, round(random.uniform(300, 550), 2), f"{ob_val}%", dl_val, binding_energy, status])
    
    st.table(pd.DataFrame(res, columns=["Molecule Name", "MW (g/mol)", "OB (%)", "DL", "Affinity", "Status"]))

    # Table 2: CONSTITUENTS TABLE (Exact requested format)
    st.markdown("---")
    st.subheader("🧬 Bioactive Constituent Profile")
    constituent_data = [
        ["isovitexin", "Saponaretin", "C1=CC(=CC=C1C2=CC(=O)C3=C(O2)C=C(C(=C3O)[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O)O", "162350", "MOL002322"],
        ["Leucanthoside", "Isoorientin 7-methyl ether", "COC1=C(C(=C2C(=C1)OC(=CC2=O)C3=CC(=C(C=C3)O)O)O)[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O", "442659", "MOL003137"],
        ["gentirigenic acid", "GENTIRIGENate", "C[C@@]12CC[C@@H]([C@H]1CC[C@H]3[C@]2(CC[C@@H]4[C@@]3(CC[C@@H]([C@]4(C)CO)O)C)C)[C@@]5(C[C@@H]([C@@H](C(O5)(C)C)O)O)C(=O)O", "44423055", "MOL003143"],
        ["sitosterol", "Beta-sistosterol", "CC[C@@H](CC[C@@H](C)[C@H]1CC[C@@H]2[C@@]1(CC[C@H]3[C@H]2CCC4[C@@]3(CC[C@@H](C4)O)C)C)C(C)C", "12303645", "MOL000359"]
    ]
    st.table(pd.DataFrame(constituent_data, columns=["CONSTITUENTS NAME", "TCM NAME / SYM(PB)", "SMILE", "PUBCHEM ID", "MOL ID"]))

# -------------------------------------------------
# 2. VENN DIAGRAM
# -------------------------------------------------
elif module == "Venn Diagram Analysis":
    st.header("📊 Target Overlap Analysis")
    if VENN_AVAILABLE:
        fig, ax = plt.subplots(figsize=(8, 5))
        venn2(subsets=(45, 35, 52), set_labels=(f'Targets ({selected_drug})', 'Disease Targets'))
        st.pyplot(fig)
    st.table(pd.DataFrame({"Target Symbol": ["AKT1", "TP53", "VEGFA", "CASP3", "TNF", "STAT3"], "Role": ["Survival", "Apoptosis", "Angiogenesis", "Caspase", "Cytokine", "Transcription"]}))

# -------------------------------------------------
# 3. NETWORK PHARMACOLOGY (MESSY STRING)
# -------------------------------------------------
elif module == "Network Pharmacology Explorer":
    st.header("🕸️ PPI Network (STRING v11.5 Aesthetic)")
    net = Network(height="650px", width="100%", bgcolor="#ffffff", font_color="black")
    net.add_node(selected_drug, label=selected_drug, color="#ff4b4b", size=55, shape="star")
    
    hubs = ["AKT1", "TP53", "VEGFA", "CASP3", "EGFR", "TNF", "STAT3", "ESR1", "MAPK1", "IL6", "JUN", "MYC", "PTGS2", "CCND1", "MTOR"]
    for i, t in enumerate(hubs):
        net.add_node(t, label=t, color="#1c83e1", size=35)
        net.add_edge(selected_drug, t, width=2, color="#2c3e50")
        for t2 in hubs[i+1:]:
            if random.random() > 0.4: # Creating "messy" high-density connections
                net.add_edge(t, t2, width=1, color="#bdc3c7", alpha=0.5)
    
    net.toggle_physics(True)
    net.save_graph("string_net.html")
    with open("string_net.html", 'r') as f: components.html(f.read(), height=700)
    
    

# -------------------------------------------------
# 4. DOCKING / 5. CONCLUSION
# -------------------------------------------------
elif module == "Molecular Docking":
    st.header("🧩 In-Silico Docking Analysis")
    poses = [[i, round(binding_energy + random.uniform(-0.4, 0.4), 2), "H-Bond / Pi-Stacking"] for i in range(1, 6)]
    st.table(pd.DataFrame(poses, columns=["Pose ID", "Affinity (kcal/mol)", "Primary Interaction"]))

elif module == "Project Conclusion":
    st.header("🏁 Research Verdict")
    st.markdown(f'<div class="conclusion-card go-signal"><h2 style="text-align: center;">VERDICT: GO</h2><p style="text-align: center;">Systemic analysis of <b>{selected_drug}</b> indicates high therapeutic potential.</p></div>', unsafe_allow_html=True)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        pd.DataFrame([{"Drug": selected_drug, "Class": selected_class, "Affinity": binding_energy}]).to_excel(writer, index=False)
    st.download_button(label="Download Clinical Report (.xlsx)", data=buffer, file_name=f"{selected_drug}_Report.xlsx", mime="application/vnd.ms-excel")
