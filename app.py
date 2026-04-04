import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from PyPDF2 import PdfReader
from fpdf import FPDF

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="MedGuide Pro", layout="wide")

# -------------------- CSS --------------------
st.markdown("""
<style>
body {background-color: #0E1117; color: white;}
.card {
    background-color: #1C1F26;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("<h1 style='text-align:center;'>🩺 MedGuide Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI Health Intelligence System</p>", unsafe_allow_html=True)

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

# -------------------- SIDEBAR --------------------
st.sidebar.title("User Profile")

age = st.sidebar.number_input("Age", 1, 100)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

symptoms = st.sidebar.multiselect(
    "Symptoms",
    ["Fever", "Cough", "Headache", "Chest Pain", "Fatigue"]
)

# -------------------- PDF UPLOAD --------------------
st.subheader("📄 Upload Medical Report")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

report_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            report_text += text.lower()

    st.success("Report uploaded successfully!")

# -------------------- ANALYSIS FUNCTION --------------------
def analyze(symptoms):
    input_data = [0,0,0,0,0]
    symptom_list = ["Fever","Cough","Headache","Chest Pain","Fatigue"]

    for i, symptom in enumerate(symptom_list):
        if symptom in symptoms:
            input_data[i] = 1

    return model.predict([input_data])[0]

# -------------------- HEALTH SCORE --------------------
def calculate_score(symptoms):
    return max(100 - (len(symptoms) * 20), 10)

# -------------------- SESSION --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- MAIN --------------------
tabs = st.tabs(["📊 Analysis", "📄 Report Insights", "💬 AI Chat"])

# -------------------- ANALYSIS TAB --------------------
with tabs[0]:

    if st.button("🚀 Run Analysis", use_container_width=True):

        if len(symptoms) == 0:
            st.warning("Please select symptoms")
        else:
            prediction = analyze(symptoms)

            score = calculate_score(symptoms)

            st.subheader("🧠 Health Score")
            st.progress(score)
            st.write(f"Health Score: {score}/100")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("Summary")
                st.write(f"Condition: {prediction}")
                st.write(f"Age: {age}, Gender: {gender}")
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("Risk Level")

                if "Chest Pain" in symptoms:
                    risk = "High"
                    st.error("High Risk 🚨")
                elif len(symptoms) >= 3:
                    risk = "Moderate"
                    st.warning("Moderate Risk ⚠️")
                else:
                    risk = "Low"
                    st.success("Low Risk ✅")

                st.markdown("</div>", unsafe_allow_html=True)

            with col3:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("Suggestions")

                suggestions = []
                if prediction == "Flu":
                    suggestions.append("Drink fluids & rest")
                if prediction == "Migraine":
                    suggestions.append("Avoid screens")
                if prediction == "Heart Issue":
                    suggestions.append("Consult doctor urgently")

                if not suggestions:
                    suggestions.append("Consult doctor")

                for s in suggestions:
                    st.write("✔️", s)

                st.markdown("</div>", unsafe_allow_html=True)

            st.session_state.prediction = prediction
            st.session_state.risk = risk
            st.session_state.suggestions = suggestions
            st.session_state.score = score

# -------------------- REPORT TAB --------------------
with tabs[1]:

    st.subheader("📑 Report Insights")

    if report_text:
        insights = []

        if "cholesterol" in report_text:
            insights.append("Cholesterol detected ⚠️")
        if "bp" in report_text or "blood pressure" in report_text:
            insights.append("Blood Pressure info found")
        if "sugar" in report_text:
            insights.append("Blood Sugar mentioned")

        if insights:
            for i in insights:
                st.info(i)
        else:
            st.write("No major markers detected")

        st.text_area("Extracted Text", report_text[:800])

    else:
        st.write("Upload a report to see insights")

# -------------------- CHAT TAB --------------------
with tabs[2]:

    st.subheader("💬 AI Assistant")

    user_input = st.text_input("Ask your question")

    if user_input:
        if "prediction" in st.session_state:
            response = f"Based on your condition ({st.session_state.prediction}), monitor symptoms and consult doctor if needed."
        else:
            response = "Please run analysis first."

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI", response))

    for role, msg in st.session_state.chat_history:
        if role == "You":
            st.write(f"🧑 {msg}")
        else:
            st.write(f"🤖 {msg}")

# -------------------- DOWNLOAD PDF --------------------
if "prediction" in st.session_state:

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="MedGuide Pro Report", ln=True)
    pdf.cell(200, 10, txt=f"Condition: {st.session_state.prediction}", ln=True)
    pdf.cell(200, 10, txt=f"Risk: {st.session_state.risk}", ln=True)
    pdf.cell(200, 10, txt=f"Health Score: {st.session_state.score}", ln=True)

    pdf.cell(200, 10, txt="Suggestions:", ln=True)
    for s in st.session_state.suggestions:
        pdf.cell(200, 10, txt=f"- {s}", ln=True)

    pdf.output("report.pdf")

    with open("report.pdf", "rb") as f:
        st.download_button("📥 Download Full Report", f, file_name="MedGuide_Report.pdf")

# -------------------- FOOTER --------------------
st.markdown("---")
st.warning("⚠️ This is not a medical diagnosis. Consult a doctor.")
