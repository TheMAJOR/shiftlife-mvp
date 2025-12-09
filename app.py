import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ShiftLife", page_icon="🏥", layout="centered")

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

# --- CHECK URL MODE (Simulating the Web Link) ---
# We check if the URL has "?mode=partner". If yes, we show Mark's view.
query_params = st.query_params
mode = query_params.get("mode", "nurse") 

# --- DATA GENERATION (Simulated AI) ---
data = {
    "Date": [
        (datetime.now() + timedelta(days=0)).strftime('%Y-%m-%d'),
        (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
        (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
        (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'),
    ],
    "Shift Code": ["D", "D", "N", "N", "OFF"] # <--- EDIT THIS TO CHANGE STORY
}
df = pd.DataFrame(data)
df[['Status', 'Traffic Light', 'Advice']] = df['Shift Code'].apply(
    lambda x: pd.Series(calculate_life_plan(x))
)

# ==========================================
# VIEW 1: MARK'S VIEW (The "Internet Link")
# This is what Mark sees on his browser. No Login. No App.
# ==========================================
if mode == "partner":
    st.title("❤️ Sarah's Availability")
    st.info("You are viewing Sarah's live schedule via ShiftLife Web Link.")
    
    st.subheader("Next Green Days (Free)")
    
    # Filter for GREEN days only
    green_days = df[df['Traffic Light'] == "🟢 Free"]
    
    if not green_days.empty:
        for index, row in green_days.iterrows():
            # Big Green Cards for Mark
            st.success(f"**{row['Date']}** | ✅ FREE FOR DINNER/GYM")
    else:
        st.warning("No free days found in this batch.")
        
    st.markdown("---")
    # Button to go back for your Demo purposes
    if st.button("⬅️ (Demo: Go Back to App)"):
        st.query_params["mode"] = "nurse"
        st.rerun()

# ==========================================
# VIEW 2: SARAH'S APP (The Dashboard)
# ==========================================
else:
    st.title("ShiftLife 🏥")
    st.caption("Nurse Dashboard")
    
    # 1. INPUT
    uploaded_file = st.file_uploader("📸 Snap/Upload Roster Photo", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        st.success("Analysis Complete. Roster sync active.")
        st.divider()
        
        # 2. NURSE SCHEDULE DISPLAY
        st.subheader("Your Life Plan")
        for index, row in df.iterrows():
            with st.container():
                if "NIGHT" in row['Status']:
                    st.error(f"**{row['Date']}** | {row['Status']}\n\n*{row['Advice']}*")
                elif "DAY" in row['Status']:
                    st.warning(f"**{row['Date']}** | {row['Status']}\n\n*{row['Advice']}*")
                else:
                    st.success(f"**{row['Date']}** | {row['Status']}\n\n*{row['Advice']}*")
                st.write("") # Spacer

        st.divider()

        # 3. THE MAGIC LINK GENERATOR
        st.header("🔗 Relationship Saver")
        st.write("Mark doesn't need to download the app. Send him this web link:")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.code("https://shiftlife.app/u/sarah/view?share=true", language="html")
        
        st.markdown("### 👇 Demo Interaction")
        if st.button("Simulate Mark Clicking the Link 🚀"):
            st.toast("Switching to Partner View...", icon="❤️")
            # This line changes the URL mode to 'partner' and reloads the page
            st.query_params["mode"] = "partner"
            st.rerun()