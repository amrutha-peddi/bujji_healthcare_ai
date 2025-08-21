

````markdown
# 🏥 Healthcare AI Diagnosis Assistant

A **Flask-based web application** that helps users understand potential medical conditions based on the symptoms they enter.  
It provides **professional advice**, generates **AI-powered summaries**, supports **voice narration**, and allows **PDF downloads** of the diagnosis report.

---

## 🔧 Features

### 1. Symptom Analysis
- Users enter symptoms in a text box.  
- The app scans a predefined **symptom–disease mapping**.  
- Provides:
  - Probable diagnosis  
  - Medical advice  
  - Severity level  

### 2. AI Summarization
- Powered by Hugging Face’s [`facebook/bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn) model.  
- Uses the `transformers` library to generate a **concise summary** from the detailed diagnostic output.  

### 3. Voice Narration
- Integrated with **`pyttsx3`** for text-to-speech.  
- Reads out the AI-generated summary.  
- Works offline and supports most OS voice engines.  

### 4. PDF Report Generation
- Generates a **downloadable PDF** report of the summary using the `fpdf` library.  
- Useful for sharing or storing medical history.  

## 5. Web Interface
- Clean, responsive, and **chatbot-style UI**.  
- Features:
  - Symptom autocomplete  
  - Result cards with diagnosis & advice  
  - Action buttons to **download PDF** or **listen to narration**  

---

## 🧠 How It Works (Internal Flow)

```mermaid
flowchart TD
    A[User Input Symptoms] --> B[Match in SYMPTOM_MAP]
    B --> C[Probable Diagnosis + Advice]
    C --> D[AI Summarization with Transformers]
    D --> E[Voice Narration via pyttsx3]
    D --> F[PDF Report via fpdf]
    E & F --> G[Result Page - index.html]
````

---

## 🖥️ How to Run Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/amrutha-peddi/bujji_healthcare_ai.git
   cd healthcare-ai-assistant
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**

   ```bash
   python app.py
   ```

5. **Open in browser**

   ```
   http://127.0.0.1:5000/
   ```

---

## 📂 Project Structure

```
healthcare-ai-assistant/
│── app.py                # Main Flask application
│── templates/
│   └── index.html        # Web interface (chatbot-style UI)
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
│── how_it_works.txt      # Application Working Documentation



```

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**.
It is **not a replacement for professional medical advice**.
Always consult a certified doctor for accurate medical guidance.

---

## ✨ Future Enhancements

* Expand the **symptom database** with real-world datasets.
* Support for **multilingual diagnosis and narration**.
* Integration with **cloud-hosted AI models** for faster responses.
* Add **user authentication** and **medical history tracking**.

---
