from flask import Flask, render_template, request, jsonify, send_file
from transformers import pipeline
from datetime import datetime
import pyttsx3
from io import BytesIO
from fpdf import FPDF

app = Flask(__name__)

# Load summarization pipeline from Hugging Face (no local model files)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Convert summary to speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Generate PDF
def generate_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary_text)
    byte_io = BytesIO()
    pdf.output(byte_io)
    byte_io.seek(0)
    return byte_io

SYMPTOM_MAP = {
    "fever": {
        "diagnosis": "You may have a viral infection such as the flu, dengue, or COVID-19.",
        "advice": "Monitor temperature, take paracetamol if needed, and consult a doctor if it persists.",
        "severity": "Moderate"
    },
    "cough": {
        "diagnosis": "Could be bronchitis, cold, or COVID-19.",
        "advice": "Drink warm fluids, consider steam inhalation, and consult a physician.",
        "severity": "Mild to Moderate"
    },
    "headache": {
        "diagnosis": "Possibly migraine, dehydration, or stress-related.",
        "advice": "Stay hydrated, rest in a quiet dark room, and consider mild painkillers.",
        "severity": "Mild"
    },
    "nausea": {
        "diagnosis": "May indicate food poisoning or stomach infection.",
        "advice": "Drink ORS, avoid solid foods temporarily, consult if persistent.",
        "severity": "Mild"
    },
    "chest pain": {
        "diagnosis": "Critical symptom—could be related to the heart or lungs.",
        "advice": "Seek emergency medical help immediately.",
        "severity": "High"
    },
    "sore throat": {
        "diagnosis": "Likely viral or bacterial infection such as strep throat.",
        "advice": "Use saltwater gargles, warm fluids; consult if it worsens.",
        "severity": "Mild to Moderate"
    },
    "fatigue": {
        "diagnosis": "Could be due to anemia, poor sleep, or thyroid issues.",
        "advice": "Check iron levels, rest well, and consider a health checkup.",
        "severity": "Mild"
    },
    "shortness of breath": {
        "diagnosis": "Serious symptom. Could be asthma, pneumonia, or cardiac issue.",
        "advice": "Seek immediate medical attention.",
        "severity": "High"
    },
    "vomiting": {
        "diagnosis": "May indicate food poisoning, gastritis, or motion sickness.",
        "advice": "Hydrate well and avoid solid food temporarily.",
        "severity": "Moderate"
    },
    "diarrhea": {
        "diagnosis": "Often due to infection or contaminated food.",
        "advice": "Stay hydrated, take ORS, and consult if persistent.",
        "severity": "Moderate"
    },
    "dizziness": {
        "diagnosis": "Could be due to low blood pressure, dehydration, or inner ear issues.",
        "advice": "Sit or lie down, hydrate, and monitor.",
        "severity": "Mild to Moderate"
    },
    "rash": {
        "diagnosis": "May be allergic reaction, eczema, or viral infection.",
        "advice": "Avoid irritants and consult dermatologist.",
        "severity": "Mild"
    },
    "itching": {
        "diagnosis": "Could be due to allergies, infections, or dry skin.",
        "advice": "Apply moisturizer, avoid allergens.",
        "severity": "Mild"
    },
    "joint pain": {
        "diagnosis": "May be arthritis, viral infection, or injury.",
        "advice": "Rest, use ice packs, consult orthopedist if it persists.",
        "severity": "Moderate"
    },
    "swelling": {
        "diagnosis": "May indicate inflammation or fluid retention.",
        "advice": "Elevate limb and apply cold compress.",
        "severity": "Moderate"
    },
    "weight loss": {
        "diagnosis": "Unintentional weight loss could be due to thyroid, diabetes, or cancer.",
        "advice": "Seek medical evaluation immediately.",
        "severity": "High"
    },
    "weight gain": {
        "diagnosis": "Could be due to thyroid issues, lifestyle, or fluid retention.",
        "advice": "Monitor diet and activity, consult if unexplained.",
        "severity": "Mild"
    },
    "blurred vision": {
        "diagnosis": "May indicate diabetes, eye strain, or neurological issue.",
        "advice": "Consult an ophthalmologist.",
        "severity": "Moderate"
    },
    "frequent urination": {
        "diagnosis": "Could be a sign of diabetes or UTI.",
        "advice": "Drink water, consider sugar and urine tests.",
        "severity": "Moderate"
    },
    "burning urination": {
        "diagnosis": "Commonly indicates a urinary tract infection.",
        "advice": "Increase fluid intake, consult doctor for antibiotics.",
        "severity": "Moderate"
    },
    "back pain": {
        "diagnosis": "May be due to posture, injury, or kidney problems.",
        "advice": "Rest, apply heat, consider physiotherapy.",
        "severity": "Moderate"
    },
    "abdominal pain": {
        "diagnosis": "Could be gas, appendicitis, or ulcer.",
        "advice": "Monitor intensity and location, seek medical help.",
        "severity": "Moderate to High"
    },
    "constipation": {
        "diagnosis": "Common due to low fiber diet or dehydration.",
        "advice": "Increase fiber intake, drink water.",
        "severity": "Mild"
    },
    "cold hands": {
        "diagnosis": "Could be circulatory issue or anemia.",
        "advice": "Warm up and check iron levels.",
        "severity": "Mild"
    },
    "palpitations": {
        "diagnosis": "May indicate stress, arrhythmia, or thyroid issue.",
        "advice": "Relax and consult cardiologist.",
        "severity": "Moderate to High"
    },
    "memory loss": {
        "diagnosis": "Could be stress, aging, or neurological issue.",
        "advice": "Monitor and consult neurologist.",
        "severity": "Moderate"
    },
    "depression": {
        "diagnosis": "Mental health condition requiring attention.",
        "advice": "Talk to a counselor or psychiatrist.",
        "severity": "Moderate"
    },
    "anxiety": {
        "diagnosis": "May affect daily life and sleep.",
        "advice": "Practice relaxation and seek counseling.",
        "severity": "Mild to Moderate"
    },
    "insomnia": {
        "diagnosis": "Difficulty sleeping may indicate stress or medical condition.",
        "advice": "Follow sleep hygiene and consult doctor.",
        "severity": "Moderate"
    },
    "night sweats": {
        "diagnosis": "Could be due to TB, hormone imbalance.",
        "advice": "Check for infections or consult doctor.",
        "severity": "Moderate"
    },
    "hair loss": {
        "diagnosis": "May be due to stress, genetics, or nutrition.",
        "advice": "Consider dermatologist or nutritionist.",
        "severity": "Mild"
    },
    "snoring": {
        "diagnosis": "May be harmless or indicate sleep apnea.",
        "advice": "Evaluate sleeping posture, consult ENT.",
        "severity": "Mild"
    },
    "nosebleed": {
        "diagnosis": "Could be dryness or high blood pressure.",
        "advice": "Apply pressure, humidify air.",
        "severity": "Mild"
    },
    "ear pain": {
        "diagnosis": "May indicate ear infection or wax build-up.",
        "advice": "Consult ENT specialist.",
        "severity": "Mild to Moderate"
    },
    "tremors": {
        "diagnosis": "Could be Parkinson’s, stress, or caffeine.",
        "advice": "Monitor frequency, consult neurologist.",
        "severity": "Moderate"
    },
    "dry mouth": {
        "diagnosis": "Often due to dehydration or medication side-effects.",
        "advice": "Drink water, check medications.",
        "severity": "Mild"
    },
    "sensitivity to light": {
        "diagnosis": "Could indicate migraine or eye infection.",
        "advice": "Rest in dark room, use sunglasses.",
        "severity": "Mild"
    },
    "muscle cramps": {
        "diagnosis": "May result from dehydration or overexertion.",
        "advice": "Stretch and hydrate.",
        "severity": "Mild"
    },
    "difficulty swallowing": {
        "diagnosis": "Could be infection or esophageal disorder.",
        "advice": "Seek ENT evaluation.",
        "severity": "Moderate"
    },
    "loss of appetite": {
        "diagnosis": "May signal infection, depression, or digestive issue.",
        "advice": "Monitor and seek dietary support.",
        "severity": "Moderate"
    },
    "red eyes": {
        "diagnosis": "Could be conjunctivitis or allergy.",
        "advice": "Use eye drops and consult if worsening.",
        "severity": "Mild"
    },
    "difficulty concentrating": {
        "diagnosis": "May result from anxiety, ADHD, or fatigue.",
        "advice": "Limit distractions, consult doctor.",
        "severity": "Moderate"
    },
    "irregular periods": {
        "diagnosis": "Could be PCOS, stress, or hormonal imbalance.",
        "advice": "Consult gynecologist.",
        "severity": "Moderate"
    },
    "yellow skin": {
        "diagnosis": "Likely jaundice. Could indicate liver issues.",
        "advice": "Consult physician immediately.",
        "severity": "High"
    },
    "cold feet": {
        "diagnosis": "Often due to poor circulation or diabetes.",
        "advice": "Keep warm and consult if numb.",
        "severity": "Mild"
    }
}
def diagnose(symptoms):
    symptoms = symptoms.lower()
    found = []

    for keyword, info in SYMPTOM_MAP.items():
        if keyword in symptoms:
            found.append({
                "symptom": keyword,
                "diagnosis": info["diagnosis"],
                "advice": info["advice"],
                "severity": info["severity"]
            })

    if not found:
        return [{
            "symptom": "Unknown",
            "diagnosis": "No specific diagnosis found.",
            "advice": "Please consult a healthcare professional.",
            "severity": "Unknown"
        }]

    return found

@app.route('/')
def home():
    symptom_keys = list(SYMPTOM_MAP.keys())
    return render_template('index.html', result=None, summary=None, symptom_keys=symptom_keys)

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.form.get('symptoms', '')
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] User input: {symptoms}")

    results = diagnose(symptoms)
    summary_input = " ".join([f"{item['symptom']} causes {item['diagnosis']}. Advice: {item['advice']}." for item in results])
    summary = summarizer(summary_input, max_length=100, min_length=30, do_sample=False)[0]['summary_text']

    # Optional: Speak out summary
    speak_text(summary)

    # Store summary in session for PDF export
    symptom_keys = list(SYMPTOM_MAP.keys())
    return render_template('index.html', result=results, summary=summary, symptom_keys=symptom_keys)

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    summary_text = request.form.get('summary', '')
    pdf_file = generate_pdf(summary_text)
    return send_file(pdf_file, download_name="diagnosis_summary.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)