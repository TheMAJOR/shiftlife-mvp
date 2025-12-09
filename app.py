import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="ShiftLife", page_icon="🏥", layout="centered")

# --- 2. INITIALIZE MEMORY ---
if 'roster_data' not in st.session_state:
    st.session_state['roster_data'] = None
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = True

# --- 3. DYNAMIC STYLING (DAY/NIGHT MODE) ---
def apply_theme():
    if st.session_state['dark_mode']:
        # NIGHT MODE CSS (Deep Blue/Black)
        theme_style = """
        <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        .stMarkdown, .stText, h1, h2, h3 { color: #FAFAFA !important; }
        div[data-testid="stContainer"] { background-color: #262730; border-radius: 10px; padding: 15px; border: 1px solid #444; }
        </style>
        """
    else:
        # DAY MODE CSS (Clean White/Gray)
        theme_style = """
        <style>
        .stApp { background-color: #FFFFFF; color: #000000; }
        .stMarkdown, .stText, h1, h2, h3 { color: #000000 !important; }
        div[data-testid="stContainer"] { background-color: #F0F2F6; border-radius: 10px; padding: 15px; border: 1px solid #CCC; }
        </style>
        """
    
    # Hide Streamlit Branding (Standard Polish)
    hide_st = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(theme_style + hide_st, unsafe_allow_html=True)

# Apply the theme at the start of every run
apply_theme()

# --- 4. CORE LOGIC (CIRCADIAN RHYTHM UPDATE) ---
def get_daily_schedule(shift_code):
    if shift_code == "N":
        return {
            "Status": "⛔ NIGHT SHIFT",
            "Color": "red",
            "Work": "19:00 - 07:00 (Next Morning)",
            "Sleep": "😴 08:00 AM - 11:00 AM (Core Sleep)",
            "BioHack": "☀️ 11:00 AM: WAKE UP & GET SUNLIGHT. (Reset Clock)",
            "Leisure": "16:00 - 18:00 (Before Work)",
            "Activity": "🧘 Light Yoga or Meal Prep"
        }
    elif shift_code == "D":
        return {
            "Status": "🏥 DAY SHIFT",
            "Color": "orange",
            "Work": "07:00 - 19:00",
            "Sleep": "😴 22:00 - 06:00 (Pre-shift)",
            "BioHack": "🥗 Eat high protein at 12:00 PM. No caffeine after 2 PM.",
            "Leisure": "19:30 - 21:00",
            "Activity": "📺 Netflix (Wind Down)"
        }
    elif shift_code == "OFF":
        return {
            "Status": "✅ OFF DUTY",
            "Color": "green",
            "Work": "None",
            "Sleep": "😴 23:00 - 08:00 (Natural)",
            "BioHack": "🏃‍♀️ Cardio Zone 2 to flush cortisol.",
            "Leisure": "All Day",
            "Activity": "🏋️ Gym, Date Night, or Hiking"
        }
    else:
        return {
            "Status": "Unknown", "Color": "gray", "Work": "-", "Sleep": "-", "BioHack": "-", "Leisure": "-", "Activity": "-"
        }

# --- 5. CHECK URL MODE ---
query_params = st.query_params
mode = query_params.get("mode", "nurse") 

# ==========================================
# VIEW 1: MARK'S VIEW (Partner Link)
# ==========================================
if mode == "partner":
    st.title("❤️ Sarah's Availability")
    
    if st.session_state['roster_data'] is not None:
        df = st.session_state['roster_data']
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # --- SECTION 1: TODAY'S STATUS (SEPARATE PAGE FEEL) ---
        today_row = df[df['Date'] == today_str]
        
        if not today_row.empty:
            row = today_row.iloc[0] # Get the single row
            st.header("📅 Today's Status")
            
            # Big Hero Card for Today
            with st.container():
                st.markdown(f"### {today_str}")
                if row['Shift Code'] == "OFF":
                    st.success("✅ **SARAH IS FREE ALL DAY**")
                    st.caption("Suggestion: Go out for dinner!")
                elif row['Shift Code'] == "D":
                    st.warning("🏥 **SARAH IS WORKING (DAY)**")
                    st.info(f"🕒 She is free between: **{row['Leisure']}**")
                else:
                    st.error("⛔ **SARAH IS WORKING (NIGHT)**")
                    st.info(f"🕒 She is free between: **{row['Leisure']}**")
        else:
            st.info("Today's data is not uploaded.")

        st.divider()
        
        # --- SECTION 2: UPCOMING SCHEDULE ---
        st.subheader("Upcoming Free Days")
        green_days = df[(df['Shift Code'] == "OFF") & (df['Date'] > today_str)]
        
        if not green_days.empty:
            for index, row in green_days.iterrows():
                st.success(f"**{row['Date']}** | ✅ FREE ALL DAY")
        else:
            st.caption("No upcoming free days found in this roster.")
            
    else:
        st.error("No schedule has been published yet.")
        
    st.markdown("---")
    if st.button("⬅️ (Demo: Back to App)"):
        st.query_params["mode"] = "nurse"
        st.rerun()

# ==========================================
# VIEW 2: SARAH'S APP (Nurse Dashboard)
# ==========================================
else:
    # Sidebar for Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        # DAY / NIGHT TOGGLE
        is_dark = st.toggle("🌙 Night Mode", value=st.session_state['dark_mode'])
        if is_dark != st.session_state['dark_mode']:
            st.session_state['dark_mode'] = is_dark
            st.rerun()
            
    c1, c2 = st.columns([1, 5])
    with c1:
        st.markdown("### 🏥")
    with c2:
        st.title("ShiftLife")
    
    # INPUT SECTION
    if st.session_state['roster_data'] is None:
        uploaded_file = st.file_uploader("📸 Snap/Upload Roster Photo", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            # GENERATE 30 DAYS
            shift_pattern = ["D", "D", "N", "N", "OFF", "OFF", "OFF", "OFF"]
            dates = []
            codes = []
            start_date = datetime.now()

            for i in range(30):
                current_date = start_date + timedelta(days=i)
                dates.append(current_date.strftime('%Y-%m-%d'))
                code_index = i % len(shift_pattern)
                codes.append(shift_pattern[code_index])

            data = { "Date": dates, "Shift Code": codes }
            df = pd.DataFrame(data)
            schedule_data = df['Shift Code'].apply(lambda x: pd.Series(get_daily_schedule(x)))
            df = pd.concat([df, schedule_data], axis=1)
            
            st.session_state['roster_data'] = df
            st.rerun() # Refresh to show the dashboard immediately

    # DASHBOARD DISPLAY
    if st.session_state['roster_data'] is not None:
        df = st.session_state['roster_data']
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # --- SECTION 1: TODAY'S ACTION PLAN (SEPARATE PAGE FEEL) ---
        today_row = df[df['Date'] == today_str]
        
        if not today_row.empty:
            row = today_row.iloc[0]
            st.markdown("## ⚡ Today's Action Plan")
            
            # THE "NOW" CARD
            with st.container():
                # Dynamic Header Color based on Shift
                header_md = f"### {row['Date']} | {row['Status']}"
                if row['Color'] == "red":
                    st.error(header_md)
                elif row['Color'] == "orange":
                    st.warning(header_md)
                else:
                    st.success(header_md)

                # CIRCADIAN PROTOCOL (The "Science" Part)
                st.markdown("#### 🧬 Circadian Protocol")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**🛏️ Sleep**")
                    st.info(f"{row['Sleep']}")
                with c2:
                    st.markdown("**🧪 Bio-Hack**")
                    st.warning(f"{row['BioHack']}")
                
                # SCHEDULE
                st.markdown("#### 📅 Schedule")
                c3, c4 = st.columns(2)
                with c3:
                    st.caption(f"**Work:** {row['Work']}")
                with c4:
                    st.caption(f"**Leisure:** {row['Leisure']}")
                    st.markdown(f"**Activity:** {row['Activity']}")
                    
        else:
            st.info("Roster expired. Please upload new photo.")

        st.divider()
        
        # --- SECTION 2: FULL MONTH VIEW ---
        with st.expander("📅 View Full 30-Day Calendar"):
            for index, row in df.iterrows():
                # Skip today (since we showed it above)
                if row['Date'] == today_str:
                    continue
                    
                with st.container():
                    st.markdown(f"**{row['Date']}** | {row['Status']}")
                    c_a, c_b = st.columns(2)
                    with c_a:
                        st.caption(f"Sleep: {row['Sleep']}")
                    with c_b:
                        st.caption(f"Free: {row['Leisure']}")
                st.write("") #
