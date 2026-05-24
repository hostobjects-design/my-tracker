import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Abdullah's Skill Tracker", page_icon="🚀", layout="centered")

# 2. Simple English Login System
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔐 Sign In")
        st.info("Please enter your credentials to access the dashboard.")
        
        # English Inputs
        username = st.text_input("Username", placeholder="Enter your name")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        if st.button("Sign In"):
            if username == "abdullah" and password == "baba123":
                st.session_state["authenticated"] = True
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password!")
        return False
    return True

# 3. Main App (Only shows if logged in)
if check_password():
    # Sidebar for logout and inputs
    st.sidebar.title("Navigation")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title("📊 My Skill Progress Tracker")
    st.write("Welcome back, Abdullah! Track your daily learning below.")
    st.markdown("---")

    # Entry Section
    with st.sidebar:
        st.header("Add New Task")
        task_name = st.text_input("Task Name", placeholder="e.g., Python Basics")
        duration = st.number_input("Hours Spent", min_value=0.1, max_value=24.0, step=0.5)
        category = st.selectbox("Category", ["Coding", "Learning", "Project", "Research"])
        
        if st.button("Save Entry"):
            st.balloons()
            st.success("Data saved successfully!")

    # Display Graph
    st.subheader("Your Productivity Chart")
    # This is placeholder data for the demo
    chart_data = pd.DataFrame({
        'Category': ['Coding', 'Learning', 'Project', 'Research'],
        'Hours': [8, 5, 3, 2]
    })
    st.bar_chart(chart_data.set_index('Category'))

st.markdown("---")
st.caption("Developed by Abdullah Developer | 2026")
st.caption("Created with ❤️ by Abdullah Developer | 2026")
