from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# 감정 단어 사전
emotion_dict = {
    "짜증": 0.7, "짜증나": 0.8, "짜증남": 0.8, "화나": 0.8, "화났": 0.9, "빡치": 1.0,
    "열받": 0.9, "불쾌": 0.8, "서운": 0.8, "실망": 0.8, "속상": 0.8, "섭섭": 0.8,
    "슬퍼": 0.7, "우울": 0.6, "싫어": 0.7, "미워": 0.7, "피곤": 0.6,
    "개짜증": 1.0, "개빡": 1.0, "개열받": 1.0, "씨발": 1.0, "ㅅㅂ": 1.0, "ㅈㄴ": 1.0,
    "존나": 1.0, "ㅈ같": 1.0, "개같": 1.0
}

THRESHOLD = 0.4  # 감정 민감도 낮춤

# ✅ 홈페이지 안내 페이지
@app.route("/", methods=["GET"])
def home():
    return """
    <html>
    <head><meta charset="utf-8"><title>ㅇㅅㅇㄱㅇ 봇 서버</title></head>
    <body style="font-family:sans-serif; background:#fafafa; color:#333; margin:40px;">
        <h2>ㅇㅅㅇㄱㅇ 감정 응답 서버</h2>
        <p>이 서버는 <b>/webhook</b> 경로로 감정 문장을 받으면,</p>
        <p>짜증나거나 서운한 말이 포함될 때 <b>ㅇㅅㅇㄱㅇ</b> 로 응답합니다.</p>
        <hr>
        <p><b>테스트 방법:</b></p>
        <pre style="background:#eee; padding:10px; border-radius:8px;">
curl -X POST -H "Content-Type: application/json" \\
-d '{"message": "짜증나"}' \\
https://osogoi-bot.onrender.com/webhook
        </pre>
        <p>카카오 오픈빌더 스킬 URL에도 동일하게 <code>/webhook</code> 주소를 사용하세요 ✅</p>
    </body>
    </html>
    """

# ✅ 카카오 오픈빌더용 Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    message = data.get("message", "").lower()
    intensity = 0.0
    matched = []

    for word, score in emotion_dict.items():
        if re.search(word, message):
            matched.append(word)
            intensity = max(intensity, score)

    reply = "ㅇㅅㅇㄱㅇ" if intensity >= THRESHOLD else "(무응답)"

    # 서버 콘솔 로그
    print(f"[입력] {message} → [감정단어] {matched} → [강도] {intensity:.2f} → [응답] {reply}")

    return jsonify({"response": reply, "intensity": intensity, "matched": matched})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
