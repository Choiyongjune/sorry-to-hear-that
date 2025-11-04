from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# ✅ 감정 단어 사전: {단어: 강도 점수(0~1)}
emotion_dict = {
    # 짜증/화남
    "짜증": 0.8, "짜증나": 0.8, "짜증남": 0.8, "짜증나요": 0.7, "짜증나네": 0.7, "짜증나서": 0.8,
    "화나": 0.9, "화났": 1.0, "빡치": 1.0, "열받": 0.9, "화딱지": 1.0,
    "미쳐": 0.7, "스트레스": 0.6, "불쾌": 0.7,

    # 서운/실망/슬픔
    "서운": 0.8, "서운해": 0.9, "실망": 0.9, "슬퍼": 0.8, "우울": 0.7, "속상": 0.9,
    "섭섭": 0.9, "눈물": 0.6, "눈물이": 0.7,

    # 싫음/미움
    "싫어": 0.9, "미워": 0.8, "정떨어": 0.9, "질려": 0.8, "짜증나버": 1.0,

    # 욕/강한 표현
    "빡쳐": 1.0, "ㅈㄴ": 1.0, "씨발": 1.0, "ㅅㅂ": 1.0, "개빡": 1.0, "존나": 1.0,
    "개짜증": 1.0, "개열받": 1.0, "ㅈ같": 1.0, "개같": 1.0, "ㅁㅊ": 0.9, "미친": 0.8
}

# ✅ 감정 강도 판단 기준 (조정 가능)
THRESHOLD = 0.7

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_msg = data.get("userRequest", {}).get("utterance", "").lower()

    # ✅ 메시지에서 감정 단어 찾기
    intensity = 0.0
    for word, score in emotion_dict.items():
        if re.search(word, user_msg):
            intensity = max(intensity, score)

    # ✅ 감정 강도가 기준 이상이면 반응
    if intensity >= THRESHOLD:
        reply = "ㅇㅅㅇㄱㅇ"
    else:
        reply = ""  # 평온하면 아무 대답 안 함

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": reply}}]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
