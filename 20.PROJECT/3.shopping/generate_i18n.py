"""
public/locales/ko.json 을 기반으로 OpenAI API를 사용해
en.json, ja.json, zh.json 을 자동 생성하는 스크립트입니다.

사용법:
    python generate_i18n.py
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
LOCALES_DIR = Path(__file__).parent / "public" / "locales"

LANG_NAMES = {
    "en": "English",
    "ja": "Japanese",
    "zh": "Simplified Chinese",
}


def translate(ko_data: dict, target_lang: str) -> dict:
    ko_json = json.dumps(ko_data, ensure_ascii=False, indent=2)
    lang_name = LANG_NAMES[target_lang]

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    f"You are a professional UI translator for an e-commerce shopping mall. "
                    f"Translate all JSON values from Korean to {lang_name}. "
                    f"Rules:\n"
                    f"- Keep all JSON keys exactly as-is.\n"
                    f"- Keep template placeholders like {{score}} and {{rating}} unchanged.\n"
                    f"- Keep special characters like ← and © as-is.\n"
                    f"- Use natural, concise UI phrasing appropriate for a shopping app.\n"
                    f"- Return only valid JSON with no explanation or markdown."
                ),
            },
            {
                "role": "user",
                "content": ko_json,
            },
        ],
        temperature=0.1,
    )

    raw = response.output_text.strip()
    # strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]

    return json.loads(raw)


def main():
    ko_path = LOCALES_DIR / "ko.json"
    if not ko_path.exists():
        print(f"Error: {ko_path} not found.")
        return

    with open(ko_path, encoding="utf-8") as f:
        ko_data = json.load(f)

    for lang in LANG_NAMES:
        print(f"Translating → {lang} ({LANG_NAMES[lang]})...")
        try:
            translated = translate(ko_data, lang)
            out_path = LOCALES_DIR / f"{lang}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(translated, f, ensure_ascii=False, indent=2)
                f.write("\n")
            print(f"  ✓ {out_path}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
