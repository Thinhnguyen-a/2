from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "gpt-oss-20b"  # Đổi tại đây nếu cần

@app.route('/', methods=['GET'])
def home():
    return "✅ Flask server đang hoạt động với Groq!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Thiếu trường \"question\"'}), 400

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-oss-20b",
        "messages": [{"role": "user", "content": question}]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        result = response.json()

        # Nếu Groq trả về lỗi
        if "error" in result:
            return jsonify({
                'error': 'Groq trả về lỗi',
                'code': result["error"].get("code", "unknown"),
                'message': result["error"].get("message", "Không rõ nguyên nhân")
            }), 500

        # Nếu phản hồi hợp lệ
        if "choices" in result and result["choices"]:
            answer = result["choices"][0]["message"]["content"]
            return jsonify({'answer': answer})

        # Nếu phản hồi không có "choices"
        return jsonify({'error': 'Phản hồi không hợp lệ từ Groq', 'raw': result}), 500

    except Exception as e:
        return jsonify({'error': 'Lỗi hệ thống', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
