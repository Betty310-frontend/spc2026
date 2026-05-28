"""
1. API 라우팅, 웹 서비스 라우팅 분리
2. 제품 목록
3. 제품 목록에서 제품 클릭 시 상세 페이지 이동
4. 상세 페이지에서 제품 정보, 리뷰, 평점 표시
5. 상세 페이지에서 리뷰와 평점 작성 가능
6. reviews를 분석하여 AI가 요약한 결과를 노출
7. 사용자 친화적인 인터페이스 제공
8. 다국어 지원
"""

# -*- coding: utf-8 -*-
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from openai import OpenAI

import json

from flask import Flask, jsonify, request, send_from_directory

load_dotenv()  # .env 파일에서 환경 변수 로드

openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__, static_folder='public')
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# 번역 캐시: (원문, 언어코드) → 번역문
_translation_cache: dict = {}
_LANG_NAMES = {'en': 'English', 'ja': 'Japanese', 'zh': 'Simplified Chinese'}

# 제품 목록을 저장할 변수 (예시로 간단한 제품 정보를 담은 리스트를 사용)
products = [
    {
        'id': 1,
        'name': '에어핏 러닝화',
        'description': '가벼운 니트 어퍼와 쿠셔닝 미드솔로 장시간 착용에도 편안한 데일리 러닝화',
        'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80'
    },
    {
        'id': 2,
        'name': '미니멀 백팩',
        'description': '생활 방수 소재와 노트북 수납 공간을 갖춘 출퇴근용 백팩',
        'image': 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80'
    },
    {
        'id': 3,
        'name': '클래식 손목시계',
        'description': '심플한 다이얼과 메탈 스트랩 조합으로 포멀/캐주얼 모두 어울리는 시계',
        'image': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=900&q=80'
    },
    {
        'id': 4,
        'name': '무선 블루투스 이어폰',
        'description': '저지연 모드와 노이즈 캔슬링을 지원해 음악 통화 품질을 높인 이어폰',
        'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80'
    },
    {
        'id': 5,
        'name': '스테인리스 텀블러',
        'description': '보온 보냉 기능이 우수하고 누수 방지 캡을 적용한 500ml 텀블러',
        'image': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=80'
    },
    {
        'id': 6,
        'name': '우드 데스크 램프',
        'description': '눈부심을 줄인 따뜻한 조명과 각도 조절 기능을 갖춘 책상용 램프',
        'image': 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=900&q=80'
    },
    {
        'id': 7,
        'name': '스마트폰 거치대',
        'description': '높이와 각도 조절이 가능한 접이식 거치대로 영상 시청과 화상회의에 최적화',
        'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80'
    },
    {
        'id': 8,
        'name': '휴대용 블루투스 스피커',
        'description': '컴팩트한 크기에 풍부한 저음을 담아 실내외 어디서나 사용 가능한 스피커',
        'image': 'https://images.unsplash.com/photo-1589003077984-894e133dabab?auto=format&fit=crop&w=900&q=80'
    },
    {
        'id': 9,
        'name': '프리미엄 커피 원두',
        'description': '다크초콜릿 향과 견과류 풍미가 조화로운 미디엄 로스트 블렌드 원두',
        'image': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=900&q=80'
    },
    {
        'id': 10,
        'name': '코튼 오버핏 티셔츠',
        'description': '부드러운 촉감의 100% 코튼 소재로 사계절 활용 가능한 베이직 티셔츠',
        'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80'
    }
]
# 사용자들의 댓글을 저장할 변수
# 예시: {'product_id': 1, 'rating': 5, 'comment': '좋아요'}
reviews = [
    {
        'product_id': 1,
        'rating': 5,
        'comment': '착화감이 정말 좋고 오래 걸어도 편합니다.',
        'created_at': '2026-05-25T09:20:00+00:00'
    },
    {
        'product_id': 1,
        'rating': 4,
        'comment': '쿠셔닝은 만족스럽고 디자인도 깔끔합니다.',
        'created_at': '2026-05-26T14:05:00+00:00'
    },
    {
        'product_id': 2,
        'rating': 5,
        'comment': '노트북 수납이 넉넉하고 어깨 부담이 적어요.',
        'created_at': '2026-05-24T07:42:00+00:00'
    },
    {
        'product_id': 3,
        'rating': 4,
        'comment': '정장에 잘 어울립니다. 다만 줄 길이 조절이 조금 아쉬워요.',
        'created_at': '2026-05-23T11:18:00+00:00'
    },
    {
        'product_id': 4,
        'rating': 3,
        'comment': '음질은 괜찮지만 배터리 지속시간은 보통입니다.',
        'created_at': '2026-05-26T03:33:00+00:00'
    },
    {
        'product_id': 5,
        'rating': 5,
        'comment': '보온력이 기대 이상이라 겨울에도 잘 사용 중입니다.',
        'created_at': '2026-05-25T19:50:00+00:00'
    },
    {
        'product_id': 7,
        'rating': 4,
        'comment': '각도 조절이 쉬워서 화상회의할 때 유용합니다.',
        'created_at': '2026-05-26T08:10:00+00:00'
    },
    {
        'product_id': 8,
        'rating': 5,
        'comment': '작은 크기인데 저음이 잘 살아있어요.',
        'created_at': '2026-05-27T01:05:00+00:00'
    }
]


def now_iso_utc():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def get_request_lang() -> str:
    """요청의 lang 쿼리 파라미터를 읽어 반환합니다. 기본값은 'ko'."""
    lang = request.args.get('lang', 'ko')
    return lang if lang in ('ko', 'en', 'ja', 'zh') else 'ko'


def translate_batch(texts: list, target_lang: str) -> list:
    """한국어 문자열 목록을 target_lang으로 번역합니다. 결과는 캐시에 저장됩니다."""
    if target_lang == 'ko' or not openai_api_key:
        return list(texts)

    result = [None] * len(texts)
    uncached_indices = []

    for i, text in enumerate(texts):
        cached = _translation_cache.get((text, target_lang))
        if cached is not None:
            result[i] = cached
        else:
            uncached_indices.append(i)

    if not uncached_indices:
        return result

    uncached_texts = [texts[i] for i in uncached_indices]
    lang_name = _LANG_NAMES.get(target_lang, 'English')
    model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')

    try:
        response = client.responses.create(
            model=model,
            input=[
                {
                    'role': 'system',
                    'content': (
                        f'Translate the following JSON array of Korean strings to {lang_name}. '
                        'Return only a valid JSON array of translated strings in the same order. '
                        'Use natural, concise phrasing for an e-commerce shopping app. '
                        'No explanation or markdown fences.'
                    )
                },
                {'role': 'user', 'content': json.dumps(uncached_texts, ensure_ascii=False)}
            ],
            temperature=0.1,
        )

        raw = (getattr(response, 'output_text', '') or '').strip()
        if raw.startswith('```'):
            raw = raw.split('\n', 1)[1].rsplit('```', 1)[0]

        translated = json.loads(raw)
        for i, idx in enumerate(uncached_indices):
            t_text = translated[i] if i < len(translated) else texts[idx]
            _translation_cache[(texts[idx], target_lang)] = t_text
            result[idx] = t_text

    except Exception:
        for idx in uncached_indices:
            result[idx] = texts[idx]

    return result


def translate_text(text: str, target_lang: str) -> str:
    """단일 한국어 문자열을 target_lang으로 번역합니다."""
    return translate_batch([text], target_lang)[0]


def build_ai_summary(product_reviews):
    if not product_reviews:
        return '아직 등록된 리뷰가 없습니다.'

    ratings = [review['rating'] for review in product_reviews]
    average = round(sum(ratings) / len(ratings), 1)
    positive_count = sum(1 for rating in ratings if rating >= 4)
    negative_count = sum(1 for rating in ratings if rating <= 2)

    if positive_count >= max(1, len(ratings) * 0.6):
        tone = '대체로 만족도가 높습니다.'
    elif negative_count >= max(1, len(ratings) * 0.4):
        tone = '개선이 필요하다는 의견이 있습니다.'
    else:
        tone = '의견이 다양하게 나타납니다.'

    return f'리뷰 {len(ratings)}개 기준 평균 {average}점이며, {tone}'


_NO_REVIEWS_MSG = {
    'ko': '아직 등록된 리뷰가 없습니다.',
    'en': 'No reviews yet.',
    'ja': 'まだレビューはありません。',
    'zh': '暂无评价。',
}

_SUMMARY_LANG_PROMPT = {
    'ko': '한국어로 2~3문장으로 간결하게 요약하고 핵심 장점/아쉬운 점을 균형 있게 작성하세요.',
    'en': 'Write a concise 2-3 sentence summary in English, balancing key strengths and shortcomings.',
    'ja': '日本語で2〜3文で簡潔にまとめ、主な長所と短所をバランスよく記述してください。',
    'zh': '用中文写2-3句简洁的摘要，均衡地描述主要优点和不足之处。',
}


def request_openai_review_summary(product, product_reviews, lang='ko'):
    if not product_reviews:
        return _NO_REVIEWS_MSG.get(lang, _NO_REVIEWS_MSG['ko'])

    if not openai_api_key:
        summary = build_ai_summary(product_reviews)
        return translate_text(summary, lang) if lang != 'ko' else summary

    model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
    reviews_text = '\n'.join(
        f"- 평점 {review['rating']}점 / 리뷰: {review.get('comment', '').strip() or '내용 없음'}"
        for review in product_reviews
    )

    try:
        response = client.responses.create(
            model=model,
            input=[
                {
                    'role': 'system',
                    'content': (
                        '당신은 이커머스 리뷰 요약 도우미입니다. '
                        + _SUMMARY_LANG_PROMPT.get(lang, _SUMMARY_LANG_PROMPT['en'])
                    )
                },
                {
                    'role': 'user',
                    'content': (
                        f"제품명: {product['name']}\n"
                        f"제품 설명: {product['description']}\n"
                        f"리뷰 목록:\n{reviews_text}\n\n"
                        '위 리뷰를 바탕으로 구매자가 빠르게 이해할 수 있는 요약을 작성해주세요.'
                    )
                }
            ],
            temperature=0.3,
            max_output_tokens=220,
        )

        output_text = getattr(response, 'output_text', None)
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        return build_ai_summary(product_reviews)
    except Exception:
        return build_ai_summary(product_reviews)

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    content_type = response.headers.get('Content-Type', '')
    if content_type and 'charset=' not in content_type.lower():
        response.headers['Content-Type'] = f'{content_type}; charset=utf-8'
    return response

# ----------------
# 웹 서비스 라우팅
# ----------------
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # 제품 상세 페이지 렌더링
    return send_from_directory(app.static_folder, 'product_detail.html')

@app.route('/<path:filename>')
def static_files(filename):
    # public/ 폴더의 정적 파일 서빙 (layout.js, components/ 등)
    return send_from_directory(app.static_folder, filename)

# ----------------
# API 라우팅
# ----------------
@app.route('/api/products', methods=['GET'])
def get_products():
    lang = get_request_lang()
    if lang == 'ko':
        return jsonify({'products': products})

    texts = []
    for p in products:
        texts.append(p['name'])
        texts.append(p['description'])

    translated = translate_batch(texts, lang)
    translated_products = [
        {**p, 'name': translated[i * 2], 'description': translated[i * 2 + 1]}
        for i, p in enumerate(products)
    ]
    return jsonify({'products': translated_products})

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    lang = get_request_lang()
    if lang == 'ko':
        return jsonify({'product': product})

    translated = translate_batch([product['name'], product['description']], lang)
    return jsonify({'product': {**product, 'name': translated[0], 'description': translated[1]}})

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    # reviews를 가져와서 반환
    return jsonify({'reviews': reviews})

@app.route('/api/reviews', methods=['POST'])
def create_review():
    # reviews에 저장
    data = request.get_json() or {}
    product_id = data.get('product_id')
    rating = data.get('rating')
    comment = (data.get('comment') or '').strip()

    if product_id is None or rating is None:
        return jsonify({'error': 'product_id와 rating은 필수입니다.'}), 400

    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return jsonify({'error': 'product_id는 숫자여야 합니다.'}), 400

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return jsonify({'error': 'rating은 1~5 사이의 숫자여야 합니다.'}), 400

    if rating < 1 or rating > 5:
        return jsonify({'error': 'rating은 1~5 사이여야 합니다.'}), 400

    review = {
        'product_id': product_id,
        'rating': rating,
        'comment': comment,
        'created_at': now_iso_utc()
    }
    reviews.append(review)

    return jsonify({'review': review}), 201


@app.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    lang = get_request_lang()
    product_reviews = [review for review in reviews if review.get('product_id') == product_id]
    average_rating = round(
        sum(review['rating'] for review in product_reviews) / len(product_reviews),
        1
    ) if product_reviews else None

    if lang != 'ko' and product_reviews:
        comments = [r.get('comment', '') for r in product_reviews]
        translated_comments = translate_batch(comments, lang)
        product_reviews = [
            {**r, 'comment': translated_comments[i]}
            for i, r in enumerate(product_reviews)
        ]

    return jsonify({
        'reviews': product_reviews,
        'average_rating': average_rating,
        'ai_summary': build_ai_summary(product_reviews)
    })


@app.route('/api/products/<int:product_id>/reviews', methods=['POST'])
def create_product_review(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json() or {}
    rating = data.get('rating')
    comment = (data.get('comment') or '').strip()

    if rating is None:
        return jsonify({'error': 'rating은 필수입니다.'}), 400

    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return jsonify({'error': 'rating은 1~5 사이의 숫자여야 합니다.'}), 400

    if rating < 1 or rating > 5:
        return jsonify({'error': 'rating은 1~5 사이여야 합니다.'}), 400

    review = {
        'product_id': product_id,
        'rating': rating,
        'comment': comment,
        'created_at': now_iso_utc()
    }
    reviews.append(review)
    return jsonify({'review': review}), 201


@app.route('/api/products/<int:product_id>/ai-summary', methods=['GET'])
def get_product_ai_summary(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product_reviews = [review for review in reviews if review.get('product_id') == product_id]
    average_rating = round(
        sum(review['rating'] for review in product_reviews) / len(product_reviews),
        1
    ) if product_reviews else None
    lang = get_request_lang()
    ai_summary_text = request_openai_review_summary(product, product_reviews, lang)

    return jsonify({
        'ai_summary': ai_summary_text,
        'average_rating': average_rating,
        'review_count': len(product_reviews)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)