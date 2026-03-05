import streamlit as st
import requests
import os
import time

# ---------------- CONFIG ----------------

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_NEWSAPI_KEY")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "fauxybot"

st.set_page_config(
    page_title="Fauxy – Satirical News AI",
    page_icon="🤡",
    layout="centered"
)

# ---------------- UI ----------------

st.title("🤡 Fauxy")
st.subheader("Agentic Satirical News Generator")

st.write("Turn real news into sarcastic satire.")

topic = st.text_input("Enter a news topic", placeholder="Cricket, Elections, Budget...")

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

generate = st.button("🚀 Generate Fauxy News")

# ---------------- FUNCTIONS ----------------

def fetch_news(topic):

    url = f"https://newsapi.org/v2/everything?q={topic}&language=en&pageSize=1&apiKey={NEWS_API_KEY}"

    response = requests.get(url)

    data = response.json()

    if not data.get("articles"):
        return None

    article = data["articles"][0]

    return article.get("description") or article.get("title")


def generate_satire(news_summary):

    prompt = f"""
You are a sarcastic reporter from 'The Fauxy'.

Real news:
{news_summary}

Write a funny, sarcastic Indian satire news report.
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()

    return data.get("response", "")


# ---------------- MAIN LOGIC ----------------

if generate:

    if not topic:
        st.error("Please enter a topic")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    status.write("🔎 Searching news...")
    progress.progress(20)

    news_summary = fetch_news(topic)

    if not news_summary:
        st.error("No news found for this topic.")
        st.stop()

    status.write("📰 Found news article")
    progress.progress(50)

    status.write("🤖 Generating satire...")
    progress.progress(80)

    satire = generate_satire(news_summary)

    progress.progress(100)
    status.empty()

    st.success("Satire generated!")

    st.subheader("📰 Real News Summary")
    st.write(news_summary)

    st.subheader("😂 Fauxy Report")
    st.write(satire)
