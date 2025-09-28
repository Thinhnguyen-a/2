from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/', methods=['GET'])
def home():
    return "✅ Flask server đang hoạt động với Groq!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Thiếu trường "question"'}), 400

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",

        "messages": [{"role": "user", "content": question}]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        result = response.json()

        # Kiểm tra phản hồi có "choices" không
        if "choices" in result and len(result["choices"]) > 0:
            answer = result["choices"][0]["message"]["content"]
            return jsonify({'answer': answer})
        else:
            # Trả về toàn bộ phản hồi lỗi từ Groq để dễ debug
            return jsonify({'error': 'Phản hồi không hợp lệ từ Groq', 'raw': result}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
