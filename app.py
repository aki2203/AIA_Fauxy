from flask import Flask, request, jsonify
import requests, os, json
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama3-70b-8192")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY or not NEWS_API_KEY:
    raise RuntimeError("Set GROQ_API_KEY and NEWS_API_KEY in your environment or .env file.")

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def call_groq(payload):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    return requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)

@app.route('/satire', methods=['POST'])
def generate_satire():
    data = request.get_json()
    topic = data.get("topic", "")
    if not topic:
        return jsonify({"error": "Missing 'topic' field"}), 400

    # Fetch news
    try:
        news_url = f"https://newsapi.org/v2/everything?q={topic}&language=en&pageSize=1&apiKey={NEWS_API_KEY}"
        r = requests.get(news_url, timeout=10)
        r.raise_for_status()
        articles = r.json().get("articles", [])
        if not articles:
            return jsonify({"error": "No articles found"}), 404
        factual = articles[0].get("description") or articles[0].get("title")
    except Exception as e:
        return jsonify({"error": f"Failed to fetch news: {str(e)}"}), 500

    prompt = f"""
You are a satirical news reporter from 'The Fauxy'.
REAL NEWS: {factual}
Now, write a funny, sarcastic one-paragraph satirical news version.
"""

    groq_payload = {
        "model": GROQ_MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a sharp, witty satirical journalist."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 300
    }

    try:
        resp = call_groq(groq_payload)
        resp.raise_for_status()
        result = resp.json()
        satire = result["choices"][0]["message"]["content"]
        return jsonify({"topic": topic, "satire": satire.strip()})
    except Exception as e:
        return jsonify({"error": f"Groq failed: {str(e)}"}), 502

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
