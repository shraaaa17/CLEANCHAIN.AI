import streamlit as st
col1, col2 = st.columns([8,1])

with col2:
    if st.button("Logout", key="admin_logout"):
        st.session_state.role = None
        st.rerun()

st.sidebar.image("assets/cleanchain_logo.png", width=120)
st.sidebar.title("CleanChain")
st.sidebar.caption("CSR Transparency Platform")

def show_admin_dashboard():

    if st.sidebar.button("⬅ Back to Home", key="admin_back_home"):
        st.session_state.role = None
        st.rerun()

    st.title("Admin Panel")

    if "pending_ngos" not in st.session_state or len(st.session_state.pending_ngos) == 0:

        st.info("No NGOs pending verification.")

    else:

        st.header("Pending NGO Registrations")

        for i, ngo in enumerate(st.session_state.pending_ngos):

            with st.expander(f"{ngo['name']}"):

                st.write("Registration Number:", ngo["reg_no"])
                st.write("Email:", ngo["email"])

                col1, col2 = st.columns(2)

                if col1.button("Approve", key=f"approve_{i}"):

                    ngo["verified"] = True
                    st.success("NGO Approved")

                if col2.button("Reject", key=f"reject_{i}"):

                    st.session_state.pending_ngos.pop(i)
                    st.warning("NGO Rejected")

def show_admin_login():

    password = st.text_input("Admin Password", type="password")

    if st.button("Login"):

        if password == "admin123":
            st.session_state.role = "admin"
            st.rerun()

        else:
            st.error("Invalid password")