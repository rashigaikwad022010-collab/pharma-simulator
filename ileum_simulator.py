import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
st.subheader("Interactive Pharmacology Practical Simulator (Zero Lab Exposure)")

# -----------------------------
# GENERAL THEORY
# -----------------------------
with st.expander("📘 General Theory"):
    st.markdown("""
### Aim
Study the dose–response relationship of a drug using chicken ileum (virtual lab).  

### Principle
- Smooth muscle in chicken ileum contracts in response to agonists.  
- Graded doses produce increasing contraction until a maximum response is reached.  

### Virtual Lab
- Students can **simulate experiments** without real tissue.  
- Responses can be **auto-generated** or **entered manually**.  
- Drug interactions (competitive/non-competitive antagonists) can be visualized.
""")

# -----------------------------
# SELECT EXPERIMENT TYPE
# -----------------------------
experiment_type = st.selectbox(
    "Select Experiment Type",
    ["Single Drug", "Two Drugs"]
)

# -----------------------------
# EXTRA THEORY (CLICKABLE)
# -----------------------------
with st.expander("ℹ️ Extra Theory / Tips for this Experiment (Click to Read)"):
    st.markdown("""
**Single Drug Experiment:**  
- Observe graded responses.  
- Determine EC50 (dose producing 50% max response) and Emax (max contraction).  
- Compare potency with other drugs.  

**Two Drugs Experiment:**  
- Study agonist-antagonist interaction.  
- Competitive antagonism: rightward shift without changing max response.  
- Non-competitive antagonism: reduces maximum response.  
- Learn to interpret dose-response shifts and compare EC50 values.
""")

# -----------------------------
# STEP-BY-STEP VIRTUAL LAB VISUALS
# -----------------------------
with st.expander("🧪 Virtual Wet Lab Procedure (Images & GIFs)"):
    st.markdown("### Step 1: Chicken Ileum Isolation")
    st.image("images/ileum_isolated.jpg", caption="Isolated chicken ileum", use_column_width=True)
    
    st.markdown("### Step 2: Cleaning the Ileum")
    st.image("images/ileum_cleaned.jpg", caption="Ileum cleaned and trimmed", use_column_width=True)
    
    st.markdown("### Step 3: Mounting in Organ Bath")
    st.image("images/ileum_organ_bath.jpg", caption="Ileum mounted in organ bath", use_column_width=True)
    
    st.markdown("### Step 4: Connecting to Transducer/Simulator")
    st.image("images/organ_bath_transducer.jpg", caption="Tissue connected to recording device", use_column_width=True)
    
    st.markdown("### Step 5: Adding Drug & Recording Response")
    st.image("images/drug_added.gif", caption="Simulated tissue contraction", use_column_width=True)

# -----------------------------
# SIMULATION OPTION
# -----------------------------
use_simulation = st.checkbox("Use Virtual Lab Simulation (Auto-generate responses)", value=True)

# -----------------------------
# FUNCTION TO SIMULATE RESPONSE
# -----------------------------
def simulate_response(doses, Max=20, EC50=2, n=1):
    return Max * (np.array(doses)**n) / (EC50**n + np.array(doses)**n)

# -----------------------------
# SIDEBAR SLIDERS FOR ANIMATION
# -----------------------------
st.sidebar.header("⚙️ Simulation Parameters for Animated Plot")
Max_val = st.sidebar.slider("Maximum Response (Emax)", min_value=5, max_value=50, value=20, step=1)
EC50_val = st.sidebar.slider("EC50 (µg/mL)", min_value=0.1, max_value=20.0, value=2.0, step=0.1)
Hill_n = st.sidebar.slider("Hill Coefficient (n)", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
dose_max = st.sidebar.number_input("Maximum Dose (µg/mL) for Animation", min_value=1, max_value=50, value=10, step=1)

dose_points = np.linspace(0.1, dose_max, 20)
response_points = Max_val * (dose_points ** Hill_n) / (EC50_val ** Hill_n + dose_points ** Hill_n)

# -----------------------------
# SINGLE DRUG FLOW
# -----------------------------
if experiment_type == "Single Drug":
    drug_name = st.text_input("Drug Name", value="Acetylcholine")
    doses = [st.number_input(f"Dose {i} (µg/mL)", min_value=0.0, step=0.1, key=f"sd_dose_{i}") for i in range(1,6)]
    
    if use_simulation:
        responses = simulate_response(doses, Max=Max_val, EC50=EC50_val, n=Hill_n)
        st.info("Responses auto-generated using virtual lab model")
    else:
        responses = [st.number_input(f"Response for Dose {dose}", min_value=0.0, step=0.5, key=f"sd_resp_{i}") for i,dose in enumerate(doses)]
    
    if st.button("📊 Generate Dose–Response Curve (Single Drug)"):
        data = pd.DataFrame({"Dose (µg/mL)": doses, "Response (mm)": responses})
        data["Log Dose"] = np.log10(data["Dose (µg/mL)"]+1e-6)
        st.dataframe(data)
        
        # Animated interactive Plotly curve
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers',
                                 line=dict(color='blue', width=3),
                                 marker=dict(size=8),
                                 hovertemplate=
                                 "Dose: %{x}<br>Response: %{y}<br>EC50: "+str(EC50_val)+"<br>Emax: "+str(Max_val)+"<extra></extra>"))
        frames = [go.Frame(data=[go.Scatter(x=doses[:k+1], y=responses[:k+1])]) for k in range(len(doses))]
        fig.frames = frames
        fig.update_layout(
            title=f"Animated Dose–Response Curve of {drug_name}",
            xaxis_title="Dose (µg/mL)",
            yaxis_title="Response (mm)",
            updatemenus=[dict(type="buttons",
                              showactive=False,
                              buttons=[dict(label="Play",
                                            method="animate",
                                            args=[None, {"frame": {"duration": 200, "redraw": True},
                                                         "fromcurrent": True}]),
                                       dict(label="Pause",
                                            method="animate",
                                            args=[[None], {"frame": {"duration": 0, "redraw": False},
                                                           "mode": "immediate"}])])]
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TWO DRUG FLOW
# -----------------------------
else:
    drug_A = st.text_input("Drug A Name", value="Acetylcholine")
    drug_B = st.text_input("Drug B Name", value="Atropine")
    
    doses_A = [st.number_input(f"Drug A Dose {i}", min_value=0.0, step=0.1, key=f"da_dose_{i}") for i in range(1,6)]
    doses_B = [st.number_input(f"Drug B Dose {i}", min_value=0.0, step=0.1, key=f"db_dose_{i}") for i in range(1,6)]
    
    interaction = st.selectbox("Type of interaction", ["Competitive Antagonist", "Non-competitive Antagonist", "No Interaction"])
    
    if use_simulation:
        responses_A = simulate_response(doses_A, Max=Max_val, EC50=EC50_val, n=Hill_n)
        responses_B = simulate_response(doses_B, Max=Max_val*0.8, EC50=EC50_val*1.2, n=Hill_n)
        if interaction == "Competitive Antagonist":
            Ki = 2
            responses_A_with_B = responses_A / (1 + np.array(doses_B)/Ki)
        elif interaction == "Non-competitive Antagonist":
            fraction_blocked = 0.4
            responses_A_with_B = responses_A * (1 - fraction_blocked)
        else:
            responses_A_with_B = responses_A
        st.info("Responses auto-generated using virtual lab model")
    else:
        responses_A = [st.number_input(f"Response for Drug A Dose {dose}", min_value=0.0, step=0.5, key=f"da_resp_{i}") for i,dose in enumerate(doses_A)]
        responses_B = [st.number_input(f"Response for Drug B Dose {dose}", min_value=0.0, step=0.5, key=f"db_resp_{i}") for i,dose in enumerate(doses_B)]
        responses_A_with_B = responses_A
    
    if st.button("📊 Generate Dose–Response Curve (Two Drugs)"):
        data_A = pd.DataFrame({"Dose (µg/mL)": doses_A, "Response (mm)": responses_A, "Response with B": responses_A_with_B})
        data_B = pd.DataFrame({"Dose (µg/mL)": doses_B, "Response (mm)": responses_B})
        data_A["Log Dose"] = np.log10(data_A["Dose (µg/mL)"]+1e-6)
        data_B["Log Dose"] = np.log10(data_B["Dose (µg/mL)"]+1e-6)
        st.subheader("Drug A Data")
        st.dataframe(data_A)
        st.subheader("Drug B Data")
        st.dataframe(data_B)
        
        # Animated Plotly for two-drug curves
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', name=f"{drug_A} Alone",
                                 line=dict(color='blue', width=3), marker=dict(size=8),
                                 hovertemplate="Dose: %{x}<br>Response: %{y}<extra></extra>"))
        frames = [go.Frame(data=[
            go.Scatter(x=doses_A[:k+1], y=responses_A[:k+1], name=f"{drug_A} Alone"),
            go.Scatter(x=doses_A[:k+1], y=responses_A_with_B[:k+1], name=f"{drug_A} with {drug_B}"),
            go.Scatter(x=doses_B[:k+1], y=responses_B[:k+1], name=f"{drug_B} Alone")
        ]) for k in range(len(doses_A))]
        fig.frames = frames
        fig.update_layout(
            title="Animated Dose–Response Curves (Two Drugs)",
            xaxis_title="Dose (µg/mL)",
            yaxis_title="Response (mm)",
            updatemenus=[dict(type="buttons",
                              showactive=False,
                              buttons=[dict(label="Play",
                                            method="animate",
                                            args=[None, {"frame": {"duration": 200, "redraw": True},
                                                         "fromcurrent": True}]),
                                       dict(label="Pause",
                                            method="animate",
                                            args=[[None], {"frame": {"duration": 0, "redraw": False},
                                                           "mode": "immediate"}])])]
        )
        st.plotly_chart(fig, use_container_width=True)

