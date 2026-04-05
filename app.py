import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from PyPDF2 import PdfReader
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="MedGuide Pro", layout="wide")

# ---------------- SESSION ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- AUTH ----------------
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

# ---------------- NAVBAR ----------------
col1, col2, col3 = st.columns([6,2,2])

with col1:
    st.markdown("## 🩺 MedGuide Pro")

with col2:
    st.write("")

with col3:
    if st.session_state.logged_in:
        st.write(f"👤 {st.session_state.current_user}")
        if st.button("Logout"):
            logout()
    else:
        with st.popover("Login / Signup"):
            auth = st.radio("", ["Login", "Sign Up"])
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")

            if auth == "Sign Up":
                if st.button("Create Account"):
                    if signup(user, pwd):
                        st.success("Account created")
                    else:
                        st.error("User exists")

            if auth == "Login":
                if st.button("Login"):
                    if login(user, pwd):
                        st.success("Logged in")
                    else:
                        st.error("Invalid login")

# ---------------- HERO ----------------
st.markdown("""
<div style='background: linear-gradient(90deg,#4A90E2,#6FC3FF);
padding:40px;border-radius:15px;color:white'>
<h1>AI Health Intelligence Platform</h1>
<p>Analyze symptoms, upload reports, and get instant medical insights</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- FEATURE CARDS ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966485.png", width=90)
    st.subheader("Report Analysis")
    st.caption("Upload reports and extract insights")

with c2:
    st.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=90)
    st.subheader("AI Diagnosis")
    st.caption("Predict conditions intelligently")

with c3:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=90)
    st.subheader("Health Monitoring")
    st.caption("Track risk and health score")

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

# ---------------- PDF ----------------
st.subheader("📄 Upload Medical Report")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

report_text = ""
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            report_text += txt.lower()

    st.success("Report uploaded")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📊 Analysis", "📄 Report", "💬 Chat"])

# ---------------- ANALYSIS ----------------
with tab1:

    if st.button("🚀 Run Analysis", use_container_width=True):

        if len(symptoms) == 0:
            st.warning("Select symptoms")
        else:
            input_data = [1 if s in symptoms else 0 for s in ["Fever","Cough","Headache","Chest Pain","Fatigue"]]
            prediction = model.predict([input_data])[0]

            score = max(100 - len(symptoms)*20, 10)

            st.subheader("Health Score")
            st.progress(score)
            st.write(f"{score}/100")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Summary")
                st.write(f"Condition: {prediction}")

            with col2:
                st.subheader("Risk")
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
                st.subheader("Suggestions")
                st.write("✔️ Rest & hydrate")
                st.write("✔️ Monitor symptoms")

            st.session_state.prediction = prediction
            st.session_state.risk = risk
            st.session_state.score = score

# ---------------- REPORT ----------------
with tab2:
    if report_text:
        st.subheader("Report Insights")

        if "cholesterol" in report_text:
            st.warning("Cholesterol detected")
        if "bp" in report_text:
            st.info("Blood Pressure found")
        if "sugar" in report_text:
            st.warning("Sugar levels mentioned")

        st.text_area("Extracted Text", report_text[:800])
    else:
        st.write("Upload report first")

# ---------------- CHAT ----------------
with tab3:

    user_input = st.text_input("Ask anything")

    if user_input:
        if "prediction" in st.session_state:
            reply = f"Based on {st.session_state.prediction}, monitor symptoms and consult doctor."
        else:
            reply = "Run analysis first."

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI", reply))

    for role, msg in st.session_state.chat_history:
        if role == "You":
            st.write(f"🧑 {msg}")
        else:
            st.write(f"🤖 {msg}")

# ---------------- PDF DOWNLOAD ----------------
if "prediction" in st.session_state:

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="MedGuide Pro Report", ln=True)
    pdf.cell(200, 10, txt=f"Condition: {st.session_state.prediction}", ln=True)
    pdf.cell(200, 10, txt=f"Risk: {st.session_state.risk}", ln=True)
    pdf.cell(200, 10, txt=f"Score: {st.session_state.score}", ln=True)

    pdf.output("report.pdf")

    with open("report.pdf", "rb") as f:
        st.download_button("📥 Download Report", f)

# ---------------- FOOTER ----------------
st.markdown("---")
st.warning("⚠️ This is not a real medical diagnosis.")
