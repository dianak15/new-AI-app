
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI
app = FastAPI()

# Define schema for health inputs
class HealthInput(BaseModel):
    age: int
    gender: str
    hemoglobin: float
    symptoms: str  # Free-text symptoms description

# Load a Hugging Face model (e.g., text classification for symptom analysis)
model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Diagnostic App!"}

@app.post("/diagnose")
def diagnose(input: HealthInput):
    # Analyze hemoglobin levels
    diagnosis = []
    if input.gender.lower() == "female" and input.hemoglobin < 12.0:
        diagnosis.append("Anemia")
    elif input.gender.lower() == "male" and input.hemoglobin < 13.5:
        diagnosis.append("Anemia")
    elif input.gender.lower() == "female" and input.hemoglobin > 16.0:
        diagnosis.append("Polycythemia")
    elif input.gender.lower() == "male" and input.hemoglobin > 16.5:
        diagnosis.append("Polycythemia")

    # Use Hugging Face model for symptom analysis
    symptom_analysis = model(input.symptoms)
    diagnosis.append(f"Symptom Analysis: {symptom_analysis[0]['label']} with confidence {symptom_analysis[0]['score']:.2f}")

    # Return results
    return {
        "diagnosis": diagnosis,
        "recommendation": "This is not a substitute for medical advice. Consult a healthcare professional."
    }

# Run the backend
# Use `uvicorn app:app --reload` to start the backend server
 
