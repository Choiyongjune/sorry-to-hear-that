from flask import Flask, request, jsonify
import re

app = Flask(__name__)

emotion_dict = {
    "짜증": 0.7, "짜증나": 0.8, "짜증남": 0.8, "화나": 0.8, "화났": 0.9, "빡치": 1.0,
    "열받": 0.9, "불쾌": 0.8, "서운": 0.8, "실망": 0.8, "속상": 0.8, "섭섭": 0.8,
    "슬퍼": 0.7, "우울": 0.6, "싫어": 0.7, "미워": 0.7, "피곤": 0.6,
    "개짜증": 1.0, "개빡": 1.0, "개열받": 1.0, "씨발": 1.0, "ㅅㅂ": 1.0, "ㅈㄴ": 1.0,
    "존나": 1.0, "ㅈ같": 1.0, "개같": 1.0
}

THRESHOLD = 0.4  # 감정 민감도 낮춤

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

    if intensity >= THRESHOLD:
        reply = "ㅇㅅㅇㄱㅇ"
    else:
        reply = "(무응답)"

    # 서버 로그에도 표시
    print(f"[입력] {message} → [감정단어] {matched} → [강도] {intensity:.2f} → [응답] {reply}")

    # 서버 응답 JSON 형태로 반환
    return jsonify({"response": reply, "intensity": intensity, "matched": matched})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
