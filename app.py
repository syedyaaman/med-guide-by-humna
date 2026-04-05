import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Health App", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    .topbar {
        background-color: #0B3C6D;
        padding: 12px 30px;
        border-radius: 10px;
        color: white;
        font-size: 18px;
    }
    .search-box {
        background-color: #F1F3F6;
        padding: 10px;
        border-radius: 20px;
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: #F9FAFB;
        text-align: center;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }
    .btn {
        background-color: #0B3C6D;
        color: white;
        padding: 8px 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2, col3 = st.columns([2,5,2])

with col1:
    st.markdown("<div class='topbar'><b>HealthCare+</b></div>", unsafe_allow_html=True)

with col2:
    st.text_input("Search Medicines...", key="search")

with col3:
    if st.session_state.logged_in:
        st.success("Logged In ✅")
        if st.button("Logout"):
            st.session_state.logged_in = False
    else:
        if st.button("Sign In"):
            st.session_state.show_login = True

# ---------------- LOGIN FORM ----------------
if "show_login" in st.session_state and st.session_state.show_login:
    st.subheader("🔐 Sign In")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.session_state.show_login = False
            st.success("Login Successful!")
        else:
            st.error("Invalid credentials")

# ---------------- HERO SECTION ----------------
st.markdown("""
    <div style='background-color:#2E6EB5;padding:30px;border-radius:15px;color:white'>
    <h1>Tired of Waiting at Hospital?</h1>
    <h3>Let us handle everything for you</h3>
    </div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- CARDS SECTION ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='card'><h4>Pharmacy</h4><p>Upload prescription</p></div>", unsafe_allow_html=True)
    st.button("Order Now", key="p1")

with col2:
    st.markdown("<div class='card'><h4>Doctor</h4><p>Consult online</p></div>", unsafe_allow_html=True)
    st.button("Book Now", key="p2")

with col3:
    st.markdown("<div class='card'><h4>Home Care</h4><p>Services at home</p></div>", unsafe_allow_html=True)
    st.button("Book Now", key="p3")

with col4:
    st.markdown("<div class='card'><h4>Lab Tests</h4><p>Checkups</p></div>", unsafe_allow_html=True)
    st.button("Book Now", key="p4")

# ---------------- FOOTER ----------------
st.write("---")
st.write("© 2026 HealthCare+ App")
