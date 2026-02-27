# Student Grievance Redressal System

A web app that lets students submit complaints and track their resolution status. Complaints are automatically classified into departments using a machine learning model.

---

## Features

- Submit complaints with your name and room number
- Auto-classification of complaints into departments using ML
- Track complaint status using a unique complaint ID
- Rate your experience once a complaint is resolved
- Admin panel to manage and update complaint statuses
- Stats dashboard showing total, resolved, pending, and in-progress complaints

---

## Project Structure

```
Grievance/
├── .streamlit/
│   └── config.toml       # App theme
├── app.py                # Main Streamlit app
├── training.py           # Model training script
├── grievances.csv        # Training data
├── complaints.csv        # Submitted complaints (auto-created)
└── model.pkl             # Trained ML model (auto-created)
```

---

## Setup

1. Install dependencies:
   ```
   pip install streamlit pandas scikit-learn
   ```

2. Train the model:
   ```
   python training.py
   ```

3. Run the app:
   ```
   streamlit run app.py
   ```

---

## Departments

Complaints are classified into one of five departments: Maintenance, Accounts, Academics, Examination, and Library.

---

## Tech Stack

- Python
- Streamlit
- Scikit-learn (Logistic Regression + TF-IDF)
- Pandas

---

## Admin Access

Go to the **Admin** tab and enter the password to manage complaints. Default password: `admin123`
