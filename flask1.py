from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'Missing "question" field'}), 400

    question = data['question']

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response['choices'][0]['message']['content']
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Mở cổng cho Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
