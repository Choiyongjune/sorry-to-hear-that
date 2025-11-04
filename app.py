from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route("/webhook", methods=["POST"])
def kakao_webhook():
    data = request.get_json()
    user_msg = data['userRequest']['utterance']

    emotion_prompt = f"""
    다음 문장의 감정을 분석해줘: "{user_msg}"
    가능한 결과: 긍정적, 중립적, 짜증, 서운함, 화남, 슬픔
    한 단어로만 답해줘.
    """

    emotion_res = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": emotion_prompt}]
    )
    emotion = emotion_res.choices[0].message.content.strip()

    if emotion in ["짜증", "서운함", "화남", "슬픔"]:
        reply_text = "ㅇㅅㅇㄱㅇ"
    else:
        return jsonify({
            "version": "2.0",
            "template": {"outputs": []}
        })

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": reply_text}}]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)