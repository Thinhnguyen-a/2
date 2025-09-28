from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "✅ Flask server đang hoạt động!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Thiếu trường \"question\"'}), 400

    # Trả về phản hồi giả lập
    fake_answer = f"Bạn vừa hỏi: \"{question}\". Đây là phản hồi giả lập từ AI."
    return jsonify({'answer': fake_answer})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
