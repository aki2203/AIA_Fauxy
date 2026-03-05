import streamlit as st
import requests
import json

BACKEND_URL = "http://127.0.0.1:5000/satire"

st.set_page_config(page_title="Fauxy Chatbot 🇮🇳", page_icon="📰")

st.title("📰 Fauxy Chatbot")
st.subheader("Satirical Indian-Style News Generator 🇮🇳")

st.markdown(
    "This demo uses a Flask backend with a Streamlit frontend."
)

topic = st.text_input(
    "Enter a news topic",
    value="Indian elections"
)

tone = st.selectbox(
    "Choose satire tone",
    [
        "light satire",
        "sarcastic Indian stand-up comedian",
        "political parody",
        "social media meme style"
    ]
)

if st.button("Generate Fauxy News 🚀"):
    with st.spinner("Generating satire..."):
        payload = {
            "topic": topic,
            "tone": tone
        }

        try:
            response = requests.post(
                BACKEND_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=60
            )

            if response.status_code == 200:
                st.success("Here’s your Fauxy News 😄")
                st.json(response.json())
            else:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)

        except Exception as e:
            st.error("Could not connect to backend")
            st.text(str(e))
