import streamlit as st

# Logout button
col1, col2 = st.columns([8,1])

with col2:
    if st.button("Logout", key="corporate_logout"):
        st.session_state.role = None
        st.rerun()

st.sidebar.image("assets/cleanchain_logo.png", width=120)
st.sidebar.title("CleanChain")
st.sidebar.caption("CSR Transparency Platform")


# -------------------------
# CORPORATE REGISTRATION
# -------------------------

st.subheader("Corporate Registration")

company_name = st.text_input("Company Name", key="corp_reg_company")

email = st.text_input("Corporate Email", key="corp_reg_email")

password = st.text_input("Password", type="password", key="corp_reg_password")

if st.button("Register", key="corp_reg_btn"):

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


# -------------------------
# CORPORATE LOGIN
# -------------------------

st.subheader("Corporate Login")

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


# -------------------------
# CORPORATE DASHBOARD
# -------------------------

def show_corporate_dashboard():

    if st.sidebar.button("⬅ Back to Home", key="corp_back_home"):
        st.session_state.role = None
        st.rerun()

    st.title("🏢 Corporate CSR Dashboard")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Verified NGOs",
            "Campaign Proposals",
            "Approved Campaigns",
            "Escrow Funding",
            "Impact Monitoring",
            "CSR Analytics"
        ]
    )

    if menu == "Verified NGOs":

        st.header("Verified NGOs")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total NGOs", 12)
        col2.metric("Active NGOs", 8)
        col3.metric("Cities Covered", 5)

        st.subheader("NGO Directory")

        data = {
            "NGO Name": ["Clean Mumbai", "Green Earth"],
            "Location": ["Mumbai", "Pune"],
            "Credibility Score": [82, 76],
            "Status": ["Verified", "Verified"]
        }

        st.table(data)


    elif menu == "Campaign Proposals":

        st.header("NGO Campaign Proposals")

        proposal = {
            "Campaign": ["Versova Beach Cleanup"],
            "NGO": ["Clean Mumbai"],
            "Location": ["Versova"],
            "Budget": ["₹100000"],
            "Date": ["20 June"]
        }

        st.table(proposal)

        st.write("### Approve Campaign")

        campaign = st.selectbox(
            "Select Campaign",
            ["Versova Beach Cleanup"]
        )

        if st.button("Approve Campaign"):
            st.success("Campaign approved and moved to funding stage")

        if st.button("Reject Campaign"):
            st.warning("Campaign rejected")


    elif menu == "Approved Campaigns":

        st.header("Approved Campaigns")

        data = {
            "Campaign": ["Versova Cleanup"],
            "NGO": ["Clean Mumbai"],
            "Budget": ["₹100000"],
            "Status": ["Awaiting Funding"]
        }

        st.table(data)


    elif menu == "Escrow Funding":

        st.header("CSR Escrow Funding")

        campaign = st.selectbox(
            "Select Campaign",
            ["Versova Cleanup"]
        )

        total_fund = st.number_input("Total CSR Budget", value=100000)

        upfront = st.slider(
            "Upfront Funding (%)",
            10, 70, 40
        )

        final_payment = 100 - upfront

        st.write(f"Upfront Release: {upfront}%")
        st.write(f"Final Release: {final_payment}%")

        if st.button("Lock Funds in Escrow"):
            st.success("Funds locked in smart contract")


    elif menu == "Impact Monitoring":

        st.header("Campaign Impact Monitoring")

        st.subheader("Versova Beach Cleanup")

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/6/6e/Garbage_on_beach.jpg",
                caption="Before Cleaning"
            )

        with col2:
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/0/0e/Clean_beach.jpg",
                caption="After Cleaning"
            )

        st.metric("Cleanliness Score", "78%")

        st.write("Waste Removed: 250kg")

        st.write("IPFS Hash: QmX23ABC...")


    elif menu == "CSR Analytics":

        st.header("CSR Impact Analytics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Campaigns Funded", 5)
        col2.metric("CSR Budget Used", "₹500000")
        col3.metric("Avg Cleanliness Improvement", "74%")

        st.progress(74)


# -------------------------
# LOAD DASHBOARD AFTER LOGIN
# -------------------------

if st.session_state.get("role") == "corporate":
    show_corporate_dashboard()

if st.session_state.get("role") != "corporate":
    # show registration + login
    pass