import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from PyPDF2 import PdfReader
from fpdf import FPDF

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="MedGuide Pro", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}
.card {
    background-color: #1C1F26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
h1, h2, h3 {
    color: #4A90E2;
}
</style>
""", unsafe_allow_html=True)

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
st.markdown("<h1 style='text-align:center;'>🩺 MedGuide Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI-Powered Medical Intelligence Platform</p>", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.title("User Profile")
age = st.sidebar.number_input("Age", 1, 100)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

symptoms = st.sidebar.multiselect(
    "Symptoms",
    ["Fever", "Cough", "Headache", "Chest Pain", "Fatigue"]
)

# -------------------- PDF UPLOAD --------------------
st.markdown("### 📄 Upload Medical Report")
uploaded_file = st.file_uploader("", type=["pdf"])

report_text = ""
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            report_text += text

    st.success("Report processed successfully!")

# -------------------- ANALYSIS --------------------
def analyze(symptoms):
    input_data = [0,0,0,0,0]
    symptom_list = ["Fever","Cough","Headache","Chest Pain","Fatigue"]

    for i, symptom in enumerate(symptom_list):
        if symptom in symptoms:
            input_data[i] = 1

    return model.predict([input_data])[0]

# -------------------- SESSION STATE --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- MAIN BUTTON --------------------
if st.button("🚀 Run Full Analysis", use_container_width=True):

    if len(symptoms) == 0:
        st.warning("Please select symptoms.")
    else:
        prediction = analyze(symptoms)

        col1, col2, col3 = st.columns(3)

        # SUMMARY CARD
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🧠 Summary")
            st.write(f"Patient ({age}, {gender}) may have **{prediction}**.")
            st.markdown("</div>", unsafe_allow_html=True)

        # RISK CARD
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("⚠️ Risk Level")

            if "Chest Pain" in symptoms:
                risk = "High Risk"
                st.error("Immediate medical attention required!")
            elif len(symptoms) >= 3:
                risk = "Moderate Risk"
                st.warning("Consult doctor soon.")
            else:
                risk = "Low Risk"
                st.success("Low risk. Monitor condition.")

            st.markdown("</div>", unsafe_allow_html=True)

        # SUGGESTIONS CARD
        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("💡 Suggestions")

            suggestions = []
            if prediction == "Flu":
                suggestions.append("Hydration & rest")
            if prediction == "Migraine":
                suggestions.append("Avoid screens & stress")
            if prediction == "Heart Issue":
                suggestions.append("Consult specialist urgently")

            if not suggestions:
                suggestions.append("Medical consultation recommended")

            for s in suggestions:
                st.write("✔️", s)

            st.markdown("</div>", unsafe_allow_html=True)

        # -------------------- REPORT TEXT --------------------
        if report_text:
            st.markdown("### 📑 Extracted Report Insights")
            st.info(report_text[:500] + "...")

        # -------------------- CHAT --------------------
        st.markdown("### 💬 AI Assistant")

        user_input = st.text_input("Ask follow-up question")

        if user_input:
            response = f"Based on {prediction}, maintain care and consult a doctor if symptoms worsen."
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", response))

        for role, msg in st.session_state.chat_history:
            if role == "You":
                st.write(f"🧑 {msg}")
            else:
                st.write(f"🤖 {msg}")

        # -------------------- PDF --------------------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="MedGuide Pro Report", ln=True)
        pdf.cell(200, 10, txt=f"Age: {age} | Gender: {gender}", ln=True)
        pdf.cell(200, 10, txt=f"Condition: {prediction}", ln=True)
        pdf.cell(200, 10, txt=f"Risk: {risk}", ln=True)

        pdf.cell(200, 10, txt="Suggestions:", ln=True)
        for s in suggestions:
            pdf.cell(200, 10, txt=f"- {s}", ln=True)

        pdf.output("report.pdf")

        with open("report.pdf", "rb") as f:
            st.download_button("📥 Download Full Report", f, file_name="MedGuide_Report.pdf")

# -------------------- FOOTER --------------------
st.markdown("---")
st.warning("⚠️ Not a medical diagnosis. Always consult a professional.")
