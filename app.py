import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from PyPDF2 import PdfReader
from fpdf import FPDF

# -------------------- MODEL --------------------
data = {
    "Fever": [1,1,0,0,1,0],
    "Cough": [1,1,0,0,0,1],
    "Headache": [1,0,1,0,1,1],
    "Chest Pain": [0,0,1,1,0,1],
    "Fatigue": [1,1,1,0,1,1],
    "Disease": ["Flu","Cold","Migraine","Heart Issue","Viral Infection","Infection"]
}

df = pd.DataFrame(data)
X = df.drop("Disease", axis=1)
y = df["Disease"]

model = DecisionTreeClassifier()
model.fit(X, y)

# -------------------- HEADER --------------------
st.markdown("""
<h1 style='text-align: center; color: #4A90E2;'>🩺 MedGuide Pro</h1>
<p style='text-align: center;'>AI Medical Assistant</p>
""", unsafe_allow_html=True)

# -------------------- USER INPUT --------------------
st.sidebar.header("User Info")

age = st.sidebar.number_input("Age", 1, 100)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

symptoms = st.multiselect(
    "Select your symptoms",
    ["Fever", "Cough", "Headache", "Chest Pain", "Fatigue"]
)

# -------------------- PDF UPLOAD --------------------
st.subheader("📄 Upload Medical Report (Optional)")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

report_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        report_text += page.extract_text()

    st.success("Report uploaded successfully!")

# -------------------- PREDICTION --------------------
def analyze(symptoms):
    input_data = [0,0,0,0,0]
    symptom_list = ["Fever","Cough","Headache","Chest Pain","Fatigue"]

    for i, symptom in enumerate(symptom_list):
        if symptom in symptoms:
            input_data[i] = 1

    return model.predict([input_data])[0]

# -------------------- GENERATE RESULT --------------------
if st.button("Get Full Analysis"):

    if len(symptoms) == 0:
        st.warning("Please select at least one symptom.")
    else:
        prediction = analyze(symptoms)

        st.subheader("🧠 Summary")
        summary = f"""
        Based on your symptoms and profile ({age}, {gender}),
        the system suggests a possible condition: {prediction}.
        """
        st.write(summary)

        st.subheader("⚠️ Risk Level")
        if "Chest Pain" in symptoms:
            risk = "High Risk"
            st.error("🚨 Seek immediate medical attention!")
        elif len(symptoms) >= 3:
            risk = "Moderate Risk"
            st.warning("Visit a doctor soon.")
        else:
            risk = "Low Risk"
            st.success("Rest and monitor symptoms.")

        st.subheader("💡 Suggestions")
        suggestions = []
        if prediction == "Flu":
            suggestions.append("Rest and stay hydrated")
        if prediction == "Migraine":
            suggestions.append("Avoid bright lights & take rest")
        if prediction == "Heart Issue":
            suggestions.append("Consult cardiologist immediately")

        if not suggestions:
            suggestions.append("Consult a doctor if symptoms persist")

        for s in suggestions:
            st.write("✔️", s)

        # -------------------- CHAT --------------------
        st.subheader("💬 Follow-up Chat")

        user_question = st.text_input("Ask anything about your condition:")

        if user_question:
            response = f"Based on {prediction}, it's advised to monitor your condition and consult a doctor if needed."
            st.write("🤖:", response)

        # -------------------- PDF GENERATION --------------------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Medical Report", ln=True)

        pdf.cell(200, 10, txt=f"Age: {age} | Gender: {gender}", ln=True)
        pdf.cell(200, 10, txt=f"Condition: {prediction}", ln=True)
        pdf.cell(200, 10, txt=f"Risk: {risk}", ln=True)

        pdf.cell(200, 10, txt="Suggestions:", ln=True)
        for s in suggestions:
            pdf.cell(200, 10, txt=f"- {s}", ln=True)

        file_path = "report.pdf"
        pdf.output(file_path)

        with open(file_path, "rb") as f:
            st.download_button("📥 Download Report", f, file_name="medical_report.pdf")

# -------------------- FOOTER --------------------
st.warning("⚠️ This is not a real medical diagnosis. Consult a doctor.")
