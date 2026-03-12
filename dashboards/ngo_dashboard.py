import streamlit as st
st.sidebar.image("assets/cleanchain_logo.png", width=120)
st.sidebar.title("CleanChain")
st.sidebar.caption("CSR Transparency Platform")

def show_ngo_dashboard():

     # Back / Logout button
    if st.sidebar.button("Logout", key="ngo_logout"):
        st.session_state.role = None
        st.rerun()

    st.title("🌱 NGO Dashboard")

    # ensure campaigns storage exists
    if "campaigns" not in st.session_state:

     st.session_state.campaigns = [

        {
            "Campaign": "Versova Beach Cleanup",
            "Location": "Versova Beach",
            "Date": "20 June 2026",
            "Status": "Approved",
            "Corporate": "EcoCorp",
            "Total Fund": 100000,
            "Upfront": 40000,
            "Remaining": 60000
        },

        {
            "Campaign": "Juhu Plastic Removal Drive",
            "Location": "Juhu Beach",
            "Date": "10 May 2026",
            "Status": "Completed",
            "Corporate": "GreenEarth Ltd",
            "Total Fund": 75000,
            "Upfront": 30000,
            "Remaining": 0
        },

        {
            "Campaign": "Marine Drive Waste Audit",
            "Location": "Marine Drive",
            "Date": "15 July 2026",
            "Status": "Proposed",
            "Corporate": "Pending Approval",
            "Total Fund": 120000,
            "Upfront": 0,
            "Remaining": 0
        }

    ]


    menu = st.sidebar.radio(
        "Navigation",
        [
            "Create Campaign Proposal",
            "My Campaigns",
            "Campaign Execution",
            "Submit Impact Proof",
            "Funding Status"
        ]
    )

    # ---------------- CREATE CAMPAIGN ----------------

    if menu == "Create Campaign Proposal":

        st.header("Create New Campaign")

        title = st.text_input("Campaign Title")
        location = st.text_input("Location")
        date = st.date_input("Campaign Date")

        volunteers = st.number_input(
            "Expected Volunteers",
            min_value=0,
            step=1
        )

        waste_type = st.selectbox(
            "Waste Type",
            ["Plastic", "Organic", "Mixed"]
        )

        budget = st.number_input(
            "Budget Required",
            min_value=0
        )

        description = st.text_area("Campaign Description")

        if st.button("Submit Campaign Proposal", key="campaign_submit_btn"):

            campaign = {
                "Campaign": title,
                "Location": location,
                "Budget": budget,
                "Date": date,
                "Upfront": int(budget * 0.4),
                "Remaining": int(budget * 0.6)
            }

            st.session_state.campaigns.append(campaign)

            st.success("Campaign proposal submitted to corporates.")

    # ---------------- MY CAMPAIGNS ----------------

    elif menu == "My Campaigns":

        st.header("My Campaigns")

        for campaign in st.session_state.campaigns:

            with st.container():

                col1, col2, col3 = st.columns(3)

                col1.write(f"### {campaign['Campaign']}")
                col2.write(f"📍 {campaign['Location']}")
                col3.write(f"📅 {campaign['Date']}")

                status = campaign["Status"]

                if status == "Proposed":
                    st.warning("Status: Proposed (Awaiting Corporate Approval)")

                elif status == "Approved":
                    st.success("Status: Approved")

                elif status == "Completed":
                    st.info("Status: Completed")

                st.divider()

    # ---------------- CAMPAIGN EXECUTION ----------------

    elif menu == "Campaign Execution":

        st.header("Campaign Execution")

        approved_campaigns = [
        c for c in st.session_state.campaigns
        if c["Status"] == "Approved"
        ]

        if len(approved_campaigns) == 0:

            st.info("No approved campaigns yet.")

        else:

            for campaign in approved_campaigns:

                st.subheader(campaign["Campaign"])

                st.write("Corporate Sponsor:", campaign["Corporate"])

                col1, col2, col3 = st.columns(3)

                col1.metric("Total Fund", f"₹{campaign['Total Fund']}")
                col2.metric("Upfront Received", f"₹{campaign['Upfront']}")
                col3.metric("Remaining Payment", f"₹{campaign['Remaining']}")

                st.progress(40)

                st.divider()

    # ---------------- IMPACT PROOF ----------------

    elif menu == "Submit Impact Proof":

        st.header("Upload Impact Proof")

    # Ensure campaigns list exists
        if "campaigns" not in st.session_state:
            st.session_state.campaigns = []

    # Campaign selection
        if len(st.session_state.campaigns) > 0:
            campaign_names = [c["Campaign"] for c in st.session_state.campaigns]
        else:
            campaign_names = ["Demo Cleanup Campaign"]

        campaign = st.selectbox("Select Campaign", campaign_names)

        st.subheader("Before Cleanup")

        before_img = st.file_uploader(
                "Upload BEFORE Image",
                type=["jpg", "png"],
                key="before_upload"
            )

        st.subheader("After Cleanup")

        after_img = st.file_uploader(
                "Upload AFTER Image",
                type=["jpg", "png"],
                key="after_upload"
            )

        if st.button("Run AI Analysis", key="ai_analysis_btn"):

            if before_img and after_img:

                    score = 78  # temporary AI score

                    st.success("Impact Analysis Complete")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.image(before_img, caption="Before Cleanup")

                    with col2:
                        st.image(after_img, caption="After Cleanup")

                    st.metric("Cleanliness Score", f"{score}%")

                    st.write("Waste Removed: 250 kg")

            else:
                    st.warning("Please upload both BEFORE and AFTER images.")

    # ---------------- FUNDING STATUS ----------------

    elif menu == "Funding Status":

        st.header("Funding Status")

        funding = {
            "Campaign": ["Versova Cleanup"],
            "Total Fund": ["₹100000"],
            "Upfront Received": ["₹40000"],
            "Remaining": ["₹60000"],
            "Status": ["Pending Final Release"]
        }

        st.table(funding)