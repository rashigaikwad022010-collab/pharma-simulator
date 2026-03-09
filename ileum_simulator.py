import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Virtual Pharmacology Lab", layout="wide")

st.title("🧪 Virtual Pharmacology Lab Simulator")

st.header("Organ Bath Dose Response Experiment")

# Session state to store experiment data
if "doses" not in st.session_state:
    st.session_state.doses = []

if "responses" not in st.session_state:
    st.session_state.responses = []

# Drug selection
drug = st.selectbox(
    "Select Drug",
    ["Acetylcholine", "Acetylcholine + Atropine"]
)

# Dose selector
dose = st.slider(
    "Select Dose (µg)",
    min_value=0.1,
    max_value=10.0,
    step=0.1
)

# Response simulation function
def response_function(dose, drug):
    
    if drug == "Acetylcholine":
        Emax = 100
        EC50 = 2
        
    else:  # Acetylcholine + Atropine
        Emax = 100
        EC50 = 5
        
    response = (Emax * dose) / (EC50 + dose)
    
    noise = np.random.normal(0,2)
    
    return max(response + noise,0)

col1, col2 = st.columns(2)

with col1:

    if st.button("Inject Dose"):
        
        resp = response_function(dose, drug)

        st.session_state.doses.append(dose)
        st.session_state.responses.append(resp)

        st.success(f"Injected {dose} µg of {drug}")

with col2:

    if st.button("Wash Tissue"):
        
        st.session_state.doses = []
        st.session_state.responses = []
        
        st.warning("Tissue washed. Experiment reset.")

st.subheader("Organ Bath Drum Recording")

if len(st.session_state.responses) > 0:

    contraction = st.session_state.responses[-1]

    x = np.linspace(0,10,200)
    y = contraction + np.sin(x)*contraction*0.1

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=x, y=y, mode='lines', name="Contraction")
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Tissue Contraction",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

st.subheader("Experimental Data")

if len(st.session_state.doses) > 0:

    df = pd.DataFrame({
        "Dose (µg)": st.session_state.doses,
        "Response": st.session_state.responses
    })

    st.dataframe(df)

st.subheader("Log Dose Response Curve")

if len(st.session_state.doses) > 1:

    log_dose = np.log10(st.session_state.doses)

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=log_dose,
            y=st.session_state.responses,
            mode="lines+markers",
            name="Dose Response"
        )
    )

    fig2.update_layout(
        xaxis_title="Log Dose",
        yaxis_title="Response",
        height=400
    )

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.markdown("Author: **Rashi Gaikwad**")
