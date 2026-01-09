import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Chicken Ileum Dose–Response Simulator (Virtual Lab)",
    layout="centered"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🧪 Chicken Ileum Dose–Response Simulator (Virtual Lab)")
st.subheader("Educational Pharmacology Practical Simulator (Zero Lab Exposure)")

# -----------------------------
# THEORY SECTION
# -----------------------------
with st.expander("📘 Experiment Description & Virtual Lab Theory"):
    st.markdown("""
### Aim
To study the dose–response relationship of a drug using isolated chicken ileum, simulated for virtual lab learning.

### Principle
Chicken ileum contains smooth muscle that contracts in response to agonists like acetylcholine. Increasing doses produce increasing contractions until a maximum response is reached.

### Virtual Lab Simulation
- Students **can visualize drug responses without real tissue**.
- The app can **generate realistic dose–response data automatically**.
- Two-drug interactions can be simulated:
    - **Competitive antagonism**: shifts Drug A curve to the right without changing max response.  
      $$ Response_{A\\,with\\,B} = \\frac{Max \\times Dose^n}{EC50 \\times (1 + [B]/Ki)^n + Dose^n} $$
    - **Non-competitive antagonism**: reduces maximum response.  
      $$ Response_{A\\,with\\,B} = Max \\times (1 - fraction\_blocked) \\times \\frac{Dose^n}{EC50^n + Dose^n} $$
- Students can also **enter their own experimental values** if desired.

### Procedure (Lab Method)
1. Isolated chicken ileum (2–3 cm) is mounted in an organ bath.
2. Tissue is bathed in physiological salt solution at 37°C.
3. Graded doses of drug are added.
4. Contractions are recorded using a kymograph.
5. Dose–response curves are plotted or simulated in this app.

### Learning Outcome
- Understand drug potency
- Observe graded dose responses
- Interpret pharmacological curves
- Learn about drug interactions virtually
""")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.header("🧾 Experimental Setup")

experiment_type = st.selectbox(
    "Select Experiment Type",
    ["Single Drug", "Two Drugs"]
)

use_simulation = st.checkbox(
    "Use Virtual Lab Simulation (Auto-generate responses)", value=True
)

# -----------------------------
# FUNCTION TO SIMULATE DOSE–RESPONSE
# -----------------------------
def simulate_response(doses, Max=20, EC50=2, n=1):
    return Max * (np.array(doses)**n) / (EC50**n + np.array(doses)**n)

# -----------------------------
# SINGLE DRUG SECTION
# -----------------------------
if experiment_type == "Single Drug":
    drug_name = st.text_input("Drug Name", value="Acetylcholine")
    
    st.markdown("### Enter doses (µg/mL)")
    doses = []
    for i in range(1, 6):
        dose = st.number_input(f"Dose {i}", min_value=0.0, step=0.1, key=f"sd_dose_{i}")
        doses.append(dose)
    
    if use_simulation:
        responses = simulate_response(doses)
        st.info("Responses auto-generated using virtual lab model")
    else:
        responses = []
        st.markdown("### Enter observed responses (mm contraction)")
        for i, dose in enumerate(doses):
            resp = st.number_input(f"Response for Dose {dose}", min_value=0.0, step=0.5, key=f"sd_resp_{i}")
            responses.append(resp)
    
    # -----------------------------
    # DATA AND PLOT
    # -----------------------------
    if st.button("📊 Generate Dose–Response Curve (Single Drug)"):
        data = pd.DataFrame({"Dose (µg/mL)": doses, "Response (mm)": responses})
        data["Log Dose"] = np.log10(data["Dose (µg/mL)"] + 1e-6)
        
        st.subheader("📋 Experimental Data Table")
        st.dataframe(data)
        
        fig, ax = plt.subplots()
        ax.plot(data["Log Dose"], data["Response (mm)"], marker="o")
        ax.set_xlabel("Log Dose (µg/mL)")
        ax.set_ylabel("Contraction Response (mm)")
        ax.set_title(f"Dose–Response Curve of {drug_name}")
        ax.grid(True)
        st.pyplot(fig)
        
        st.subheader("🧠 Interpretation")
        st.markdown(f"""
- The response increases with increasing dose of **{drug_name}**
- Demonstrates a **graded dose–response relationship**
- Curve can be used to study potency or compare with other drugs
        """)

# -----------------------------
# TWO DRUG SECTION
# -----------------------------
else:
    st.subheader("Drug A")
    drug_A = st.text_input("Drug A Name", value="Acetylcholine")
    doses_A = []
    for i in range(1, 6):
        dose = st.number_input(f"Drug A Dose {i}", min_value=0.0, step=0.1, key=f"da_dose_{i}")
        doses_A.append(dose)
    
    st.subheader("Drug B")
    drug_B = st.text_input("Drug B Name", value="Atropine")
    doses_B = []
    for i in range(1, 6):
        dose = st.number_input(f"Drug B Dose {i}", min_value=0.0, step=0.1, key=f"db_dose_{i}")
        doses_B.append(dose)
    
    interaction = st.selectbox("Type of interaction", ["Competitive Antagonist", "Non-competitive Antagonist", "No Interaction"])
    
    if use_simulation:
        responses_A = simulate_response(doses_A)
        responses_B = simulate_response(doses_B, Max=15)
        
        # Simulate interaction
        if interaction == "Competitive Antagonist":
            Ki = 2  # constant for simplicity
            responses_A_with_B = responses_A / (1 + np.array(doses_B)/Ki)
        elif interaction == "Non-competitive Antagonist":
            fraction_blocked = 0.4  # reduces max 40%
            responses_A_with_B = responses_A * (1 - fraction_blocked)
        else:
            responses_A_with_B = responses_A
        
        st.info("Responses auto-generated using virtual lab model")
    else:
        responses_A = []
        responses_B = []
        st.markdown("### Enter observed responses for Drug A")
        for i, dose in enumerate(doses_A):
            resp = st.number_input(f"Response for Drug A Dose {dose}", min_value=0.0, step=0.5, key=f"da_resp_{i}")
            responses_A.append(resp)
        st.markdown("### Enter observed responses for Drug B")
        for i, dose in enumerate(doses_B):
            resp = st.number_input(f"Response for Drug B Dose {dose}", min_value=0.0, step=0.5, key=f"db_resp_{i}")
            responses_B.append(resp)
        responses_A_with_B = responses_A  # No automatic interaction
    
    if st.button("📊 Generate Dose–Response Curve (Two Drugs)"):
        data_A = pd.DataFrame({"Dose (µg/mL)": doses_A, "Response (mm)": responses_A, "Response with B": responses_A_with_B})
        data_B = pd.DataFrame({"Dose (µg/mL)": doses_B, "Response (mm)": responses_B})
        
        data_A["Log Dose"] = np.log10(data_A["Dose (µg/mL)"] + 1e-6)
        data_B["Log Dose"] = np.log10(data_B["Dose (µg/mL)"] + 1e-6)
        
        st.subheader("📋 Experimental Data Table - Drug A")
        st.dataframe(data_A)
        st.subheader("📋 Experimental Data Table - Drug B")
        st.dataframe(data_B)
        
        fig, ax = plt.subplots()
        ax.plot(data_A["Log Dose"], data_A["Response (mm)"], 'o-', label=f"{drug_A} Alone")
        ax.plot(data_A["Log Dose"], data_A["Response with B"], 's--', label=f"{drug_A} with {drug_B}")
        ax.plot(data_B["Log Dose"], data_B["Response (mm)"], 'd-', label=f"{drug_B} Alone")
        ax.set_xlabel("Log Dose (µg/mL)")
        ax.set_ylabel("Contraction Response (mm)")
        ax.set_title("Dose–Response Curves (Two Drugs)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        
        st.subheader("🧠 Interpretation")
        st.markdown(f"""
- The curves show how **{drug_A}** responds alone and in presence of **{drug_B}**.
- **{interaction}** interaction is demonstrated.
- This virtual lab allows study of **drug potency, graded responses, and drug interactions** without real tissue.
        """)
