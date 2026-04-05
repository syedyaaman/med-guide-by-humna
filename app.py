import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from PyPDF2 import PdfReader
from fpdf import FPDF

st.set_page_config(layout="wide")

# ---------------- SESSION ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# ---------------- AUTH FUNCTIONS ----------------
def signup(username, password):
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = password
    return True

def login(username, password):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = ""

# ---------------- HEADER ----------------
col1, col2 = st.columns([3,1])

with col1:
    st.markdown("<h2 style='color:#1f4e79;'>🩺 MedGuide Pro</h2>", unsafe_allow_html=True)

with col2:
    if st.session_state.logged_in:
        st.write(f"👤 {st.session_state.current_user}")
        if st.button("Logout"):
            logout()
    else:
        with st.expander("Login / Sign Up"):
            auth_option = st.selectbox("Choose", ["Login", "Sign Up"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if auth_option == "Sign Up":
                if st.button("Create Account"):
                    if signup(username, password):
                        st.success("Account created!")
                    else:
                        st.error("User exists")

            if auth_option == "Login":
                if st.button("Login"):
                    if login(username, password):
                        st.success("Logged in!")
                    else:
                        st.error("Invalid credentials")

# ---------------- HERO SECTION ----------------
st.markdown("""
<div style='background-color:#e6f0ff;padding:30px;border-radius:15px'>
<h1>AI Health Assistant</h1>
<p>Analyze reports, detect risks, and get smart suggestions instantly</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- FEATURE CARDS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966485.png", width=100)
    st.subheader("Upload Report")
    st.write("Analyze your medical reports instantly")

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=100)
    st.subheader("AI Diagnosis")
    st.write("Smart prediction using AI")

with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100)
    st.subheader("Health Insights")
    st.write("Get risk levels and suggestions")

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("User Profile")

age = st.sidebar.number_input("Age", 1, 100)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

symptoms = st.sidebar.multiselect(
    "Symptoms",
    ["Fever", "Cough", "Headache", "Chest Pain", "Fatigue"]
)

# ---------------- MODEL ----------------
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

# ---------------- PDF UPLOAD ----------------
st.subheader("📄 Upload Medical Report")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

report_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            report_text += text.lower()

    st.success("Report uploaded!")

# ---------------- ANALYSIS ----------------
if st.button("🚀 Run Analysis", use_container_width=True):

    if len(symptoms) == 0:
        st.warning("Select symptoms first")
    else:
        input_data = [1 if s in symptoms else 0 for s in ["Fever","Cough","Headache","Chest Pain","Fatigue"]]
        prediction = model.predict([input_data])[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🧠 Summary")
            st.write(f"Condition: {prediction}")
            st.write(f"Age: {age}, Gender: {gender}")

        with col2:
            st.subheader("⚠️ Risk")
            if "Chest Pain" in symptoms:
                risk = "High"
                st.error("High Risk 🚨")
            elif len(symptoms) >= 3:
                risk = "Moderate"
                st.warning("Moderate Risk")
            else:
                risk = "Low"
                st.success("Low Risk")

        with col3:
            st.subheader("💡 Suggestions")
            suggestions = ["Consult doctor if symptoms persist"]
            for s in suggestions:
                st.write("✔️", s)

        # ---------------- REPORT TEXT ----------------
        if report_text:
            st.subheader("📑 Report Insights")
            st.text_area("Extracted Text", report_text[:500])

        # ---------------- PDF ----------------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="MedGuide Report", ln=True)
        pdf.cell(200, 10, txt=f"Condition: {prediction}", ln=True)
        pdf.cell(200, 10, txt=f"Risk: {risk}", ln=True)

        pdf.output("report.pdf")

        with open("report.pdf", "rb") as f:
            st.download_button("📥 Download Report", f)

st.markdown("---")
st.warning("⚠️ Not a medical diagnosis. Consult a doctor.")
