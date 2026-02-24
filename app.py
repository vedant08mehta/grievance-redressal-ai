import streamlit as st
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Grievance System")

st.title("Student Grievance Redressal System")
st.subheader("AI-Based Complaint Classification Portal")

st.write("Enter your grievance below.")

complaint = st.text_area("Write your complaint here:")

if st.button("Submit Complaint"):

    if complaint.strip() == "":
        st.warning("Please enter your complaint first.")
    else:
        prediction = model.predict([complaint])[0]

        st.success("Complaint Submitted Successfully!")

        st.markdown("### Assigned Department:")
        st.info(prediction)

st.markdown("---")
st.caption("Developed for Ingenium Project Expo | AI-Based System")