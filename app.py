import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pharmacology Simulator", layout="centered")

st.title("🧪 Pharmacology Simulator")
st.write("College-level drug interaction & dose-response simulator")

st.header("Patient Details")
age = st.slider("Age (years)", 1, 90, 25)
kidney = st.selectbox("Kidney Function", ["Normal", "Impaired"])
liver = st.selectbox("Liver Function", ["Normal", "Impaired"])

st.header("Drug Selection")

drugs = ["Paracetamol", "Ibuprofen", "Warfarin", "Aspirin", "Ciprofloxacin"]

drug_a = st.selectbox("Drug A", drugs)
drug_b = st.selectbox("Drug B", drugs)

dose = st.slider("Dose of Drug A (mg)", 50, 1000, 500)

st.header("Interaction Result")

interaction = "Minor"
effect = "No significant effect"
toxicity_score = 20

interaction_score = 0

# Drug-based risk
if drug_a != drug_b:
    interaction_score += 1

if "Warfarin" in [drug_a, drug_b]:
    interaction_score += 3

# Patient factors
if kidney == "Impaired":
    interaction_score += 2

if liver == "Impaired":
    interaction_score += 2

if age > 65:
    interaction_score += 1

# Dose factor
if dose > 500:
    interaction_score += 2

# Final interpretation
if interaction_score <= 2:
    interaction = "Minor"
    effect = "No significant effect"
elif interaction_score <= 5:
    interaction = "Moderate"
    effect = "Increased toxicity risk"
else:
    interaction = "Severe"
    effect = "High toxicity / unsafe combination"
toxicity_score = (
    (dose / 1000) * 40 +
    (age / 90) * 20 +
    (20 if kidney == "Impaired" else 0) +
    (20 if liver == "Impaired" else 0)
)

if "Warfarin" in [drug_a, drug_b]:
    toxicity_score += 15

toxicity_score = min(round(toxicity_score, 1), 100)


st.subheader("Interaction Level:")
st.success(interaction)

st.subheader("Effect Type:")
st.info(effect)

st.subheader("Predicted Toxicity Score:")
st.progress(toxicity_score / 100)

st.header("Dose–Response Curve")

dose_range = np.linspace(0, 1000, 50)
response = (dose_range / (dose_range + 200)) * 100

fig, ax = plt.subplots()
ax.plot(dose_range, response)
ax.set_xlabel("Dose (mg)")
ax.set_ylabel("Effect (%)")
ax.set_title("Dose–Response Curve")

st.pyplot(fig)

st.caption("⚠️ Educational use only. Not for clinical decision-making.")
