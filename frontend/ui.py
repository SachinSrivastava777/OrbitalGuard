import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="OrbitalGuard Telemetry Console", layout="wide")

st.title("Space Debris Tracking & Collision Risk Engine")
st.markdown("---")

st.sidebar.header("Live Satellite Telemetry Inputs")

semi_major_axis = st.sidebar.slider("Semi-Major Axis (km)", 6500, 42000, 7000)
eccentricity = st.sidebar.slider("Eccentricity (Orbit shape)", 0.0, 0.1, 0.01, step=0.001)
inclination = st.sidebar.slider("Inclination Angle (degrees)", 0.0, 90.0, 51.6)
relative_distance = st.sidebar.slider("Relative Conjunction Distance (km)", 0.1, 50.0, 15.0, step=0.1)
relative_velocity = st.sidebar.slider("Relative Closing Velocity (km/s)", 0.5, 16.0, 7.5, step=0.1)

st.subheader("Real-Time Simulation Analytics")
col1, col2 = st.columns([2, 1])

with col1:
    payload = {
        "semi_major_axis": float(semi_major_axis),
        "eccentricity": float(eccentricity),
        "inclination": float(inclination),
        "relative_distance": float(relative_distance),
        "relative_velocity": float(relative_velocity)
    }
    
    if st.button("Analyze Collision Vectors", use_container_width=True):
        try:
            response = requests.post(f"{BACKEND_URL}/predict-risk", json=payload)
            if response.status_code == 200:
                result = response.json()
                risk = result["collision_risk_class"]
                
                if risk == "SAFE":
                    st.success(f"STATUS: {risk} ({result['confidence_score']}% confidence)")
                elif risk == "WARNING":
                    st.warning(f"STATUS: {risk} ({result['confidence_score']}% confidence)")
                else:
                    st.error(f"STATUS: {risk} ({result['confidence_score']}% confidence)")
                
                st.write(f"**Mission Control Guidance:** {result['recommended_action']}")
                st.markdown("#### Probability Vector Matrix:")
                st.json(result["probabilities"])
            else:
                st.error(f"Backend API Error: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to Backend Microservice: {str(e)}")

with col2:
    st.markdown("### Operational Constraints")
    st.metric(label="Simulated Orbit Environment", value="LEO" if semi_major_axis < 10000 else "GEO/MEO")
    st.metric(label="Kinetic Energy Factor (Relative)", value=f"{round(relative_velocity ** 2, 2)} MJ/kg")