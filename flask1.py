from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Khởi tạo client OpenAI với API key từ biến môi trường
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=['GET'])
def home():
    return "✅ Flask server đang hoạt động!"

@app.route('/ask', methods=['POST'])
def ask():
    print("📥 Nhận yêu cầu POST /ask")
    data = request.get_json()
    if not data or 'question' not in data:
        print("⚠️ Thiếu trường 'question'")
        return jsonify({'error': 'Missing \"question\" field'}), 400

    question = data['question']
    print(f"🧠 Câu hỏi nhận được: {question}")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        print(f"🤖 Trả lời: {answer}")
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"❌ Lỗi khi gọi OpenAI: {e}")
        return jsonify({'error': str(e)}), 500

# Mở cổng cho Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
