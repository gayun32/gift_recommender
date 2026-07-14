from http.server import BaseHTTPRequestHandler
import json
import os
from google import genai


def build_prompt(data):
    """입력값을 바탕으로 선물 추천 프롬프트 생성"""
    relationship = data.get("relationship", "")
    age = data.get("age", "")
    gender = data.get("gender", "")
    budget = data.get("budget", "")
    interest = data.get("interest", "") or "특별히 없음"

    return f"""당신은 선물 추천 전문가입니다.
아래 조건에 맞는 선물 3가지를 추천해주세요.

- 받는 사람과의 관계: {relationship}
- 나이: {age}
- 성별: {gender}
- 예산: {budget}원 이내
- 취향/관심사: {interest}

반드시 아래 JSON 형식으로만 응답하세요. 다른 설명, 코드블록 표시(```) 없이 순수 JSON만 출력하세요.

{{
  "recommendations": [
    {{"name": "선물 이름", "reason": "이 선물을 추천하는 이유 1~2문장"}},
    {{"name": "선물 이름", "reason": "이 선물을 추천하는 이유 1~2문장"}},
    {{"name": "선물 이름", "reason": "이 선물을 추천하는 이유 1~2문장"}}
  ]
}}
"""


def clean_json_text(text):
    """LLM 응답에서 코드블록 표시 제거"""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            # 1) 요청 바디 읽기
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self._send_json(400, {"error": "요청 형식이 올바르지 않습니다."})
                return

            # 2) 필수값 검증
            if not data.get("relationship") or not data.get("age") or not data.get("budget"):
                self._send_json(400, {"error": "필수값이 누락되었습니다."})
                return

            # 3) API 키 확인
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                self._send_json(500, {"error": "서버에 API 키가 설정되지 않았습니다."})
                return

            # 4) Gemini 호출
            client = genai.Client(api_key=api_key)
            prompt = build_prompt(data)

            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
            )

            # 5) 빈 응답(안전 필터 등으로 콘텐츠가 막힌 경우) 처리
            if not response.text:
                self._send_json(502, {"error": "AI가 응답을 생성하지 못했습니다. 잠시 후 다시 시도해주세요."})
                return

            # 6) AI 응답 JSON 파싱
            try:
                cleaned = clean_json_text(response.text)
                result = json.loads(cleaned)
            except json.JSONDecodeError:
                self._send_json(502, {"error": "AI 응답을 처리하는 중 오류가 발생했습니다."})
                return

            self._send_json(200, result)

        except Exception as e:
            self._send_json(500, {"error": f"서버 오류: {str(e)}"})

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))