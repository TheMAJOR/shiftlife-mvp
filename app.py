import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & UI POLISH ---
st.set_page_config(page_title="ShiftLife", page_icon="🏥", layout="centered")

# Hide Streamlit Branding
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

# --- 3. CORE LOGIC (THE UPGRADED BRAIN) ---
def get_daily_schedule(shift_code):
    """
    Returns specific time blocks for Work, Sleep, and Leisure based on shift type.
    """
    if shift_code == "N":
        return {
            "Status": "⛔ NIGHT SHIFT",
            "Color": "red",
            "Work": "19:00 - 07:00 (Next Day)",
            "Sleep": "08:00 AM - 03:00 PM (Recovery)",
            "Leisure": "16:00 - 18:00",
            "Activity": "🧘 Light Yoga or Meal Prep"
        }
    elif shift_code == "D":
        return {
            "Status": "🏥 DAY SHIFT",
            "Color": "orange",
            "Work": "07:00 - 19:00",
            "Sleep": "22:00 - 06:00 (Pre-shift)",
            "Leisure": "19:30 - 21:00",
            "Activity": "📺 Netflix (Wind Down)"
        }
    elif shift_code == "OFF":
        return {
            "Status": "✅ OFF DUTY",
            "Color": "green",
            "Work": "None",
            "Sleep": "23:00 - 08:00 (Natural)",
            "Leisure": "10:00 - 12:00 & 18:00 - 21:00",
            "Activity": "🏋️ Gym, Date Night, or Hiking"
        }
    else:
        return {
            "Status": "Unknown", "Color": "gray", "Work": "-", "Sleep": "-", "Leisure": "-", "Activity": "-"
        }

# --- 4. CHECK URL MODE ---
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
        # Filter for OFF days
        green_days = df[df['Shift Code'] == "OFF"]
        
        if not green_days.empty:
            for index, row in green_days.iterrows():
                # Clean Green Card for Partner
                st.success(f"**{row['Date']}** | ✅ FREE ALL DAY")
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
    c1, c2 = st.columns([1, 5])
    with c1:
        st.markdown("### 🏥")
    with c2:
        st.title("ShiftLife")
    
    st.caption("Nurse Dashboard | 30-Day Planner")
    
    # INPUT SECTION
    uploaded_file = st.file_uploader("📸 Snap/Upload Roster Photo", type=['png', 'jpg', 'jpeg'])

    # PROCESS UPLOAD
    if uploaded_file is not None:
        # --- THE 30-DAY GENERATOR ---
        shift_pattern = ["D", "D", "N", "N", "OFF", "OFF", "OFF", "OFF"]

        dates = []
        codes = []
        start_date = datetime.now()

        for i in range(30):
            current_date = start_date + timedelta(days=i)
            dates.append(current_date.strftime('%Y-%m-%d'))
            code_index = i % len(shift_pattern)
            codes.append(shift_pattern[code_index])

        # Build DataFrame
        data = { "Date": dates, "Shift Code": codes }
        df = pd.DataFrame(data)
        
        # Apply the Detailed Schedule Logic
        # We apply the function and expand the result into separate columns
        schedule_data = df['Shift Code'].apply(lambda x: pd.Series(get_daily_schedule(x)))
        df = pd.concat([df, schedule_data], axis=1)
        
        # SAVE TO MEMORY
        st.session_state['roster_data'] = df
        st.toast("Detailed Schedule Generated!", icon="📅")

    # DISPLAY SCHEDULE (DETAILED CARDS)
    if st.session_state['roster_data'] is not None:
        df = st.session_state['roster_data']
        
        st.write("---")
        st.subheader("Your Life Plan (Next 30 Days)")
        
        for index, row in df.iterrows():
            with st.container():
                # 1. THE HEADER (Color Coded)
                header_text = f"**{row['Date']}** | {row['Status']}"
                if row['Color'] == "red":
                    st.error(header_text)
                elif row['Color'] == "orange":
                    st.warning(header_text)
                else:
                    st.success(header_text)
                
                # 2. THE DETAILED SCHEDULE (Inside the card context)
                # We use columns to make it look like a dashboard
                c1, c2 = st.columns(2)
                
                with c1:
                    st.markdown("**💼 Work Shift**")
                    st.caption(f"{row['Work']}")
                    
                    st.markdown("**🛏️ Sleep Schedule**")
                    st.markdown(f"`{row['Sleep']}`")
                
                with c2:
                    st.markdown("**🎉 Golden Window**")
                    st.caption(f"{row['Leisure']}")
                    
                    st.markdown("**💡 Suggested Activity**")
                    st.info(f"{row['Activity']}")
            
            # Divider between days
            st.divider()

        # PARTNER LINK
        st.header("🔗 Relationship Saver")
        st.write("Mark doesn't need to download the app. Send him this web link:")
        
        if st.button("Simulate Mark Clicking the Link 🚀"):
            st.query_params["mode"] = "partner"
            st.rerun()
            
    else:
        st.info("👆 Upload your roster to generate your monthly plan.")
