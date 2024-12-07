import streamlit as st
import requests

# Define the FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000/diagnose"

# Streamlit app layout
st.title("AI Health Diagnostic App")
st.markdown("### Enter your details below to get a diagnostic suggestion.")

# User inputs
age = st.number_input("Enter your age:", min_value=0, step=1)
gender = st.radio("Select your gender:", ("Male", "Female"))
hemoglobin = st.number_input("Enter your hemoglobin level (g/dL):", step=0.1)
symptoms = st.text_area("Describe your symptoms:")

# Submit button
if st.button("Get Diagnosis"):
    # Create input payload
    input_data = {
        "age": age,
        "gender": gender,
        "hemoglobin": hemoglobin,
        "symptoms": symptoms
    }

    # Send request to FastAPI backend
    try:
        response = requests.post(f"{BACKEND_URL}", json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success("Diagnosis:")
            for diag in result["diagnosis"]:
                st.write(f"- {diag}")
            st.info(result["recommendation"])
        else:
            st.error("Failed to fetch diagnosis. Please try again.")
    except Exception as e:
        st.error(f"Error: {e}")

