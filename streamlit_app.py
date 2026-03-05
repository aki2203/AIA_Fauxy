import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:5000/satire")

st.set_page_config(page_title="Fauxy", page_icon="📰", layout="centered")
st.title("🤡 Fauxy – India's Satirical AI")

st.markdown("Witty, agentic satire from real news. Powered by Groq + NewsAPI.")

topic = st.text_input("📰 Enter a news topic", placeholder="e.g. Cricket, Budget 2024, Lok Sabha Elections")
submit = st.button("🚀 Generate Fauxy Satire")

def planner_agent(topic):
    if "election" in topic.lower():
        return {"tone": "political parody", "risk": "medium"}
    return {"tone": "sarcastic", "risk": "low"}

def evaluate_output(text):
    humor = "😂" if "😂" in text or "!" in text else "🙂"
    return {"humor": humor, "length": len(text)}

if submit:
    if not topic:
        st.warning("Enter a topic to continue.")
        st.stop()

    with st.spinner("Planning satire strategy..."):
        plan = planner_agent(topic)

    with st.spinner("Generating satire via Groq..."):
        try:
            res = requests.post(API_URL, json={"topic": topic}, timeout=30)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            st.error(f"Backend error: {e}")
            st.stop()

    with st.spinner("Evaluating quality..."):
        evaluation = evaluate_output(data["satire"])

    st.success("✅ Fauxy Satire Generated!")
    st.subheader("📋 Strategy")
    st.write(plan)

    st.subheader("🧪 Satirical Output")
    st.write(data["satire"])

    st.subheader("📊 Evaluation")
    st.write(evaluation)
