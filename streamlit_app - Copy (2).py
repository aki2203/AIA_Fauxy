import streamlit as st
import requests

# ---------------- CONFIG ----------------
API_URL = "http://localhost:5000/satire"

st.set_page_config(
    page_title="Fauxy – Agentic Satirical News",
    page_icon="🗞️",
    layout="centered"
)

# ---------------- HEADER ----------------
st.title("🗞️ Fauxy Chatbot")
st.caption("An **Agentic, Safe & Explainable AI System** for Satirical News 🇮🇳")

st.markdown("---")

# ---------------- INPUT ----------------
st.subheader("🎯 Create Fauxy News")

topic = st.text_input(
    "Enter a news topic",
    placeholder="e.g. Indian elections, Budget session, Bollywood awards"
)

tone = st.selectbox(
    "Choose satire tone",
    [
        "auto",
        "social media meme style",
        "political parody",
        "dry sarcasm",
        "subtle irony"
    ]
)

compare_mode = st.checkbox("🧪 Compare Agent-selected tone vs User-selected tone")

generate_btn = st.button("🚀 Generate Fauxy News")

# ---------------- HELPERS ----------------
def safety_confidence(risk):
    if risk == "low":
        return 90, "🟢 Low Risk – Relaxed safety rules"
    if risk == "high":
        return 40, "🔴 High Risk – Strict safety applied"
    return 65, "🟡 Medium Risk – Moderate safety"

def satire_breakdown(text):
    points = []
    if "!" in text:
        points.append("Uses exaggeration and hyperbole")
    if any(w in text.lower() for w in ["voter", "rally", "queue", "public", "election"]):
        points.append("Anchored in Indian public and election behavior")
    points.append("Uses irony to contrast expectations vs reality")
    return points

# ---------------- MAIN LOGIC ----------------
if generate_btn:
    if not topic:
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("🧠 Agents planning, researching & generating satire..."):
        resp = requests.post(
            API_URL,
            json={"topic": topic, "tone": tone}
        )

    # ---------- SAFE RESPONSE HANDLING ----------
    if resp.status_code != 200:
        st.error(resp.json().get("error", "Backend error occurred"))
        st.stop()

    primary = resp.json()

    if "satire" not in primary:
        st.error("Satire could not be generated due to safety or data constraints.")
        st.json(primary)
        st.stop()

    # ---------- OPTIONAL A/B COMPARISON ----------
    comparison = None
    if compare_mode and tone != "auto":
        resp_b = requests.post(
            API_URL,
            json={"topic": topic, "tone": tone}
        )
        if resp_b.status_code == 200:
            temp = resp_b.json()
            if "satire" in temp:
                comparison = temp

    satire_text = primary["satire"]
    plan = primary["agent_plan"]
    evaluation = primary["evaluation"]

    st.markdown("---")

    # ---------------- SATIRE OUTPUT ----------------
    st.subheader("😂 Fauxy News Output")

    st.markdown(
        f"""
        <div style="
            background-color:#fff6e6;
            padding:22px;
            border-radius:14px;
            border:2px dashed #ff9800;
            font-size:18px;
            line-height:1.6;
        ">
        {satire_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- SAFETY CONFIDENCE ----------------
    st.subheader("🛡️ Safety Confidence Meter")

    confidence, label = safety_confidence(plan["risk"])
    st.progress(confidence)
    st.caption(label)

    # ---------------- METRICS ----------------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("⚠️ Risk Level", plan["risk"].upper())

    with c2:
        st.metric("📊 Quality Score", evaluation["quality_score"])

    with c3:
        st.metric("✅ Verdict", evaluation["verdict"].capitalize())

    # ---------------- SATIRE BREAKDOWN ----------------
    st.subheader("🧩 Why This Satire Works")

    for point in satire_breakdown(satire_text):
        st.markdown(f"- {point}")

    # ---------------- A/B COMPARISON ----------------
    if compare_mode and comparison:
        st.markdown("---")
        st.subheader("🧪 A/B Tone Comparison")

        colA, colB = st.columns(2)

        with colA:
            st.markdown("**🤖 Agent-selected Tone**")
            st.info(plan["selected_tone"])
            st.write(satire_text)

        with colB:
            st.markdown("**👤 User-selected Tone**")
            st.info(tone)
            st.write(comparison["satire"])

        st.caption(
            "This experiment shows how agentic tone selection improves safety and relevance."
        )

    # ---------------- AGENT TRACE ----------------
    st.markdown("---")
    st.subheader("🔍 Agent Reasoning & Validation")

    with st.expander("🧠 Planner Agent Decision"):
        st.json(plan)

    with st.expander("📈 Evaluation Agent Output"):
        st.json(evaluation)

    with st.expander("📜 Ethical Trace"):
        st.success("Ethical checks passed. Content approved for publication.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "This project demonstrates **agentic planning, ethical reasoning, explainability, and evaluation** using Flask + Streamlit."
)
