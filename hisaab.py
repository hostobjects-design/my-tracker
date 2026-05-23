import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration (Is se Google par naam acha aata hai)
st.set_page_config(page_title="Abdullah Pro Tracker", page_icon="🚀", layout="wide")

# 2. Login System
def check_password():
    """Returns True if the user had the correct password."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔐 Welcome to Abdullah's App")
        username = st.text_input("Username", placeholder="Apna naam likhen")
        password = st.text_input("Password", type="password", placeholder="Password dalein")
        
        if st.button("Unlock App"):
            if username == "abdullah" and password == "baba123": # Password change kar sakte hain
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Ghalat credentials! Dobara koshish karein.")
        return False
    return True

# Agar login success ho jaye tabhi niche wala kaam chale
if check_password():
    
    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

    # --- MAIN APP INTERFACE ---
    st.title("🚀 Abdullah's Skill Progress Tracker")
    st.markdown("---")

    # Sidebar for Inputs
    with st.sidebar:
        st.header("📝 Naya Data Add Karein")
        date = st.date_input("Aaj ki Tareekh", datetime.now())
        task = st.text_input("Kya seekha?", placeholder="e.g. Python Functions")
        hours = st.number_input("Kitne ghante lagaye?", min_value=0.1, max_value=24.0, step=0.5)
        category = st.selectbox("Category", ["Coding", "Learning", "Design", "Research"])
        
        if st.button("Save Entry 💾"):
            st.balloons()
            st.success(f"Zabardast! {task} save ho gaya.")
            # Note: Database connection ke baghair ye refresh par urr jayega.
            # Lekin Monday ke demo ke liye ye best hai!

    # Layout for Stats
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 Aapki Progress")
        # Dummy data for the graph
        chart_data = pd.DataFrame({
            'Category': ['Coding', 'Learning', 'Design', 'Research'],
            'Hours': [5, 3, 2, 1] # Ye data aap manual update kar sakte hain abhi
        })
        st.bar_chart(chart_data.set_index('Category'))

    with col2:
        st.subheader("💡 Motivation for Today")
        st.info("The more you practice, the luckier you get. Keep coding, Abdullah!")
        
        st.subheader("📅 Recent History")
        st.write(f"**Last Entry:** {task if task else 'No entry yet'}")
        st.write(f"**Total Hours Today:** {hours}")

# Footer
st.markdown("---")
st.caption("Created with ❤️ by Abdullah Developer | 2026")
st.markdown("---")
st.caption("Created with ❤️ by Abdullah Developer | 2026")
