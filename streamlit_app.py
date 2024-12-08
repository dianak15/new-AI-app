from groq import Groq
import matplotlib.pyplot as plt
import streamlit as st
import requests
import googlemaps
import folium 


# Define the FastAPI backend URL
BACKEND_URL = "https://new-ai-app-5.onrender.com/"

# Set your Groq API Key
API_KEY = "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"  # Replace with your actual key

if not API_KEY:
    st.error("API Key is missing. Please provide a valid GROQ_API_KEY.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=API_KEY)




# Global storage for reminders and progress tracking
reminders = []
progress = {"mood": [], "fitness": [], "meditation": [], "hemoglobin": []}

# Streamlit app layout
st.title("AI Health Diagnostic App")
st.markdown("### Enter your details below to get a diagnostic suggestion.")
# User inputs
age = st.number_input("Enter your age:", min_value=0, step=1)
gender = st.radio("Select your gender:", ("Male", "Female"))
#hemoglobin = st.number_input("Enter your hemoglobin level (g/dL):", step=0.1)
symptoms = st.text_area("Describe your symptoms:")



# Function to interact with Gemma2-9b-it model
def query_gemma2(prompt, model="gemma2-9b-it"):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )
    return response.choices[0].message.content
def analyze_health(age, gender, hemoglobin, symptoms):
    prompt = (
        f"Analyze the following health data:\n"
        f"- Age: {age}\n"
        f"- Gender: {gender}\n"
        f"- Hemoglobin level: {hemoglobin} g/dL\n"
        f"- Symptoms: {symptoms}\n\n"
        f"Provide medical insights, considering if the hemoglobin level is normal, low (anemia), or high (e.g., polycythemia). "
        f"Also, relate this to the patient's age, gender, and symptoms, and suggest potential next steps."
    )
    response = query_gemma2(prompt)
    progress["hemoglobin"].append((hemoglobin, response))
    return response
# Hemoglobin tracking function
#def analyze_hemoglobin(user_input):
    #prompt = f"Analyze the hemoglobin level '{user_input} g/dL' and provide medical insights. Indicate if it is normal, low (anemia), or high (potential issues such as polycythemia)."
    #response = query_gemma2(prompt)
    #progress["hemoglobin"].append((user_input, response))
    #return response
    
    
user_input = st.text_input("Enter your hemoglobin level (g/dL):")
#if st.button("Analyze hemoglobin"):
        #if user_input:
            #response = analyze_health(user_input)
            #st.success(f"🤔 Hemoglobin Analysis: {response}")
        #else:
            #st.warning("Please enter your hemoglobin level (g/dL):")

if st.button("Analyze hemoglobin"):
    if user_input:
        try:
            # Call the analyze_health function with all necessary inputs
            response = analyze_health(age, gender, float(user_input), symptoms)
            st.success(f"🤔 Hemoglobin Analysis: {response}")
        except ValueError:
            st.error("Please enter a valid numerical value for hemoglobin.")
    else:
        st.warning("Please enter your hemoglobin level (g/dL).")

# Submit button
if st.button("Get Diagnosis"):
    # Create input payload
    input_data = {
        "age": age,
        "gender": gender,
        "hemoglobin": user_input,
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

            # Call function to get health professionals and map if location is provided
            
        else:
            st.error("Failed to fetch diagnosis. Please try again.")
    except Exception as e:
        st.error(f"Error: {e}")




        # Streamlit UI
    #st.title("🧘‍♀️ AI Wellness Assistant 🧘‍♂️")
    #st.markdown("""
    #Welcome to the **AI Wellness Assistant**! This tool helps you track your mood, generate fitness plans, and enjoy voice-guided meditation.  
    ### Features:
    #- 🌈 **Mood Tracking**  
    #- 🏋️ **Fitness Plans**  
    #- 🧘‍♂️ **Voice-Guided Meditation**  
    #- 🔔 **Set Reminders**  
    #- 📊 **Progress Tracking**
#""")

