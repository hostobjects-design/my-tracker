import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px # Graphs ke liye

# --- 1. GOOGLE SHEETS CONNECTION ---
def connect_to_sheet(sheet_name):
    try:
        creds_info = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)
        sheet = client.open("UserDatabase").worksheet(sheet_name)
        return sheet
    except Exception as e:
        return None

# --- 2. CONFIG ---
st.set_page_config(page_title="Skill Tracker Pro", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

# --- 3. LOGIN / SIGN UP ---
if not st.session_state["logged_in"]:
    # (Pehla wala login/signup code yahan rahega - assume it's there)
    # [Yahan wahi login wala hissa paste karein jo pehle chal raha tha]
    pass # (Aapne pura login code yahan barqarar rakhna hai)

# --- 4. MAIN DASHBOARD ---
else:
    user_now = st.session_state["username"]
    st.title(f"📊 {user_now}'s Skill Dashboard")
    
    # Do Sheets connect karni hain
    user_sheet = connect_to_sheet("Sheet1")
    skill_sheet = connect_to_sheet("SkillsData")

    # --- Sidebar: Add New Skill ---
    with st.sidebar:
        st.header("➕ Add New Skill")
        skill_input = st.text_input("Skill Name (e.g. Python)")
        prog_input = st.slider("Progress %", 0, 100, 50)
        if st.button("Save to Database"):
            skill_sheet.append_row([user_now, skill_input, prog_input])
            st.success("Skill Saved!")
            st.rerun()
        
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.rerun()

    # --- DATA FETCHING ---
    all_skills = skill_sheet.get_all_records()
    df = pd.DataFrame(all_skills)
    
    # Sirf login user ka data filter karna
    if not df.empty:
        user_df = df[df['username'] == user_now]
        
        if not user_df.empty:
            # --- TOP METRICS ---
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Skills", len(user_df))
            col2.metric("Avg Progress", f"{int(user_df['progress'].mean())}%")
            col3.metric("Top Skill", user_df.sort_values(by='progress', ascending=False).iloc[0]['skill_name'])

            st.write("---")

            # --- GRAPHS SECTION ---
            g1, g2 = st.columns(2)
            
            with g1:
                st.subheader("Skill Progress (Bar Chart)")
                fig_bar = px.bar(user_df, x='skill_name', y='progress', color='progress',
                                 color_continuous_scale='Viridis', text_auto=True)
                st.plotly_chart(fig_bar, use_container_width=True)

            with g2:
                st.subheader("Skill Distribution (Pie Chart)")
                fig_pie = px.pie(user_df, names='skill_name', values='progress', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
                
            # --- DATA TABLE ---
            st.subheader("Detailed Data")
            st.dataframe(user_df[['skill_name', 'progress']], use_container_width=True)
        else:
            st.info("Abhi tak koi skill add nahi kiya. Sidebar se add karein!")
    else:
        st.info("Database khali hai. Pehla skill add karein!")
