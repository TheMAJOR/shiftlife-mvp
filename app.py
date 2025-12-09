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

# --- 3. DYNAMIC STYLING (OUTLINE & HIGH CONTRAST) ---
def apply_theme():
    if st.session_state['dark_mode']:
        # NIGHT MODE (Subtle Borders)
        bg_color = "#0E1117"
        sec_bg_color = "#262730"
        text_color = "#FAFAFA"
        btn_bg = "#262730"
        btn_text = "#FAFAFA"
        border_style = "1px solid #444" # Thin grey border for night
        
        # Uploader (Night)
        uploader_css = f"""
        div[data-testid="stFileUploader"] section {{ background-color: {sec_bg_color} !important; }}
        div[data-testid="stFileUploader"] button {{ 
            background-color: {sec_bg_color} !important; 
            color: {text_color} !important; 
            border: {border_style} !important; 
        }}
        div[data-testid="stFileUploader"] span, div[data-testid="stFileUploader"] small, div[data-testid="stFileUploader"] div {{
            color: {text_color} !important;
        }}
        """
        
    else:
        # DAY MODE (HIGH CONTRAST OUTLINES)
        bg_color = "#FFFFFF"
        sec_bg_color = "#F0F2F6"
        text_color = "#000000"
        btn_bg = "#FFFFFF"
        btn_text = "#000000"
        border_style = "2px solid #000000" # THICK BLACK BORDER for visibility
        
        # Uploader (Day - With Outline)
        uploader_css = f"""
        div[data-testid="stFileUploader"] section {{ background-color: #F0F2F6 !important; }}
        div[data-testid="stFileUploader"] button {{ 
            background-color: #FFFFFF !important; 
            color: #000000 !important; 
            border: {border_style} !important; 
            font-weight: bold !important;
        }}
        div[data-testid="stFileUploader"] span, div[data-testid="stFileUploader"] small, div[data-testid="stFileUploader"] div {{
            color: #000000 !important;
        }}
        """

    # THE MASTER CSS BLOCK
    css = f"""
    <style>
    /* Main Background */
    .stApp {{ background-color: {bg_color} !important; }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{ background-color: {sec_bg_color} !important; }}
    
    /* TEXT - Force High Contrast */
    h1, h2, h3, h4, h5, h6, p, li, span, div, label {{ color: {text_color} !important; }}
    
    /* BUTTONS - WITH OUTLINE */
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: {border_style} !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }}
    
    /* BUTTON HOVER EFFECT */
    div.stButton > button:hover {{
        border-color: {text_color} !important;
        color: {bg_color} !important;
        background-color: {text_color} !important; /* Invert colors on hover */
    }}

    /* CARDS */
    div[data-testid="stExpander"] {{ 
        background-color: {sec_bg_color} !important; 
        border: {border_style} !important; 
        color: {text_color} !important;
    }}
    div[data-testid="stContainer"] {{
        background-color: {sec_bg_color};
        border: 1px solid #CCCCCC;
        border-radius: 10px;
        padding: 15px;
    }}
    
    /* TOGGLE SWITCH TEXT FIX */
    div[data-testid="stToggle"] label p {{
        color: {text_color} !important;
        font-weight: 900 !important; /* Extra Bold */
    }}
    
    /* INJECT UPLOADER CSS */
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
        
        # HERO CARD
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
        
        # UPCOMING SCHEDULE
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
    # --- TOGGLE BUTTON ---
    c1, c2 = st.columns([4, 1])
    with c1:
        st.title("ShiftLife 🏥")
    with c2:
        # Dynamic Label for the toggle
        label_text = "🌙 Night" if st.session_state['dark_mode'] else "☀️ Day"
        is_dark = st.toggle(label_text, value=st.session_state['dark_mode'])
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
        
        # 30-DAY CALENDAR
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
