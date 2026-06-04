"""
1. url을 통해 소스코드를 읽어옴
2. 진단하고 싶은 취약점 유형 선택 가능 ex. 민감정보(하드코딩된 암호), SQL Injection, XSS
3. 취약 코드 및 라인 번호 노출
4. 코드를 분석하여 취약점 설명
5. 취약점의 위험 수준(낮음, 중간, 높음) 표시
6. 사용자 친화적인 인터페이스 제공
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from flask import Flask, send_from_directory, jsonify, request

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__, static_folder='public')
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def _build_analysis_prompt(source_code, vulnerability_types):
        selected = ", ".join(vulnerability_types)
        return f"""
당신은 보안 코드 리뷰 전문가입니다.
아래 소스코드를 분석해서 선택된 취약점 유형만 점검하세요.

선택된 취약점 유형: {selected}

반드시 JSON 객체만 반환하세요. 설명 문장은 JSON 바깥에 출력하지 마세요.
JSON 스키마는 아래와 같습니다.
{{
    "summary": "분석 요약",
    "findings": [
        {{
            "vulnerability_type": "취약점 유형",
            "severity": "낮음|중간|높음",
            "line_numbers": [정수, ...],
            "problematic_code": "문제가 되는 코드 일부",
            "description": "왜 취약한지 설명",
            "recommendation": "개선 방법"
        }}
    ]
}}

만약 취약점이 없으면 findings는 빈 배열로 반환하세요.

소스코드:
```\n{source_code}\n```
"""

# -----------------
# 웹 서비스 라우팅
# -----------------
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# -----------------
# API 라우팅
# -----------------
@app.route('/api/analyze', methods=['POST'])
def analyze():
    if not openai_api_key:
        return jsonify({"error": "OPENAI_API_KEY가 설정되지 않았습니다."}), 500

    data = request.get_json(silent=True) or {}
    source_code = data.get("source_code", "")
    vulnerability_types = data.get("vulnerability_types", [])

    if not source_code.strip():
        return jsonify({"error": "분석할 소스코드가 없습니다."}), 400

    if not vulnerability_types:
        return jsonify({"error": "최소 1개 이상의 취약점 유형을 선택해주세요."}), 400

    try:
        prompt = _build_analysis_prompt(source_code, vulnerability_types)
        response = client.responses.create(
            model=openai_model,
            input=prompt,
            temperature=0.1,
        )

        output_text = (response.output_text or "").strip()
        if output_text.startswith("```"):
            output_text = output_text.strip("`")
            output_text = output_text.replace("json", "", 1).strip()

        parsed = json.loads(output_text)
        findings = parsed.get("findings", [])
        summary = parsed.get("summary", "분석을 완료했습니다.")

        normalized_findings = []
        for item in findings:
            severity = item.get("severity", "중간")
            if severity not in ["낮음", "중간", "높음"]:
                severity = "중간"

            line_numbers = item.get("line_numbers", [])
            if not isinstance(line_numbers, list):
                line_numbers = []

            normalized_findings.append({
                "vulnerability_type": item.get("vulnerability_type", "알 수 없음"),
                "severity": severity,
                "line_numbers": [n for n in line_numbers if isinstance(n, int)],
                "problematic_code": item.get("problematic_code", ""),
                "description": item.get("description", ""),
                "recommendation": item.get("recommendation", ""),
            })

        return jsonify({
            "summary": summary,
            "findings": normalized_findings,
        })
    except json.JSONDecodeError:
        return jsonify({"error": "분석 결과를 JSON으로 파싱하지 못했습니다."}), 502
    except Exception as e:
        return jsonify({"error": f"분석 중 오류가 발생했습니다: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)