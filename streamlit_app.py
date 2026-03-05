import streamlit as st
import requests
import time
import random
from datetime import datetime

# ================= CONFIG =================
API_URL = os.getenv("API_URL", "http://localhost:5000/satire")

st.set_page_config(
    page_title="Fauxy – Agentic Satirical News",
    page_icon="🤡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= ADVANCED STYLES =================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
font-family: 'Inter', sans-serif;
color: white;
}

/* Gradient Background */
.stApp {
background: linear-gradient(135deg,#5f2c82 0%,#49a09d 100%);
}

/* AI Glow */
.stApp::before{
content:"";
position:fixed;
top:-200px;
left:-200px;
width:600px;
height:600px;
background:radial-gradient(circle,rgba(255,255,255,0.15),transparent 70%);
filter:blur(120px);
z-index:-1;
}

.stApp::after{
content:"";
position:fixed;
bottom:-200px;
right:-200px;
width:600px;
height:600px;
background:radial-gradient(circle,rgba(120,100,255,0.25),transparent 70%);
filter:blur(140px);
z-index:-1;
}

/* Glass cards */
.glass-card{
background:rgba(255,255,255,0.08);
backdrop-filter:blur(12px);
border-radius:20px;
padding:25px;
margin-bottom:25px;
border:1px solid rgba(255,255,255,0.2);
box-shadow:0 8px 32px rgba(31,38,135,0.15);
}

.glass-card:hover{
transform:translateY(-6px);
transition:0.35s;
box-shadow:0 20px 45px rgba(0,0,0,0.25);
}

/* Input */
.stTextInput input{
border-radius:14px !important;
border:1px solid rgba(255,255,255,0.25) !important;
padding:14px 16px !important;
background:rgba(255,255,255,0.12) !important;
color:white !important;
}

/* Select */
.stSelectbox div{
color:white !important;
}

/* Buttons */
.stButton > button{
background:linear-gradient(135deg,#7f5af0,#2cb67d) !important;
color:white !important;
border:none !important;
padding:14px 30px !important;
font-size:16px !important;
font-weight:600 !important;
border-radius:12px !important;
}

.stButton > button:hover{
transform:scale(1.05);
}

/* Tags */
.premium-tag{
display:inline-block;
padding:6px 14px;
margin:5px;
border-radius:30px;
font-size:12px;
font-weight:600;
background:linear-gradient(145deg,#667eea,#764ba2);
color:white;
}

.premium-tag:hover{
transform:scale(1.05);
}

/* Divider */
hr{
height:1px;
border:none;
background:linear-gradient(90deg,transparent,rgba(255,255,255,0.3),transparent);
margin:40px 0;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div style="text-align:center;padding:50px 0;">

<h1 style="
font-size:56px;
font-weight:700;
background:linear-gradient(90deg,#ffffff,#cfcfff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:10px;
">
🤡 Fauxy
</h1>

<p style="
font-size:20px;
color:rgba(255,255,255,0.9);
margin-bottom:18px;
">
Agentic, Safe & Explainable AI for Indian Satirical News
</p>

<div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
<span class="premium-tag">⚡ Agentic AI</span>
<span class="premium-tag">🛡 Safety First</span>
<span class="premium-tag">🔍 Explainable</span>
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ================= INPUT =================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

topic = st.text_input(
"📰 Enter a news topic",
placeholder="Indian Budget, Elections, Bureaucracy..."
)

tone = st.selectbox(
"🎭 Choose satire tone",
[
"auto",
"social media meme style",
"political parody",
"dry sarcasm",
"subtle irony"
]
)

compare_mode = st.checkbox("🧪 A/B Test")

generate_btn = st.button("🚀 Generate Fauxy News", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ================= HELPERS =================
def satire_breakdown(text):
    points = []

    if "!" in text:
        points.append("🎯 Uses exaggeration")

    points.append("💭 Irony contrast")

    return points

# ================= MAIN LOGIC =================
# ================= MAIN LOGIC =================
if generate_btn:

    if not topic:
        st.error("Please enter a topic")
        st.stop()

    progress_bar = st.progress(0)
    status = st.empty()

    for i in range(100):

        if i < 30:
            status.markdown("🧠 Planning satire...")
        elif i < 60:
            status.markdown("🔍 Researching context...")
        elif i < 90:
            status.markdown("✍️ Generating satire...")
        else:
            status.markdown("✅ Evaluating output...")

        progress_bar.progress(i + 1)
        time.sleep(0.01)

    try:
        resp = requests.post(API_URL, json={"topic": topic, "tone": tone})
        data = resp.json()
    except Exception as e:
        st.error(f"Backend error: {e}")
        st.stop()

    progress_bar.empty()
    status.empty()

    satire = data["satire"]

# ================= OUTPUT =================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown("### 😂 Generated Satire")

tags_html=""
for tag in ["Satire","Observational","Exaggeration","🇮🇳 India"]:
tags_html+=f'<span class="premium-tag">{tag}</span>'

st.markdown(tags_html,unsafe_allow_html=True)

st.markdown(f"""
<div style="
background:linear-gradient(145deg,#fff8f0,#fff2e5);
padding:25px;
border-radius:18px;
color:#333;
font-size:18px;
line-height:1.8;
">
{satire}
</div>
""",unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ================= HUMOR ANALYSIS =================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown("### 🧩 Humor Analysis")

for point in satire_breakdown(satire):
st.markdown(f"- {point}")

st.markdown('</div>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("---")

st.markdown("""
<div style="text-align:center;padding:30px 0;color:white;opacity:0.9">

<p>
⚡ Agentic Planning • 🔍 Research • 🛡 Safety • 📊 Evaluation
</p>

<p style="font-size:14px">
Built with Fauxy Agentic System | Flask + Streamlit
</p>

</div>
""", unsafe_allow_html=True)

# ================= SESSION =================
if 'generated' not in st.session_state:
st.session_state.generated=False

if generate_btn:
st.session_state.generated=True
st.balloons()
