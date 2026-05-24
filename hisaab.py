import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# --- 1. GOOGLE SHEETS CONNECTION ---
def connect_to_sheet():
    try:
        # Streamlit Secrets se data uthana
        creds_info = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)
        # Sheet ka naam wahi rakhen jo aapne rakha hai
        sheet = client.open("UserDatabase").sheet1
        return sheet
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None

# --- 2. APP CONFIG ---
st.set_page_config(page_title="Skill Tracker Pro", page_icon="📈")
sheet = connect_to_sheet()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

# --- 3. LOGIN / SIGN UP UI ---
if not st.session_state["logged_in"]:
    st.title("🚀 Skill Tracker Pro")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login to your account")
        l_user = st.text_input("Username", key="l_user")
        l_pass = st.text_input("Password", type="password", key="l_pass")
        
        if st.button("Login"):
            all_data = sheet.get_all_records()
            user_found = False
            for row in all_data:
                if str(row['username']) == l_user and str(row['password']) == l_pass:
                    user_found = True
                    break
            
            if user_found:
                st.session_state["logged_in"] = True
                st.session_state["username"] = l_user
                st.success(f"Welcome back, {l_user}!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    with tab2:
        st.subheader("Create a new account")
        s_user = st.text_input("Choose Username", key="s_user")
        s_email = st.text_input("Email Address", key="s_email")
        s_pass = st.text_input("Choose Password", type="password", key="s_pass")

        if st.button("Create Account"):
            if s_user and s_pass:
                all_users = sheet.col_values(1)
                if s_user in all_users:
                    st.warning("Username already exists. Try another.")
                else:
                    sheet.append_row([s_user, s_pass, s_email])
                    st.balloons()
                    st.success("Account created successfully! Now go to Login tab.")
            else:
                st.error("Please fill all fields.")

# --- 4. MAIN DASHBOARD (Only after Login) ---
else:
    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.title("📊 Your Skill Dashboard") # Dashboard ke andar naya skill add karne ka form
    with st.expander("➕ Add New Skill"):
        new_skill = st.text_input("Skill Name")
        progress = st.slider("Progress", 0, 100, 25)
        if st.button("Save Skill"):
            # Yahan hum aik aur sheet bana sakte hain skills save karne ke liye
            st.success(f"{new_skill} saved at {progress}%!")

    # Skill Display (Dummy data for now)
    st.subheader("Your Progress")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Python**")
        st.progress(80)
    with col2:
        st.write("**Marketing**")
        st.progress(45)
    st.info(f"Logged in as: {st.session_state['username']}")
    
    # Placeholder for Tracker Content
    st.write("---")
    st.write("Ab aap yahan apna tracker ka saara kaam kar sakte hain.")
    st.success("App is successfully connected to Google Sheets! ✅")
