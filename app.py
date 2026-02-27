import streamlit as st
import pandas as pd
import pickle
import uuid

st.set_page_config(page_title="Student Grievance Redressal System", layout="wide", page_icon="🎓")

st.markdown("""
    <style>
        .block-container {
            padding: 2rem 3rem;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {
            border-radius: 8px;
            border: 1px solid #4F46E5;
            background-color: #1E293B;
        }

        div[data-testid="stButton"] button {
            background-color: #4F46E5;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            border: none;
            transition: background-color 0.2s ease;
        }

        div[data-testid="stButton"] button:hover {
            background-color: #4338CA;
        }

        div[data-testid="stTabs"] button {
            font-size: 1rem;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

def load_complaints():
    try:
        return pd.read_csv("complaints.csv")
    except:
        return pd.DataFrame(columns=["ComplaintID","Name","Room","Complaint","Department","Status","Rating"])

def save_complaints(df):
    df.to_csv("complaints.csv", index=False)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

if "submitted" not in st.session_state:
    st.session_state.submitted = False

home, status, admin, about = st.tabs(["Home", "Complaint Status", "Admin", "About"])

with home:

    complaints_df = load_complaints()

    st.title("Student Grievance Redressal System")

    total = len(complaints_df)
    st.write(f"📬 Total complaints submitted so far: **{total}**")

    st.divider()

    if st.session_state.submitted == False:

        name = st.text_input("Name")
        room = st.text_input("Room Number")
        complaint_text = st.text_area("Enter your Complaint")

        if st.button("Submit Complaint"):

            if name.strip() == "" or room.strip() == "" or complaint_text.strip() == "":
                st.warning("Please fill all fields.")
            else:

                with st.spinner("Classifying your complaint..."):
                    department = model.predict([complaint_text])[0]

                complaint_id = str(uuid.uuid4())[:8]

                new_row = pd.DataFrame({
                    "ComplaintID": [complaint_id],
                    "Name": [name],
                    "Room": [room],
                    "Complaint": [complaint_text],
                    "Department": [department],
                    "Status": ["Pending"],
                    "Rating": [""]
                })

                updated_df = pd.concat([load_complaints(), new_row], ignore_index=True)
                save_complaints(updated_df)

                st.session_state.submitted = True
                st.session_state.cid = complaint_id
                st.session_state.dept = department
                st.rerun()

    else:

        st.success("Complaint submitted successfully")

        st.write("Complaint ID:")
        st.code(st.session_state.cid)
        st.write("Assigned Department:", st.session_state.dept)

with status:

    complaints_df = load_complaints()

    st.title("Check Complaint Status")

    complaint_id = st.text_input("Enter Complaint ID")

    if st.button("Check Status"):

        result = complaints_df[complaints_df["ComplaintID"] == complaint_id]

        if result.empty:
            st.error("Complaint ID not found")
        else:

            name = result.iloc[0]["Name"]
            room = result.iloc[0]["Room"]
            department = result.iloc[0]["Department"]
            complaint_text = result.iloc[0]["Complaint"]
            status_value = result.iloc[0]["Status"]
            existing_rating = result.iloc[0]["Rating"] if "Rating" in result.columns else None

            department_icons = {
                "Maintenance": "🔧",
                "Accounts": "💰",
                "Academics": "📚",
                "Examination": "📝",
                "Library": "📖"
            }

            dept_icon = department_icons.get(department, "🏢")

            st.write("Name:", name)
            st.write("Room:", room)
            st.write(f"Department: {dept_icon} {department}")
            st.write("Complaint:", complaint_text)

            if status_value == "Resolved":
                st.success("Status: Resolved")

                st.divider()

                if pd.notna(existing_rating) and existing_rating != "":
                    st.write(f"Your Rating: {'⭐' * int(existing_rating)}")
                else:
                    st.subheader("Rate your experience")
                    rating = st.feedback("stars")

                    if rating is not None:
                        complaints_df.loc[complaints_df["ComplaintID"] == complaint_id, "Rating"] = rating + 1
                        save_complaints(complaints_df)
                        st.success(f"Thank you for rating us {'⭐' * (rating + 1)}")

            elif status_value == "In Progress":
                st.warning("Status: In Progress")
            else:
                st.info("Status: Pending")

with admin:

    complaints_df = load_complaints()

    st.title("Admin Panel")

    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":

        st.success("Access Granted")

        st.divider()

        dept_filter = st.selectbox("Filter by Department", ["All", "Maintenance", "Accounts", "Academics", "Examination", "Library"])
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Resolved"])

        filtered_df = complaints_df.dropna(subset=["ComplaintID"])

        if dept_filter != "All":
            filtered_df = filtered_df[filtered_df["Department"] == dept_filter]
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]

        st.dataframe(filtered_df[["ComplaintID", "Name", "Room", "Complaint", "Department", "Status"]], use_container_width=True)

        st.divider()

        st.subheader("Update Complaint Status")

        update_id = st.text_input("Enter Complaint ID to Update")
        new_status = st.selectbox("New Status", ["Pending", "In Progress", "Resolved"])

        if st.button("Update Status"):
            if update_id.strip() == "":
                st.warning("Please enter a Complaint ID")
            else:
                match = complaints_df[complaints_df["ComplaintID"] == update_id]
                if match.empty:
                    st.error("Complaint ID not found")
                else:
                    complaints_df.loc[complaints_df["ComplaintID"] == update_id, "Status"] = new_status
                    save_complaints(complaints_df)
                    st.success(f"Status updated to {new_status}")

    elif password != "":
        st.error("Incorrect password")

with about:

    complaints_df = load_complaints()

    total = len(complaints_df)
    resolved = len(complaints_df[complaints_df["Status"] == "Resolved"])
    pending = len(complaints_df[complaints_df["Status"] == "Pending"])
    in_progress = len(complaints_df[complaints_df["Status"] == "In Progress"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Complaints", total)
    with col2:
        st.metric("Resolved", resolved)
    with col3:
        st.metric("In Progress", in_progress)
    with col4:
        st.metric("Pending", pending)

    st.divider()

    st.title("About")

    st.write(
        """
        The Student Grievance Redressal System allows students to submit complaints
        and track their resolution status.

        Complaints are automatically classified into departments using a
        machine learning model.
        """
    )

    st.subheader("Model")

    st.write(
        """
        Logistic Regression with TF-IDF vectorization implemented using a
        Scikit-learn pipeline.
        """
    )

    st.subheader("Model Accuracy")

    st.write("86%")

    st.subheader("Technologies Used")

    st.write(
        """
        Python  
        Streamlit  
        Scikit-learn  
        Natural Language Processing  
        Pandas
        """
    )