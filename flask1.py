from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "✅ Flask server đang hoạt động!"

@app.route('/ask', methods=['POST'])
def ask():
    print("📥 Nhận yêu cầu POST /ask")
    data = request.get_json()
    if not data or 'question' not in data:
        print("⚠️ Thiếu trường 'question'")
        return jsonify({'error': 'Missing "question" field'}), 400

    question = data['question']
    print(f"🧠 Câu hỏi nhận được: {question}")

    if not openai.api_key:
        print("❌ Thiếu API key")
        return jsonify({'error': 'Missing OpenAI API key'}), 500

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response['choices'][0]['message']['content']
        print(f"🤖 Trả lời: {answer}")
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"❌ Lỗi khi gọi OpenAI: {e}")
        return jsonify({'error': str(e)}), 500

# Mở cổng cho Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
