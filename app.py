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

# --- 3. DYNAMIC STYLING (NUCLEAR FIX) ---
def apply_theme():
    if st.session_state['dark_mode']:
        # NIGHT MODE CSS
        theme_style = """
        <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        section[data-testid="stSidebar"] { background-color: #262730; color: #FAFAFA; }
        div[data-testid="stExpander"] { background-color: #262730; border: 1px solid #444; color: #FAFAFA; }
        p, span, h1, h2, h3, div { color: #FAFAFA; }
        </style>
        """
    else:
        # DAY MODE CSS (The Nuclear Option)
        theme_style = """
        <style>
        /* Force Main Background White */
        .stApp { background-color: #FFFFFF !important; }
        
        /* Force Sidebar Light Gray */
        section[data-testid="stSidebar"] { background-color: #F0F2F6 !important; }
        
        /* Force ALL Text Black */
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, li, span, label, div {
            color: #000000 !important;
        }
        
        /* Fix Expander/Cards Background for Day Mode */
        div[data-testid="stExpander"] { 
            background-color: #FFFFFF !important; 
            border: 1px solid #CCC !important; 
            color: #000000 !important;
        }
        
        /* Specific Fix for Metrics/Info Boxes */
        div[data-testid="stMetricValue"] { color: #000000 !important; }
        </style>
        """
    
    hide_st = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(theme_style + hide_st, unsafe_allow_html=True)

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
        
        # --- SECTION 1: TODAY (HERO CARD) ---
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
        
        # --- SECTION 2: FULL UPCOMING SCHEDULE (UPDATED) ---
        st.subheader("Upcoming Schedule")
        
        # Filter for all future dates
        future_days = df[df['Date'] > today_str]
        
        if not future_days.empty:
            for index, row in future_days.iterrows():
                # Logic to determine what to show
                if row['Shift Code'] == "OFF":
                    # Full Free Day
                    st.success(f"**{row['Date']}** | ✅ FREE ALL DAY")
                else:
                    # Working Day - Show Partial Availability
                    # We use a neutral message that highlights the FREE time
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
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
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
            st.rerun() 

    # DASHBOARD DISPLAY
    if st.session_state['roster_data'] is not None:
        df = st.session_state['roster_data']
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # --- SECTION 1: TODAY (HERO) ---
        today_row = df[df['Date'] == today_str]
        
        if not today_row.empty:
            row = today_row.iloc[0]
            st.markdown("## ⚡ Today's Action Plan")
            
            with st.container():
                # HEADER
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
        
        # --- SECTION 2: 30-DAY CALENDAR (CLICKABLE DETAILS) ---
        st.subheader("📅 Full 30-Day Calendar")
        st.caption("Click on any date to see the full Bio-Hack plan.")
        
        for index, row in df.iterrows():
            if row['Date'] == today_str:
                continue
            
            # Use Expander for "Click to see details" functionality
            label = f"{row['Date']} | {row['Emoji']} {row['Status']}"
            with st.expander(label):
                
                # Inside the click, show the full detailed dashboard
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
