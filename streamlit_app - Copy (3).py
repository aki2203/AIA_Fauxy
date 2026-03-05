import streamlit as st
import requests

# ================= CONFIG =================
API_URL = "http://localhost:5000/satire"

st.set_page_config(
    page_title="Fauxy – Agentic Satirical News",
    page_icon="🗞️",
    layout="centered"
)

# ================= HEADER =================
st.title("🗞️ Fauxy Chatbot")
st.caption("An **Agentic, Safe & Explainable AI System** for Satirical News 🇮🇳")

st.markdown("---")

# ================= INPUT =================
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

compare_mode = st.checkbox("🧪 Compare Agent-selected vs User-selected tone (A/B Test)")

generate_btn = st.button("🚀 Generate Fauxy News")

# ================= HELPERS =================
def safety_confidence(risk):
    if risk == "low":
        return 90, "🟢 Low Risk – Relaxed safety rules"
    return 40, "🔴 High Risk – Strict safety applied"


def satire_breakdown(text):
    points = []
    if "!" in text:
        points.append("Uses exaggeration and hyperbole for humor")
    if any(w in text.lower() for w in ["voter", "rally", "queue", "public", "election"]):
        points.append("Anchored in Indian public and political behavior")
    points.append("Uses irony to contrast expectations vs reality")
    return points


# ================= MAIN =================
if generate_btn:
    if not topic:
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("🧠 Agents planning, researching & generating satire..."):
        resp = requests.post(API_URL, json={"topic": topic, "tone": tone})

    if resp.status_code != 200:
        st.error(resp.json().get("error", "Backend error occurred"))
        st.stop()

    data = resp.json()
    if "satire" not in data:
        st.error("Satire could not be generated due to safety or data constraints.")
        st.stop()

    satire = data["satire"]
    plan = data["agent_plan"]
    evaluation = data["evaluation"]

    # ---------- Optional A/B comparison ----------
    comparison = None
    if compare_mode and tone != "auto":
        resp_b = requests.post(API_URL, json={"topic": topic, "tone": tone})
        if resp_b.status_code == 200:
            temp = resp_b.json()
            if "satire" in temp:
                comparison = temp

    st.markdown("---")

    # ================= SATIRE OUTPUT =================
    st.subheader("😂 Fauxy News Output")

    st.markdown(
        f"""
        <div style="
            background-color:#fff6e6;
            padding:24px;
            border-radius:16px;
            border:2px dashed #ff9800;
            font-size:18px;
            line-height:1.6;
        ">
        {satire}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ================= SAFETY CONFIDENCE =================
    st.subheader("🛡️ Safety Confidence Meter")
    confidence, label = safety_confidence(plan["risk"])
    st.progress(confidence)
    st.caption(label)

    # ================= METRICS =================
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("⚠️ Risk Level", plan["risk"].upper())
    with c2:
        st.metric("📊 Quality Score", evaluation["quality_score"])
    with c3:
        st.metric("✅ Verdict", evaluation["verdict"].capitalize())

    # ================= SATIRE BREAKDOWN =================
    st.subheader("🧩 Why This Satire Works")
    for point in satire_breakdown(satire):
        st.markdown(f"- {point}")

    # ================= A/B COMPARISON =================
    if compare_mode and comparison:
        st.markdown("---")
        st.subheader("🧪 A/B Tone Comparison")

        colA, colB = st.columns(2)

        with colA:
            st.markdown("### 🤖 Agent-selected Tone")
            st.success(plan["selected_tone"])
            st.write(satire)

        with colB:
            st.markdown("### 👤 User-selected Tone")
            st.info(tone)
            st.write(comparison["satire"])

        st.caption(
            "This experiment shows how agentic tone selection improves safety and relevance."
        )

    # ================= AGENT REASONING (VISUAL) =================
    st.markdown("---")
    st.subheader("🧠 Agent Reasoning & Validation")

    # ---- Planner Card ----
    st.markdown("### 🧠 Planner Agent Decision")
    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("**📰 Topic**")
        st.info(plan["topic"].capitalize())

    with p2:
        st.markdown("**🎭 Final Tone**")
        st.success(plan["selected_tone"])

    with p3:
        if plan["risk"] == "low":
            st.success("🟢 Low Risk")
        else:
            st.error("🔴 High Risk")

    st.markdown(
        f"""
        ✅ Ethics Check Applied: **{plan['needs_ethics_check']}**  
        📊 Evaluation Enabled: **{plan['needs_evaluation']}**
        """
    )

    # ---- Evaluation Card ----
    st.markdown("### 📈 Evaluation Agent Output")
    e1, e2 = st.columns(2)

    with e1:
        st.metric("Quality Score", f"{evaluation['quality_score']} / 3")

    with e2:
        if evaluation["verdict"] == "high":
            st.success("🟢 High Quality")
        else:
            st.warning("🟡 Average Quality")

    st.markdown("**🧾 Evaluation Reasons:**")
    for reason in evaluation["reasons"]:
        st.markdown(f"- {reason}")

# ================= FOOTER =================
st.markdown("---")
st.caption(
    "Built using **Flask + Streamlit + Agentic AI** with planning, ethics, evaluation & explainability."
)
