from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-xxxxxxxxxxxxxxxxxxxx"))

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # 카카오톡 메시지 추출
    user_msg = data.get("userRequest", {}).get("utterance", "")

    # AI로 감정 분석 요청
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 사용자의 감정 상태를 분석해서, 상대가 짜증내거나 서운해하면 'ㅇㅅㅇㄱㅇ'만 답해. 그 외에는 아무 대답도 하지 마."},
            {"role": "user", "content": user_msg}
        ]
    )

    reply = response.choices[0].message.content.strip()

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": reply}}]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
