import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import curve_fit

st.set_page_config(layout="wide")

st.title("Virtual Pharmacology Lab Simulator")

# ------------------------------------------------
# EXPERIMENT SELECTOR
# ------------------------------------------------

experiment = st.sidebar.selectbox(
    "Select Experiment",
    [
        "Organ Bath Simulator",
        "3 Point Bioassay",
        "4 Point Bioassay"
    ]
)

# ------------------------------------------------
# THEORY
# ------------------------------------------------

with st.expander("Experiment Theory"):

    st.write("""
Bioassay is a method used to determine the potency of a drug using a biological system.

The isolated rat ileum preparation is commonly used in pharmacology laboratories
to study the effect of drugs on smooth muscle contraction.

Acetylcholine acts on muscarinic receptors producing contraction of intestinal smooth muscle.

Drug doses are added to an organ bath containing the ileum segment and the contraction
is recorded using a lever attached to a kymograph drum.

Increasing doses of an agonist produce increasing responses until a maximum response is reached.

Plotting log dose against response produces a sigmoid dose response curve from which EC50
(the dose producing 50% of maximal response) can be determined.

Bioassay techniques compare the response of a standard drug with that of an unknown test drug.

In the three point bioassay two standard doses and one test dose are used.

In the four point bioassay two doses of standard drug (S1, S2) and two doses of test drug
(T1, T2) are used to calculate relative potency.
""")

# ------------------------------------------------
# ORGAN BATH SIMULATOR
# ------------------------------------------------

if experiment == "Organ Bath Simulator":

    st.header("Organ Bath Dose Response Experiment")

    drug = st.selectbox(
        "Select Drug",
        [
            "Acetylcholine",
            "Acetylcholine + Atropine",
            "Acetylcholine + Neostigmine",
            "Histamine"
        ]
    )

    doses = np.array([0.1, 0.3, 1, 3, 10])

    def hill(x, Emax, EC50):
        return Emax * x / (EC50 + x)

    if drug == "Acetylcholine":
        Emax = 100
        EC50 = 1

    elif drug == "Acetylcholine + Atropine":
        Emax = 100
        EC50 = 3

    elif drug == "Acetylcholine + Neostigmine":
        Emax = 120
        EC50 = 0.5

    elif drug == "Histamine":
        Emax = 90
        EC50 = 1.2

    responses = hill(doses, Emax, EC50) + np.random.normal(0, 3, len(doses))

    percent = responses / np.max(responses) * 100

    table = pd.DataFrame({
        "Dose": doses,
        "Response": responses,
        "% Response": percent
    })

    st.subheader("Experimental Data")

    st.dataframe(table)

    # ---------------------------
    # DRUM RECORDING
    # ---------------------------

    st.subheader("Organ Bath Drum Recording")

    time = np.linspace(0, 60, 600)

    trace = np.zeros_like(time)

    for i, r in enumerate(responses):

        start = i * 100 + 20

        wave = np.exp(-np.linspace(0, 2, 40)) * r / 10

        trace[start:start + 40] = wave

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=time, y=trace, mode="lines"))

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Tension"
    )

    st.plotly_chart(fig)

    # ---------------------------
    # DOSE RESPONSE CURVE
    # ---------------------------

    st.subheader("Log Dose Response Curve")

    logdose = np.log10(doses)

    def sigmoid(x, Emax, EC50):

        return Emax / (1 + 10 ** (EC50 - x))

    popt, _ = curve_fit(sigmoid, logdose, percent)

    x = np.linspace(min(logdose), max(logdose), 100)

    curve1 = sigmoid(x, *popt)

    curve2 = sigmoid(x, popt[0], popt[1] + 0.5)

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=logdose,
        y=percent,
        mode="markers",
        name="Observed"
    ))

    fig2.add_trace(go.Scatter(
        x=x,
        y=curve1,
        name="ACh Curve"
    ))

    fig2.add_trace(go.Scatter(
        x=x,
        y=curve2,
        name="ACh + Atropine"
    ))

    fig2.update_layout(
        xaxis_title="Log Dose",
        yaxis_title="% Response"
    )

    st.plotly_chart(fig2)

    EC50_value = 10 ** popt[1]

    st.write("Estimated EC50:", round(EC50_value, 3))

# ------------------------------------------------
# THREE POINT BIOASSAY
# ------------------------------------------------

elif experiment == "3 Point Bioassay":

    st.header("Three Point Bioassay")

    st.write("Sequence: S1 → T → S2")

    S1 = st.number_input("Response S1", value=10.0)

    T = st.number_input("Response Test", value=15.0)

    S2 = st.number_input("Response S2", value=20.0)

    table = pd.DataFrame({
        "Dose": ["S1", "T", "S2"],
        "Response": [S1, T, S2]
    })

    st.dataframe(table)

    potency = (T - S1) / (S2 - S1)

    st.write("Relative Potency:", round(potency, 3))

# ------------------------------------------------
# FOUR POINT BIOASSAY
# ------------------------------------------------

elif experiment == "4 Point Bioassay":

    st.header("Four Point Bioassay")

    st.write("Standard doses: S1, S2   Test doses: T1, T2")

    S1 = st.number_input("Response S1", value=10.0)

    S2 = st.number_input("Response S2", value=20.0)

    T1 = st.number_input("Response T1", value=12.0)

    T2 = st.number_input("Response T2", value=18.0)

    table = pd.DataFrame({
        "Dose": ["S1", "S2", "T1", "T2"],
        "Response": [S1, S2, T1, T2]
    })

    st.dataframe(table)

    potency = ((T2 - S2) + (T1 - S1)) / ((T2 - T1) + (S2 - S1))

    st.write("Relative Potency:", round(potency, 3))

    st.subheader("Latin Square Sequence")

    latin = [
        ["S1", "S2", "T1", "T2"],
        ["S2", "T1", "T2", "S1"],
        ["T1", "T2", "S1", "S2"],
        ["T2", "S1", "S2", "T1"]
    ]

    st.table(latin)
