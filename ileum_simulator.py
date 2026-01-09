import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Chicken Ileum Dose–Response Simulator",
    layout="centered"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🧪 Chicken Ileum Dose–Response Simulator")
st.subheader("Educational Pharmacology Practical Simulator")

# -----------------------------
# THEORY SECTION
# -----------------------------
with st.expander("📘 Experiment Description (Click to Expand)"):
    st.markdown("""
### Aim
To study the dose–response relationship of a drug using isolated chicken ileum.

### Principle
Chicken ileum contains smooth muscle that contracts in response to agonists
like acetylcholine. Increasing doses produce increasing contractions until
a maximum response is reached.

### Procedure (Lab Method)
1. Isolated chicken ileum (2–3 cm) is mounted in an organ bath.
2. Tissue is bathed in physiological salt solution at 37°C.
3. Graded doses of drug are added.
4. Contractions are recorded using a kymograph.
5. A dose–response curve is plotted.

### Learning Outcome
- Understand drug potency
- Observe graded dose responses
- Interpret pharmacological curves
""")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.header("🧾 Enter Experimental Data")

drug_name = st.text_input("Drug Name", value="Acetylcholine")

st.markdown("### Enter doses and observed contractions")

dose_list = []
response_list = []

for i in range(1, 6):
    col1, col2 = st.columns(2)
    with col1:
        dose = st.number_input(
            f"Dose {i} (µg/mL)",
            min_value=0.0,
            step=0.1,
            key=f"dose_{i}"
        )
    with col2:
        response = st.number_input(
            f"Response {i} (mm contraction)",
            min_value=0.0,
            step=0.5,
            key=f"response_{i}"
        )
    dose_list.append(dose)
    response_list.append(response)

# -----------------------------
# DATA PROCESSING
# -----------------------------
if st.button("📊 Generate Dose–Response Curve"):
    if all(d > 0 for d in dose_list) and all(r > 0 for r in response_list):
        data = pd.DataFrame({
            "Dose (µg/mL)": dose_list,
            "Response (mm)": response_list
        })

        data["Log Dose"] = np.log10(data["Dose (µg/mL)"])

        st.success("Dose–response data recorded successfully")

        st.subheader("📋 Experimental Data Table")
        st.dataframe(data)

        # -----------------------------
        # PLOT
        # -----------------------------
        fig, ax = plt.subplots()
        ax.plot(data["Log Dose"], data["Response (mm)"], marker="o")
        ax.set_xlabel("Log Dose (µg/mL)")
        ax.set_ylabel("Contraction Response (mm)")
        ax.set_title(f"Dose–Response Curve of {drug_name}")
        ax.grid(True)

        st.pyplot(fig)

        # -----------------------------
        # INTERPRETATION
        # -----------------------------
        st.subheader("🧠 Interpretation")
        st.markdown(f"""
- The response increases with increasing dose of **{drug_name}**
- This demonstrates a **graded dose–response relationship**
- The curve can be used to compare potency with other drugs
        """)

    else:
        st.error("⚠️ Please enter NON-ZERO values for all doses and responses")
