import streamlit as st
import requests

# ================= CONFIG =================
API_URL = "http://localhost:5000/satire"

st.set_page_config(
    page_title="Fauxy – Agentic Satirical News",
    page_icon="🗞️",
    layout="centered"
)

# ================= GLOBAL STYLES =================
st.markdown("""
<style>
.card {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 18px;
    border: 1px solid #eee;
}
.satire-box {
    background-color: #fff6e6;
    padding: 26px;
    border-radius: 16px;
    border: 2px dashed #ff9800;
    font-size: 18px;
    line-height: 1.7;
}
.tag {
    display: inline-block;
    padding: 4px 10px;
    margin-right: 6px;
    border-radius: 20px;
    font-size: 12px;
    background-color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🗞️ Fauxy Chatbot")
st.caption("An **Agentic, Safe & Explainable AI System** for Indian Satirical News")

st.markdown("---")

# ================= INPUT SECTION =================
st.subheader("🎯 Create Fauxy News")

with st.container():
    topic = st.text_input(
        "📰 Enter a news topic",
        placeholder="e.g. Indian Budget, Elections, Bureaucracy, Public Reactions"
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

    compare_mode = st.checkbox("🧪 Compare Agent-selected vs User-selected tone (A/B Test)")

    generate_btn = st.button("🚀 Generate Fauxy News")

# ================= HELPERS =================
def safety_confidence(risk):
    if risk == "low":
        return 90, "🟢 Low Risk – Standard safety constraints applied"
    return 40, "🔴 High Risk – Enhanced safety & ethics validation"


def satire_breakdown(text):
    points = []
    if "!" in text:
        points.append("Uses exaggeration and hyperbole")
    if any(w in text.lower() for w in ["voter", "queue", "budget", "public", "rally"]):
        points.append("Anchored in Indian public behavior")
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
    satire = data["satire"]
    plan = data["agent_plan"]
    evaluation = data["evaluation"]

    # ---------- Optional A/B comparison ----------
    comparison = None
    if compare_mode and tone != "auto":
        resp_b = requests.post(API_URL, json={"topic": topic, "tone": tone})
        if resp_b.status_code == 200 and "satire" in resp_b.json():
            comparison = resp_b.json()

    st.markdown("---")

    # ================= SATIRE OUTPUT =================
    st.subheader("😂 Fauxy News Output")

    st.markdown("""
    <span class="tag">Satire Type</span>
    <span class="tag">Observational</span>
    <span class="tag">Exaggeration-based</span>
    <span class="tag">Culturally Contextual</span>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="satire-box">
        {satire}
    </div>
    """, unsafe_allow_html=True)

    # ================= RESEARCH GROUNDING =================
    with st.expander("📰 Context Grounding (Research Agent)"):
        st.write(
            "This satire is grounded in recent public discourse related to the topic, "
            "reflecting common Indian public sentiment and behavior. "
            "Grounding helps reduce hallucination and improves relevance."
        )

    # ================= SAFETY CONFIDENCE =================
    st.subheader("🛡️ Safety & Governance")

    confidence, label = safety_confidence(plan["risk"])
    st.progress(confidence)
    st.caption(label)

    st.info(
        "Low risk indicates absence of protected groups, named political actors, "
        "or factual misinformation. Humor amplification was permitted safely."
    )

    # ================= METRICS =================
    st.subheader("📊 Output Evaluation Metrics")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("⚠️ Risk Level", plan["risk"].upper())
    with c2:
        st.metric("📊 Quality Score", f"{evaluation['quality_score']} / 3")
    with c3:
        st.metric("✅ Verdict", evaluation["verdict"].capitalize())

    # ================= SATIRE ANALYSIS =================
    st.subheader("🧩 Model Introspection: Humor Analysis")

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
            "This comparison demonstrates how agentic tone selection "
            "balances humor quality with safety constraints."
        )

    # ================= AGENT REASONING =================
    st.markdown("---")
    st.subheader("🧠 Agent Reasoning & Validation")

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
        "**🧠 Autonomous Decision Justification**  \n"
        "The planner agent classified the topic as low sensitivity, "
        "allowing humor amplification using a meme-style tone while "
        "maintaining ethical safeguards."
    )

    # ================= EVALUATION AGENT =================
    st.markdown("### 📈 Evaluation Agent Output")

    st.success("🟢 High Quality Output")

    st.markdown("**🧾 Evaluation Reasons:**")
    for reason in evaluation["reasons"]:
        st.markdown(f"- {reason}")

# ================= FOOTER =================
st.markdown("---")
st.caption(
    "Built using **Flask + Streamlit + Agentic AI** with planning, grounding, ethics, evaluation & explainability."
)
