import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px

# --- 1. DATABASE CONNECTION ---
def connect_to_sheet(sheet_name):
    try:
        creds_info = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)
        sheet = client.open("UserDatabase").worksheet(sheet_name)
        return sheet
    except Exception as e:
        st.error(f"Error connecting to {sheet_name}: {e}")
        return None

# --- 2. CONFIG ---
st.set_page_config(page_title="Skill Tracker Pro", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

# --- 3. LOGIN & SIGN UP LOGIC ---
if not st.session_state["logged_in"]:
    st.title("🚀 Skill Tracker Pro")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    user_sheet = connect_to_sheet("Sheet1") # Sheet1 for Users

    with tab1:
        st.subheader("Login")
        l_user = st.text_input("Username", key="l_user")
        l_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login"):
            all_users = user_sheet.get_all_records()
            found = False
            for row in all_users:
                if str(row['username']) == l_user and str(row['password']) == l_pass:
                    found = True
                    break
            if found:
                st.session_state["logged_in"] = True
                st.session_state["username"] = l_user
                st.rerun()
            else:
                st.error("Ghalat Username ya Password!")

    with tab2:
        st.subheader("Create Account")
        s_user = st.text_input("Username", key="s_user")
        s_email = st.text_input("Email", key="s_email")
        s_pass = st.text_input("Password", type="password", key="s_pass")
        if st.button("Sign Up"):
            if s_user and s_pass:
                user_sheet.append_row([s_user, s_pass, s_email])
                st.success("Account ban gaya! Ab Login tab par jayen.")
            else:
                st.error("Saari fields bharen.")

# --- 4. MAIN DASHBOARD ---
else:
    user_now = st.session_state["username"]
    st.title(f"📊 {user_now}'s Dashboard")
    
    skill_sheet = connect_to_sheet("SkillsData") # SkillsData sheet for skills

    with st.sidebar:
        st.header("➕ Add Skill")
        s_name = st.text_input("Skill Name")
        s_prog = st.slider("Progress %", 0, 100, 50)
        if st.button("Save Skill"):
            skill_sheet.append_row([user_now, s_name, s_prog])
            st.success("Saved!")
            st.rerun()
        
        if st.button("Logout"):
          # --- 4. MAIN DASHBOARD ---
    # ... (baaki code wahi rahega)

    skill_sheet = connect_to_sheet("SkillsData")

    if skill_sheet is not None:
        with st.sidebar:
            st.header("➕ Add Skill")
            s_name = st.text_input("Skill Name")
            s_prog = st.slider("Progress %", 0, 100, 50)
            if st.button("Save Skill"):
                skill_sheet.append_row([user_now, s_name, s_prog])
                st.success("Saved!")
                st.rerun()
            
            if st.button("Logout"):
                st.session_state["logged_in"] = False
                st.rerun()

        # Data Fetching
        try:
            data = skill_sheet.get_all_records()
            if data:
                df = pd.DataFrame(data)
                # Baaki graphs wala code yahan aayega...
            else:
                st.info("Abhi tak koi data nahi hai. Sidebar se add karein!")
        except Exception as e:
            st.error(f"Data parhne mein masla: {e}")
    else:
        st.error("Error: 'SkillsData' wali sheet nahi mili. Please Google Sheet mein tab banayein!")
