import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & UI POLISH ---
st.set_page_config(page_title="ShiftLife", page_icon="🏥", layout="centered")

# Hide Streamlit Branding (Hamburger menu, footer)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 2. INITIALIZE MEMORY ---
if 'roster_data' not in st.session_state:
    st.session_state['roster_data'] = None

# --- 3. CORE LOGIC ---
def calculate_life_plan(shift_code):
    if shift_code == "N":
        return "⛔ NIGHT SHIFT", "🔴 Busy", "Recovery Mode: Sleep 8am-3pm."
    elif shift_code == "D":
        return "🏥 DAY SHIFT", "🔴 Busy", "Prep Mode: Meal prep tonight."
    elif shift_code == "OFF":
        return "✅ OFF DUTY", "🟢 Free", "Golden Window: Date Night or Gym!"
    else:
        return "Unknown", "⚪ Check", "Waiting for input..."

# --- 4. CHECK URL MODE (Nurse vs Partner) ---
query_params = st.query_params
mode = query_params.get("mode", "nurse") 

# ==========================================
# VIEW 1: MARK'S VIEW (Partner Link)
# ==========================================
if mode == "partner":
    st.title("❤️ Sarah's Availability")
    st.info("You are viewing Sarah's live schedule via ShiftLife Web Link.")
    
    if st.session_state['roster_data'] is not None:
        df = st.session_state['roster_data']
        
        st.subheader("Next Green Days (Free)")
        green_days = df[df['Traffic Light'] == "🟢 Free"]
        
        if not green_days.empty:
            for index, row in green_days.iterrows():
                # Clean Green Card for Partner
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
    # Header with Logo Placeholder
    c1, c2 = st.columns([1, 5])
    with c1:
        st.markdown("### 🏥") # You can replace this with st.image("logo.png")
    with c2:
        st.title("ShiftLife")
    
    st.caption("Nurse Dashboard | 30-Day Planner")
    
    # INPUT SECTION
    uploaded_file = st.file_uploader("📸 Snap/Upload Roster Photo", type=['png', 'jpg', 'jpeg'])

    # PROCESS UPLOAD
    if uploaded_file is not None:
        # --- THE 30-DAY GENERATOR ---
        # 1. Define the Roster Pattern (The "Rhythm")
        # Change this list to match the story you want to tell.
        shift_pattern = ["D", "D", "N", "N", "OFF", "OFF", "OFF", "OFF"]

        # 2. Generate 30 Days of Data
        dates = []
        codes = []
        start_date = datetime.now()

        for i in range(30):
            current_date = start_date + timedelta(days=i)
            dates.append(current_date.strftime('%Y-%m-%d'))
            
            # Loop the pattern
            code_index = i % len(shift_pattern)
            codes.append(shift_pattern[code_index])

        # 3. Build DataFrame
        data = {
            "Date": dates,
            "Shift Code": codes
        }
        df = pd.DataFrame(data)
        df[['Status', 'Traffic Light', 'Advice']] = df['Shift Code'].apply(
            lambda x: pd.Series(calculate_life_plan(x))
        )
        
        # SAVE TO MEMORY
        st.session_state['roster_data'] = df
        st.toast("30-Day Roster Generated!", icon="📅")

    # DISPLAY SCHEDULE
    if st.session_state['roster_data'] is not None:
        df = st.session_state['roster_data']
        
        st.write("---")
        st.subheader("Your Life Plan (Next 30 Days)")
        
        # --- IMPROVED CARD DISPLAY (Clean List) ---
        for index, row in df.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"**{row['Date']}**")
                    if "NIGHT" in row['Status']:
                        st.markdown("⛔ **NIGHT**")
                    elif "DAY" in row['Status']:
                        st.markdown("🏥 **DAY**")
                    else:
                        st.markdown("🟢 **OFF**")
                with c2:
                    st.caption("Protocol:")
                    st.info(f"{row['Advice']}")
            st.divider()

        # PARTNER LINK SECTION
        st.header("🔗 Relationship Saver")
        st.write("Mark doesn't need to download the app. Send him this web link:")
        
        if st.button("Simulate Mark Clicking the Link 🚀"):
            st.query_params["mode"] = "partner"
            st.rerun()
            
    else:
        st.info("👆 Upload your roster to generate your monthly plan.")
