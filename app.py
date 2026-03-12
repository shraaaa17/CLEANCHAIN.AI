import streamlit as st
from dashboards.ngo_dashboard import show_ngo_dashboard
from dashboards.corporate_dashboard import show_corporate_dashboard
from dashboards.admin_dashboard import show_admin_dashboard
import streamlit as st
import time
from streamlit_lottie import st_lottie
import requests

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0E1117;
}

/* Title color */
h1, h2, h3 {
    color: #2ECC71;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(145deg, #2ECC71, #2D9CDB);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 25px;
    font-weight: bold;
    box-shadow: 4px 4px 10px #000000, -2px -2px 6px #1B3C59;
}

.stButton>button:hover {
    background: linear-gradient(145deg, #2D9CDB, #2ECC71);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* 3D Input Boxes */
input, textarea, .stTextInput input, .stNumberInput input {

    border-radius: 12px !important;
    padding: 10px !important;

    background: #0f172a !important;
    color: white !important;

    box-shadow:
        inset 3px 3px 6px #050505,
        inset -3px -3px 6px #1b3c59;

    border: 1px solid #2D9CDB !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background-color: #0f172a;
    border-radius: 12px;
    border: 1px solid #2D9CDB;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* CleanChain Gradient Background */

.stApp {
    background: linear-gradient(
        135deg,
        #0b1f2a 0%,
        #1b3c59 30%,
        #2d9cdb 60%,
        #1dbf73 100%
    );

    background-attachment: fixed;
}

/* Add 3D glow effect */

.stApp::before {
    content: "";
    position: fixed;
    top: -200px;
    left: -200px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, #2ecc71 0%, transparent 70%);
    opacity: 0.2;
    z-index: -1;
}

.stApp::after {
    content: "";
    position: fixed;
    bottom: -200px;
    right: -200px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, #2d9cdb 0%, transparent 70%);
    opacity: 0.25;
    z-index: -1;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

.stApp {
    background: linear-gradient(-45deg, #1B3C59, #2D9CDB, #1DBF73, #2ECC71);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

.block-container{
    background: rgba(0,0,0,0.25);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 30px;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Main gradient background */

.stApp {
    background: linear-gradient(
        135deg,
        #0b1f2a,
        #1b3c59,
        #2d9cdb,
        #1dbf73
    );
    background-attachment: fixed;
}

/* CleanChain watermark logo */

.stApp::after {

    content: "";

    position: fixed;

    top: 50%;
    left: 50%;

    transform: translate(-50%, -50%);

    width: 600px;
    height: 600px;

    background-image: url("assets/cleanchain_logo.png");

    background-repeat: no-repeat;
    background-size: contain;
    background-position: center;

    opacity: 0.07;   /* watermark effect */

    pointer-events: none;

    z-index: -1;
}

/* soft glow effects */

.stApp::before {

    content: "";

    position: fixed;

    top: -200px;
    left: -200px;

    width: 500px;
    height: 500px;

    background: radial-gradient(circle, #2ecc71, transparent);

    opacity: 0.15;

    z-index: -1;
}

</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,5])

with col1:
    st.image("assets/cleanchain_logo.png", width=90)

with col2:
    st.title("CleanChain")
    st.caption("Verifiably Green")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



# Example animations
dirty_earth = load_lottieurl(
"https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json"
)

ai_scan = load_lottieurl(
"https://assets4.lottiefiles.com/packages/lf20_4kx2q32n.json"
)

blockchain = load_lottieurl(
"https://assets1.lottiefiles.com/packages/lf20_kdx6cani.json"
)

earth_anim = load_lottieurl(
"https://assets2.lottiefiles.com/packages/lf20_fcfjwiyb.json"
)

ai_anim = load_lottieurl(
"https://assets1.lottiefiles.com/packages/lf20_kkflmtur.json"
)

blockchain_anim = load_lottieurl(
"https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json"
)
# Intro animation sequence
def cleanchain_intro():

    st.markdown("## 🌍 Initializing CleanChain Platform")

    placeholder = st.empty()

    with placeholder.container():

        st.markdown("### 🌎 Detecting Environmental Condition")
        st_lottie(earth_anim, height=260)

    time.sleep(2)

    placeholder.empty()

    with placeholder.container():

        st.markdown("### 🤖 Running AI Waste Detection")
        st_lottie(ai_anim, height=260)

    time.sleep(2)

    placeholder.empty()

    with placeholder.container():

        st.markdown("### ⛓ Recording Impact on Blockchain")
        st_lottie(blockchain_anim, height=260)

    time.sleep(2)

    placeholder.empty()

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.image("assets/cleanchain_logo.png", width=250)
   

    st.success("Platform Ready")

# ---------------- SESSION STATE ----------------

if "role" not in st.session_state:
    st.session_state.role = None

if "pending_ngos" not in st.session_state:
    st.session_state.pending_ngos = []

# ---------------- LANDING PAGE ----------------

if "intro_shown" not in st.session_state:

    cleanchain_intro()

    st.session_state.intro_shown = True

def show_landing_page():

    option = st.selectbox(
        "Choose your role",
        ["NGO Login", "NGO Signup", "Corporate Login", "Admin Login"]
    )

    # ---------------- NGO SIGNUP ----------------

    if option == "NGO Signup":

        st.header("NGO Registration")

        ngo_name = st.text_input("NGO Name")
        reg_no = st.text_input("Registration Number")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        certificate = st.file_uploader("Upload NGO Certificate")

        if st.button("Submit for Verification", key="ngo_signup_btn"):

            ngo_data = {
                "name": ngo_name,
                "reg_no": reg_no,
                "email": email,
                "password": password,
                "verified": False
            }

            st.session_state.pending_ngos.append(ngo_data)

            st.success("Registration submitted for admin verification.")

    # ---------------- NGO LOGIN ----------------

    elif option == "NGO Login":

        st.header("NGO Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", key="ngo_login_btn"):

            found_user = None

            for ngo in st.session_state.pending_ngos:
                if ngo["email"] == email and ngo["password"] == password:
                    found_user = ngo
                    break

            if found_user:

                if found_user["verified"]:
                    st.session_state.role = "ngo"
                    st.rerun()

                else:
                    st.warning("Your NGO is not verified yet by admin.")

            else:
                st.error("Invalid credentials")

            # ---------------- CORPORATE SIGNUP/login ----------------

    elif option == "Corporate Login":

                st.header("Corporate Login")

                login_email = st.text_input("Corporate Email", key="corp_login_email")
                login_password = st.text_input("Password", type="password", key="corp_login_password")
                if st.button("Login", key="corp_login"):

                    if "corporates" not in st.session_state:
                        st.session_state.corporates = [
                            {"email": "corp@ecotech.com", "password": "1234"}
                        ]

                    found = False

                    for corp in st.session_state.corporates:
                        if corp["email"] == login_email and corp["password"] == login_password:
                            found = True

                    if found:
                        st.session_state.role = "corporate"
                        st.success("Login successful")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

                st.subheader("New Corporate? Register")

                company_name = st.text_input("Company Name", key="corp_reg_company")

                email = st.text_input("Corporate Email", key="corp_reg_email")

                password = st.text_input("Password", type="password", key="corp_reg_password")
                
                if st.button("Register", key="corp_signup_btn"):

                    if company_name and email and password:

                        if "corporates" not in st.session_state:
                            st.session_state.corporates = []

                        st.session_state.corporates.append({
                            "company": company_name,
                            "email": email,
                            "password": password
                        })

                        st.success("Corporate account created successfully!")

                    else:
                        st.error("Please fill all fields")

    # ---------------- ADMIN LOGIN ----------------

    elif option == "Admin Login":

        st.header("Admin Login")

        admin_pass = st.text_input("Admin Password", type="password")

        if st.button("Login as Admin", key="admin_login_btn"):

            if admin_pass == "admin123":
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("Invalid password")


# ---------------- ROLE BASED DASHBOARDS ----------------

if st.session_state.role == "ngo":
    show_ngo_dashboard()

elif st.session_state.role == "corporate":
    show_corporate_dashboard()

elif st.session_state.role == "admin":
    show_admin_dashboard()

else:
    show_landing_page()