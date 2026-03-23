"""
고시문 LLM 인사이트 생성기.

Claude Sonnet API를 사용하여 고시문의 요약, 영향분석, 정책 연결, 키워드를 생성합니다.
Env var: ANTHROPIC_API_KEY
"""
import os
import json
import anthropic

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

SYSTEM_PROMPT = """당신은 서울시 도시계획 전문 분석가입니다.
아래 고시문을 일반 시민이 이해할 수 있도록 분석해주세요.

## 출력 형식 (반드시 JSON으로 응답)

{
  "summary": "이 고시가 무엇인지 2~3줄 요약",
  "impact": "주변 부동산·생활에 미칠 영향 1~2줄",
  "policy_context": "관련 정책(2040 서울플랜, 강북전성시대 2.0, 서남권 대개조 2.0)과의 연결고리. 관련 없으면 null",
  "keywords": ["추출된", "핵심", "키워드", "목록"]
}

## 규칙
- summary: 전문용어를 피하고 "이 고시는 ~하는 내용입니다" 형식
- impact: "이 지역 주민에게는 ~", "부동산 관점에서는 ~" 등 실생활 관점
- policy_context: 아래 정책 레퍼런스에서 관련 내용이 있을 때만 작성. 억지로 연결하지 마세요.
- keywords: 고시문에서 추출한 도시계획 핵심 키워드 3~7개 (재건축, 용적률, 지구단위계획 등)
- 정치적 판단이나 투자 권유는 하지 마세요
- 반드시 JSON만 출력하세요. 다른 텍스트는 포함하지 마세요."""


def _load_policy_reference() -> str:
    path = os.path.join(PROMPTS_DIR, "policy_reference.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _build_user_prompt(record: dict, policy_ref: str) -> str:
    return f"""## 고시문 정보
- 고시번호: {record.get('notice_no', '')}
- 고시일자: {record.get('notice_date', '')}
- 고시기관: {record.get('organ_name', '')}
- 고시유형: {record.get('notice_type', '')}
- 위치: {record.get('location', '')}
- 중심지 등급: {record.get('center_grade', '')}
- 중심지: {record.get('center_name', '')}
- 제목: {record.get('title', '')}

## 고시 내용
{record.get('content', '내용 없음')}

## 정책 레퍼런스
{policy_ref}"""


def generate_insight(record: dict) -> dict | None:
    """고시문 레코드에 대한 LLM 인사이트를 생성합니다.

    Returns:
        {"summary": str, "impact": str, "policy_context": str|None, "keywords": list[str]}
        실패 시 None
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("    ANTHROPIC_API_KEY 미설정 — 인사이트 생략")
        return None

    policy_ref = _load_policy_reference()
    user_prompt = _build_user_prompt(record, policy_ref)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw = message.content[0].text.strip()
        # 마크다운 코드블록 제거
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]  # 첫 줄 (```json) 제거
            raw = raw.rsplit("```", 1)[0].strip()
        insight = json.loads(raw)

        # 필수 필드 검증
        for key in ("summary", "impact", "keywords"):
            if key not in insight:
                print(f"    인사이트 필드 누락: {key}")
                return None

        return insight

    except json.JSONDecodeError as e:
        print(f"    인사이트 JSON 파싱 실패: {e}")
        return None
    except Exception as e:
        print(f"    인사이트 생성 실패: {e}")
        return None
