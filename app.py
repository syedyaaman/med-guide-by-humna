import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="HealthCare App", layout="wide")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.navbar {
    background-color: #0B3C6D;
    padding: 14px;
    border-radius: 10px;
    color: white;
    font-size: 20px;
}
.search-box input {
    border-radius: 20px !important;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #F5F7FA;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}
.hero {
    background-color: #2E6EB5;
    padding: 40px;
    border-radius: 20px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2, col3 = st.columns([2,5,2])

with col1:
    st.markdown("<div class='navbar'><b>HealthCare+</b></div>", unsafe_allow_html=True)

with col2:
    st.text_input("Search medicines, services...", key="search")

with col3:
    if st.session_state.logged_in:
        st.success("Logged In")
        if st.button("Logout"):
            st.session_state.logged_in = False
    else:
        if st.button("Sign In"):
            st.session_state.page = "login"

# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":
    st.title("🔐 Sign In")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.success("Login Successful!")
        else:
            st.error("Invalid Credentials")

    st.stop()

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class='hero'>
<h1>Tired of Waiting at Hospital?</h1>
<p>Book services instantly from your home</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- SERVICES ----------------
st.subheader("Our Services")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966483.png")
    if st.button("Pharmacy"):
        st.session_state.page = "pharmacy"

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png")
    if st.button("Doctor"):
        st.session_state.page = "doctor"

with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/4320/4320371.png")
    if st.button("Home Care"):
        st.session_state.page = "homecare"

with col4:
    st.image("https://cdn-icons-png.flaticon.com/512/2785/2785819.png")
    if st.button("Lab Tests"):
        st.session_state.page = "lab"

st.write("---")

# ---------------- FEATURE PAGES ----------------

# 🏥 PHARMACY
if st.session_state.page == "pharmacy":
    st.title("💊 Pharmacy")

    uploaded_file = st.file_uploader("Upload Prescription", type=["pdf", "jpg", "png"])

    if uploaded_file:
        st.success("Prescription uploaded successfully!")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# 👨‍⚕️ DOCTOR
elif st.session_state.page == "doctor":
    st.title("👨‍⚕️ Doctor Consultation")

    name = st.text_input("Enter your name")
    issue = st.text_area("Describe your issue")

    if st.button("Book Appointment"):
        st.success("Appointment booked!")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# 🏠 HOME CARE
elif st.session_state.page == "homecare":
    st.title("🏠 Home Services")

    service = st.selectbox("Select Service", ["Nurse", "Physiotherapy", "Elder Care"])

    if st.button("Book Service"):
        st.success(f"{service} booked!")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# 🧪 LAB TESTS
elif st.session_state.page == "lab":
    st.title("🧪 Lab Tests")

    test = st.selectbox("Select Test", ["Blood Test", "Diabetes", "Covid Test"])

    if st.button("Book Test"):
        st.success(f"{test} booked!")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------- FOOTER ----------------
st.write("---")
st.write("© 2026 HealthCare+ | Your Digital Health Partner")
