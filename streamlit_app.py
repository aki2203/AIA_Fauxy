import streamlit as st
import requests
import time
import os

# ================= CONFIG =================

API_URL = os.getenv("API_URL", "http://localhost:5000/satire")

st.set_page_config(
    page_title="Fauxy – Agentic Satirical News",
    page_icon="🤡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= STYLES =================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#5f2c82 0%,#49a09d 100%);
}

/* glass card */
.glass-card{
background: rgba(255,255,255,0.08);
backdrop-filter: blur(10px);
border-radius:20px;
padding:25px;
margin-bottom:25px;
border:1px solid rgba(255,255,255,0.2);
}

/* tags */
.premium-tag{
display:inline-block;
padding:6px 14px;
margin:4px;
border-radius:30px;
font-size:12px;
font-weight:600;
background:linear-gradient(145deg,#667eea,#764ba2);
color:white;
}

/* input */
.stTextInput input{
border-radius:12px !important;
border:1px solid rgba(255,255,255,0.25) !important;
padding:12px 14px !important;
background:rgba(255,255,255,0.15) !important;
color:white !important;
}

/* button */
.stButton > button{
background:linear-gradient(135deg,#7f5af0,#2cb67d) !important;
color:white !important;
border:none !important;
padding:12px 28px !important;
border-radius:12px !important;
font-weight:600 !important;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================

st.markdown("""
<div style="text-align:center;padding:40px 0;">

<h1 style="
font-size:52px;
font-weight:700;
background:linear-gradient(90deg,#ffffff,#d4d4ff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:10px;
">
🤡 Fauxy
</h1>

<p style="font-size:18px;color:white;opacity:0.9;">
Agentic, Safe & Explainable AI for Indian Satirical News
</p>

<div style="display:flex;justify-content:center;gap:10px;">
<span class="premium-tag">⚡ Agentic AI</span>
<span class="premium-tag">🛡 Safety</span>
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

# ================= HELPER FUNCTIONS =================

def satire_breakdown(text):

    points = []

    if "!" in text:
        points.append("🎯 Uses exaggeration")

    points.append("💭 Uses irony")

    return points


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
        resp.raise_for_status()
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

    tags_html = ""

    for tag in ["Satire", "Observational", "Exaggeration", "🇮🇳 India"]:
        tags_html += f'<span class="premium-tag">{tag}</span>'

    st.markdown(tags_html, unsafe_allow_html=True)

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
    """, unsafe_allow_html=True)

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
<div style="text-align:center;padding:30px;color:white;opacity:0.9;">

<p>
⚡ Agentic Planning • 🔍 Research • 🛡 Safety • 📊 Evaluation
</p>

<p style="font-size:14px;">
Built with Fauxy Agentic System | Flask + Streamlit
</p>

</div>
""", unsafe_allow_html=True)
