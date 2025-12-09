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

# --- 3. DYNAMIC STYLING (THE PRO FIX) ---
def apply_theme():
    if st.session_state['dark_mode']:
        # NIGHT MODE COLORS
        bg_color = "#0E1117"
        sec_bg_color = "#262730"
        text_color = "#FAFAFA"
        border_color = "#444"
        
        # Specific Fix for Night Mode Uploader
        uploader_css = """
        div[data-testid="stFileUploader"] section { background-color: #262730 !important; }
        div[data-testid="stFileUploader"] button { color: #FAFAFA !important; border-color: #FAFAFA !important; }
        """
    else:
        # DAY MODE COLORS
        bg_color = "#FFFFFF"
        sec_bg_color = "#F0F2F6"
        text_color = "#000000"
        border_color = "#CCCCCC"
        
        # Specific Fix for Day Mode Uploader (Forces it White/Gray)
        uploader_css = """
        div[data-testid="stFileUploader"] section { background-color: #F0F2F6 !important; }
        div[data-testid="stFileUploader"] button { color: #000000 !important; border-color: #000000 !important; }
        span, p, div, label { color: #000000 !important; } 
        """
    
    # THE MASTER CSS BLOCK
    css = f"""
    <style>
    /* Main Background */
    .stApp {{ background-color: {bg_color} !important; }}
    
    /* Sidebar Background */
    section[data-testid="stSidebar"] {{ background-color: {sec_bg_color} !important; }}
    
    /* Cards / Expanders / Containers */
    div[data-testid="stExpander"] {{ 
        background-color: {sec_bg_color} !important; 
        border: 1px solid {border_color} !important; 
        color: {text_color} !important;
    }}
    div[data-testid="stContainer"] {{
        background-color: {sec_bg_color};
        border: 1px solid {border_color};
        border-radius: 10px;
        padding: 15px;
    }}
    
    /* Text Coloring */
    h1, h2, h3, h4, h5, h6, p, li, span, div {{ color: {text_color} !important; }}
    
    /* Input Labels */
    label {{ color: {text_color} !important; }}
    
    /* Uploader Specifics */
    {uploader_css}
    
    /* Hide Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

apply_theme()

# --- 4. CORE LOGIC ---
def get_daily_schedule(shift_code):
    if shift_code == "N":
        return {
            "Status": "⛔ NIGHT SHIFT",
            "Color": "red",
            "Emoji": "🔴",
            "Work": "19:00 - 07:00 (Next Morning)",
            "Sleep": "😴 08:00 AM - 11:00 AM (Core Sleep)",
            "BioHack": "☀️ 11:00 AM: WAKE UP & GET SUNLIGHT.",
            "Leisure": "16:00 - 18:00 (Before Work)",
            "Activity": "🧘 Light Yoga or Meal Prep"
        }
    elif shift_code == "D":
        return {
            "Status": "🏥 DAY SHIFT",
            "Color": "orange",
            "Emoji": "🟠",
            "Work": "07:00 - 19:00",
            "Sleep": "😴 22:00 - 06:00 (Pre-shift)",
            "BioHack": "🥗 Eat high protein at 12:00 PM.",
            "Leisure": "19:30 - 21:00",
            "Activity": "📺 Netflix (Wind Down)"
        }
    elif shift_code == "OFF":
        return {
            "Status": "✅ OFF DUTY",
            "Color": "green",
            "Emoji": "🟢",
            "Work": "None",
            "Sleep": "😴 23:00 - 08:00 (Natural)",
            "BioHack": "🏃‍♀️ Cardio Zone 2 to flush cortisol.",
            "Leisure": "All Day",
            "Activity": "🏋️ Gym, Date Night, or Hiking"
        }
    else:
        return {
            "Status": "Unknown", "Color": "gray", "Emoji": "⚪", "Work": "-", "Sleep": "-", "BioHack": "-", "Leisure": "-", "Activity": "-"
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
        
        # HERO CARD (TODAY)
        today_row = df[df['Date'] == today_str]
        if not today_row.empty:
            row = today_row.iloc[0]
            st.header("📅 Today's Status")
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
        
        # FULL UPCOMING SCHEDULE
        st.subheader("Upcoming Schedule")
        future_days = df[df['Date'] > today_str]
        if not future_days.empty:
            for index, row in future_days.iterrows():
                if row['Shift Code'] == "OFF":
                    st.success(f"**{row['Date']}** | ✅ FREE ALL DAY")
                else:
                    msg = f"**{row['Date']}** | {row['Emoji']} Working. Free: **{row['Leisure']}**"
                    st.info(msg)
        else:
            st.caption("No upcoming schedule found.")
            
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
    # --- TOGGLE BUTTON (MOVED TO TOP FOR MOBILE ACCESS) ---
    # We move the toggle out of the sidebar to the top right so it's always visible on mobile
    c1, c2 = st.columns([4, 1])
    with c1:
        st.title("ShiftLife 🏥")
    with c2:
        # Mini Toggle Switch
        is_dark = st.toggle("🌙", value=st.session_state['dark_mode'])
        if is_dark != st.session_state['dark_mode']:
            st.session_state['dark_mode'] = is_dark
            st.rerun()

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
            st.rerun() 

    # DASHBOARD DISPLAY
    if st.session_state['roster_data'] is not None:
        df = st.session_state['roster_data']
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # TODAY (HERO)
        today_row = df[df['Date'] == today_str]
        
        if not today_row.empty:
            row = today_row.iloc[0]
            st.markdown("## ⚡ Today's Action Plan")
            
            with st.container():
                header_md = f"### {row['Date']} | {row['Status']}"
                if row['Color'] == "red":
                    st.error(header_md)
                elif row['Color'] == "orange":
                    st.warning(header_md)
                else:
                    st.success(header_md)

                st.markdown("#### 🧬 Circadian Protocol")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**🛏️ Sleep**")
                    st.info(f"{row['Sleep']}")
                with c2:
                    st.markdown("**🧪 Bio-Hack**")
                    st.warning(f"{row['BioHack']}")
                
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
        
        # 30-DAY CALENDAR (EXPANDABLE)
        st.subheader("📅 Full 30-Day Calendar")
        
        for index, row in df.iterrows():
            if row['Date'] == today_str:
                continue
            
            label = f"{row['Date']} | {row['Emoji']} {row['Status']}"
            with st.expander(label):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**🛏️ Sleep Protocol**")
                    st.info(row['Sleep'])
                    st.markdown("**💼 Work Hours**")
                    st.caption(row['Work'])
                with c2:
                    st.markdown("**🧪 Bio-Hack**")
                    st.warning(row['BioHack'])
                    st.markdown("**🎉 Golden Window**")
                    st.caption(f"{row['Leisure']} ({row['Activity']})")

        # PARTNER LINK
        st.divider()
        st.header("🔗 Relationship Saver")
        st.write("Mark doesn't need to download the app. Send him this web link:")
        
        if st.button("Simulate Mark Clicking the Link 🚀"):
            st.query_params["mode"] = "partner"
            st.rerun()
