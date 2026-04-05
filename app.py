import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Med Guide Pro", layout="wide")

# ---------------- SESSION STATE ----------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- CSS ----------------
st.markdown("""
<style>
.navbar {
    background-color: #0B3C6D;
    padding: 15px;
    border-radius: 12px;
    color: white;
    font-size: 22px;
    font-weight: bold;
}
.hero {
    background: linear-gradient(90deg, #2E6EB5, #4DA8DA);
    padding: 40px;
    border-radius: 20px;
    color: white;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #F5F7FA;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2, col3 = st.columns([3,5,3])

with col1:
    st.markdown("<div class='navbar'>Med Guide Pro</div>", unsafe_allow_html=True)

with col2:
    st.text_input("🔍 Search medicines, services...")

with col3:
    if st.session_state.logged_in:
        st.success("Logged In ✅")
        if st.button("Logout"):
            st.session_state.logged_in = False
    else:
        colA, colB = st.columns(2)
        with colA:
            if st.button("Sign In"):
                st.session_state.page = "login"
        with colB:
            if st.button("Sign Up"):
                st.session_state.page = "signup"

# ---------------- LOGIN ----------------
if st.session_state.page == "login":
    st.title("🔐 Sign In")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in st.session_state.users and st.session_state.users[user] == pwd:
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.success("Login Successful!")
        else:
            st.error("Invalid credentials")

    if st.button("Go to Sign Up"):
        st.session_state.page = "signup"

    st.stop()

# ---------------- SIGN UP ----------------
if st.session_state.page == "signup":
    st.title("📝 Create Account")

    new_user = st.text_input("Create Username")
    new_pwd = st.text_input("Create Password", type="password")

    if st.button("Register"):
        if new_user in st.session_state.users:
            st.error("User already exists")
        elif new_user == "" or new_pwd == "":
            st.warning("Please fill all fields")
        else:
            st.session_state.users[new_user] = new_pwd
            st.success("Account created! Please login")
            st.session_state.page = "login"

    if st.button("Back to Login"):
        st.session_state.page = "login"

    st.stop()

# ---------------- HERO ----------------
st.markdown("""
<div class='hero'>
<h1>Welcome to Med Guide Pro</h1>
<p>Your smart healthcare assistant</p>
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

# ---------------- YOUR OLD FEATURES ----------------
def run_old_app():
    st.subheader("🔧 Your Existing Features")

    # 👉 PASTE YOUR OLD CODE HERE
    # Example:
    st.write("This is where your previous ML model / PDF generator / logic will run")

# ---------------- ROUTING ----------------
if st.session_state.page == "home":
    run_old_app()

elif st.session_state.page == "pharmacy":
    st.title("💊 Pharmacy")
    st.write("Integrate your pharmacy feature here")
    if st.button("⬅ Back"):
        st.session_state.page = "home"

elif st.session_state.page == "doctor":
    st.title("👨‍⚕️ Doctor Consultation")
    st.write("Integrate your doctor feature here")
    if st.button("⬅ Back"):
        st.session_state.page = "home"

elif st.session_state.page == "homecare":
    st.title("🏠 Home Services")
    st.write("Integrate your home care feature here")
    if st.button("⬅ Back"):
        st.session_state.page = "home"

elif st.session_state.page == "lab":
    st.title("🧪 Lab Tests")
    st.write("Integrate your lab test feature here")
    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------- FOOTER ----------------
st.write("---")
st.write("© 2026 Med Guide Pro | Smart Healthcare App")
