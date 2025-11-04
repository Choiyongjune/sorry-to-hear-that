from flask import Flask, request, jsonify
import openai, os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    # 루트 접속 시 간단한 확인용
    return "Server is running", 200

@app.route("/webhook", methods=["POST"])
def kakao_webhook():
    try:
        data = request.get_json(force=True)
        user_msg = data.get("userRequest", {}).get("utterance", "")
    except Exception as e:
        print("JSON parse error:", e)
        return jsonify({"error": "invalid request"}), 400

    # 감정 분석 프롬프트
    emotion_prompt = f"""
    다음 문장의 감정을 분석해줘: "{user_msg}"
    가능한 결과: 긍정적, 중립적, 짜증, 서운함, 화남, 슬픔
    한 단어로만 답해줘.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": emotion_prompt}]
        )
        emotion = response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI error:", e)
        emotion = "오류"

    # 감정에 따라 응답 결정
    if emotion in ["짜증", "서운함", "화남", "슬픔"]:
        reply_text = "ㅇㅅㅇㄱㅇ"
    else:
        reply_text = " "

    # 카카오 오픈빌더 규격 JSON
    kakao_response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": reply_text}}
            ]
        }
    }

    return jsonify(kakao_response), 200  # ← 반드시 200 반환!

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
