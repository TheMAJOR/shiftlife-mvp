import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ShiftLife", page_icon="🏥", layout="centered")

# --- INITIALIZE MEMORY (SESSION STATE) ---
# This acts as the "Long Term Memory" of the app
if 'roster_data' not in st.session_state:
    st.session_state['roster_data'] = None

# --- CORE LOGIC ---
def calculate_life_plan(shift_code):
    if shift_code == "N":
        return "⛔ NIGHT SHIFT", "🔴 Busy", "Recovery Mode: Sleep 8am-3pm."
    elif shift_code == "D":
        return "🏥 DAY SHIFT", "🔴 Busy", "Prep Mode: Meal prep tonight."
    elif shift_code == "OFF":
        return "✅ OFF DUTY", "🟢 Free", "Golden Window: Date Night or Gym!"
    else:
        return "Unknown", "⚪ Check", "Waiting for input..."

# --- CHECK URL MODE ---
query_params = st.query_params
mode = query_params.get("mode", "nurse") 

# ==========================================
# VIEW 1: MARK'S VIEW (Partner Link)
# ==========================================
if mode == "partner":
    st.title("❤️ Sarah's Availability")
    st.info("You are viewing Sarah's live schedule via ShiftLife Web Link.")
    
    # CHECK MEMORY FIRST
    if st.session_state['roster_data'] is not None:
        df = st.session_state['roster_data']
        
        st.subheader("Next Green Days (Free)")
        green_days = df[df['Traffic Light'] == "🟢 Free"]
        
        if not green_days.empty:
            for index, row in green_days.iterrows():
                st.success(f"**{row['Date']}** | ✅ FREE FOR DINNER/GYM")
        else:
            st.warning("No free days found in this batch.")
    else:
        st.error("No schedule has been published yet.")
        
    st.markdown("---")
    if st.button("⬅️ (Demo: Go Back to App)"):
        st.query_params["mode"] = "nurse"
        st.rerun()

# ==========================================
# VIEW 2: SARAH'S APP (Nurse Dashboard)
# ==========================================
else:
    st.title("ShiftLife 🏥")
    st.caption("Nurse Dashboard")
    
    # 1. INPUT (With Persistence Check)
    # We only show the uploader if we don't have data yet, OR to allow re-upload
    uploaded_file = st.file_uploader("📸 Snap/Upload Roster Photo", type=['png', 'jpg', 'jpeg'])

    # IF NEW FILE UPLOADED -> PROCESS IT
    if uploaded_file is not None:
        # Create Dummy Data (Simulating AI)
        data = {
            "Date": [
                (datetime.now() + timedelta(days=0)).strftime('%Y-%m-%d'),
                (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
                (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'),
            ],
            "Shift Code": ["D", "D", "N", "N", "OFF"] # <--- EDIT THIS FOR YOUR STORY
        }
        df = pd.DataFrame(data)
        df[['Status', 'Traffic Light', 'Advice']] = df['Shift Code'].apply(
            lambda x: pd.Series(calculate_life_plan(x))
        )
        
        # SAVE TO MEMORY (Crucial Step)
        st.session_state['roster_data'] = df
        st.toast("Roster Processed & Saved!", icon="💾")

    # 2. DISPLAY SCHEDULE (FROM MEMORY)
    # This runs even if the file uploader is cleared, as long as memory exists
    if st.session_state['roster_data'] is not None:
        df = st.session_state['roster_data']
        
        st.write("---")
        st.subheader("Your Life Plan")
        for index, row in df.iterrows():
            with st.container():
                if "NIGHT" in row['Status']:
                    st.error(f"**{row['Date']}** | {row['Status']}\n\n*{row['Advice']}*")
                elif "DAY" in row['Status']:
                    st.warning(f"**{row['Date']}** | {row['Status']}\n\n*{row['Advice']}*")
                else:
                    st.success(f"**{row['Date']}** | {row['Status']}\n\n*{row['Advice']}*")
                st.write("") 

        st.divider()

        # 3. MAGIC LINK
        st.header("🔗 Relationship Saver")
        st.write("Mark doesn't need to download the app. Send him this web link:")
        
        if st.button("Simulate Mark Clicking the Link 🚀"):
            st.query_params["mode"] = "partner"
            st.rerun()
            
    else:
        st.info("👆 Upload your roster to generate your sleep schedule.")
