"""
고시문 멀티에이전트 인사이트 생성기.

파이프라인:
  1단계 (전문가 패널) — 도시계획 교수·실전 투자자·생활 전문가 각각 분석 (Haiku)
  2단계 (편집장 통합) — 세 분석을 하나의 블로그 포스트 JSON으로 합성 (Sonnet)

정적 컨텍스트(페르소나·정책 레퍼런스·출력 형식)는 편집장 단계에서 프롬프트 캐싱으로 재사용됩니다.
매 고시문마다 토큰 사용량을 data/usage_log.jsonl에 기록합니다.

Env var: ANTHROPIC_API_KEY
"""
import os
import json
from datetime import datetime, timezone

import anthropic

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USAGE_LOG_PATH = os.path.join(DATA_DIR, "usage_log.jsonl")

SPECIALIST_MODEL = "claude-haiku-4-5"
EDITOR_MODEL = "claude-sonnet-5"

# 편집장이 최종 생성할 필드 스키마
OUTPUT_FORMAT = """{
  "hook": "독자의 관심을 끄는 도입부 1~2문장. 질문형으로 열거나, 고시 내용에 실제로 적힌 사실로 시작. 흥미를 위해 연수·규모 같은 수치를 지어내지 말 것 ('40년 가까이', '수십 년째' 등 근거 없는 표현 금지)",
  "summary": "이 고시가 무엇인지 쉽게 풀어쓴 설명. 3~5문장.",
  "background": "이 고시가 나오게 된 배경. 해당 지역의 맥락, 개발 흐름, 왜 지금 이 결정이 나왔는지. 3~5문장.",
  "key_changes": "핵심 변경 내용. 용적률·건폐율·높이 등 수치 포함. 3~5문장.",
  "key_stats": [
    {"label": "위치", "value": "구체적 주소 또는 지역명"},
    {"label": "수치 항목명 (예: 용적률, 부지면적, 세대수 등)", "value": "구체적 수치"},
    {"label": "수치 항목명 2", "value": "구체적 수치"},
    {"label": "예상 완공 또는 시행 시기", "value": "연도 또는 기간"}
  ],
  "impact_residents": [
    "주민 생활 영향 포인트 1 — 구체적으로",
    "포인트 2",
    "포인트 3"
  ],
  "impact_realestate": [
    "부동산 시장 영향 포인트 1 — 객관적 팩트만",
    "포인트 2",
    "포인트 3"
  ],
  "expert_quotes": [
    {"role": "도시계획 전문가", "quote": "이 고시의 법적·기술적 핵심 의미를 담은 한 문장"},
    {"role": "부동산 전문가", "quote": "시장 영향에 대한 객관적 핵심 한 문장"},
    {"role": "생활 전문가", "quote": "주민 관점의 핵심 한 문장"}
  ],
  "policy_context": "관련 정책과의 연결. 관련 없으면 null. 있으면 3~4문장.",
  "timeline": "향후 예상 일정. 남은 절차, 예상 소요 기간. 2~3문장.",
  "faq": [
    {"q": "이 고시를 접한 독자가 가장 궁금해할 질문 1", "a": "구체적이고 명확한 답변 2~3문장"},
    {"q": "질문 2", "a": "답변"},
    {"q": "질문 3", "a": "답변"}
  ],
  "keywords": ["핵심", "키워드", "3~7개"]
}"""


# ─── 파일 로더 ────────────────────────────────────────────────────────────────

def _read_prompt_file(filename: str) -> str:
    path = os.path.join(PROMPTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _response_text(message) -> str:
    """응답에서 텍스트만 추출. Sonnet 5는 thinking 블록을 함께 반환한다."""
    return "".join(b.text for b in message.content if b.type == "text").strip()


# ─── 고시문 정보 포매터 ───────────────────────────────────────────────────────

def _record_summary(record: dict) -> str:
    """고시문 메타데이터 요약 (전문가·편집장 공통 입력)."""
    return f"""고시번호: {record.get('notice_no', '')}
고시일자: {record.get('notice_date', '')}
고시기관: {record.get('organ_name', '')}
고시유형: {record.get('notice_type', '')}
위치: {record.get('location', '')}
중심지 등급: {record.get('center_grade', '')}
중심지: {record.get('center_name', '')}
제목: {record.get('title', '')}"""


# ─── 1단계: 전문가 분석 ───────────────────────────────────────────────────────

_SPECIALIST_FOCUS = {
    "persona_urban_planner.md": (
        "위 고시문을 도시계획 전문가 관점에서 분석해주세요.\n"
        "다음을 중심으로 작성하세요:\n"
        "- 법적·기술적 의미 (용도지역, 용적률, 높이 제한 등)\n"
        "- 2040 서울플랜·상위 계획과의 연결\n"
        "- 역사적 맥락과 후속 계획 전망\n"
        "200~400자 분량의 분석문으로 작성하세요."
    ),
    "persona_investor.md": (
        "위 고시문을 실전 투자자 관점에서 분석해주세요.\n"
        "다음을 중심으로 작성하세요:\n"
        "- 주변 시세에 미칠 영향 (객관적 팩트만)\n"
        "- 과거 유사 사례와의 비교\n"
        "- 수혜 예상 지역 vs 규제 강화 지역\n"
        "투자 권유 없이, 200~400자 분량으로 작성하세요."
    ),
    "persona_resident.md": (
        "위 고시문을 지역 생활 전문가 관점에서 분석해주세요.\n"
        "다음을 중심으로 작성하세요:\n"
        "- 공사 기간 주민 불편 (소음, 교통, 주차)\n"
        "- 완공 후 생활 변화 (교통, 학교, 상권, 공원)\n"
        "- 취약계층 영향\n"
        "200~400자 분량으로 작성하세요."
    ),
}


def _run_specialist(client: anthropic.Anthropic, record: dict, persona_file: str) -> str:
    """단일 전문가 분석 실행. 결과는 텍스트."""
    persona = _read_prompt_file(persona_file)
    focus = _SPECIALIST_FOCUS[persona_file]
    user_content = f"""## 고시문 정보
{_record_summary(record)}

## 고시 내용
{record.get('content', '내용 없음')}

## 분석 요청
{focus}"""

    message = client.messages.create(
        model=SPECIALIST_MODEL,
        max_tokens=600,
        system=persona,
        messages=[{"role": "user", "content": user_content}],
    )
    return _response_text(message)


# ─── 2단계: 편집장 통합 ───────────────────────────────────────────────────────

def _build_editor_system() -> list[dict]:
    """편집장 시스템 프롬프트. 정적이므로 캐시 블록으로 구성."""
    persona = _read_prompt_file("expert_persona.md")
    policy_ref = _read_prompt_file("policy_reference.md")
    text = f"""{persona}

당신은 도시계획·부동산·생활 전문가 3인의 분석을 받아 하나의 블로그 포스트로 엮는 편집장입니다.
각 전문가의 관점을 살리되 모순 없이 통합하고, 일반 독자가 쉽게 읽을 수 있도록 작성하세요.
단순히 세 분석을 이어붙이지 말고, 그 안에서 서로 겹치거나 부딪히는 지점을 찾아 하나의 관점으로 정리하세요 — 그것이 이 포스트가 주는 진짜 인사이트입니다.

## 문체 규칙 — 사람이 쓴 것처럼
- 문장 길이에 리듬을 준다: 단정적인 짧은 문장과 근거를 설명하는 긴 문장을 섞는다. 모든 필드에서 문장 구조를 반복하지 않는다.
- "이는 ~것으로 보인다", "~할 전망이다", "시사하는 바가 크다", "주목할 만하다", "결론적으로" 같은 AI 상투구를 쓰지 않는다. 구체적 서술로 대체한다.
- 같은 문장 시작 패턴(주어+서술어 나열, "첫째/둘째/셋째" 식 기계적 병렬)을 반복하지 않는다.
- 각 필드 안에서 사실 나열에 그치지 말고 인과관계·비교·맥락을 최소 한 번은 짚는다 (단, 근거는 고시 내용·정책 레퍼런스·전문가 분석 안에 있을 때만 사용).
- 과장된 수식어("혁신적인", "획기적인")나 근거 없는 추정 표현을 피한다. 확신이 없으면 문장 자체를 빼거나 조건을 명시한다.

## 사실 검증 — 발행 전 마지막 관문
당신은 이 글의 마지막 검수자입니다. 전문가 분석에 아래가 섞여 있으면 **그대로 옮기지 말고 삭제하거나 일반적 서술로 바꾸세요.**
- **연도·지명·기업명이 붙은 구체적 과거 사례** ("2019년 강남구 OO부지 개발 사례를 보면~"). 전문가가 기억에 의존해 지어낸 것일 가능성이 높습니다. 고유명사 없는 일반적 패턴 서술로 바꾸세요.
- **고시 내용에 없는 수치** — 면적·세대수·용적률·사업비·공사기간. "약 3만 평대로 추정" 같은 표현이 보이면 삭제하세요.
- `key_stats`에는 **고시 내용에 명시적으로 적힌 값만** 넣습니다. 채울 항목이 부족하면 항목 수를 줄이세요 — 빈칸을 추정으로 메우지 마세요.
- 고시문이 다루지 않는 후속 절차의 소요 기간을 단정하지 마세요 ("통상 1~2년" 등은 근거가 있을 때만).

원문·전문가 분석에 근거가 없는 사실은, 글이 빈약해지더라도 쓰지 않습니다.

## 참고: 서울시 정책 컨텍스트

{policy_ref}

## 출력 형식 (반드시 JSON으로만 응답)

{OUTPUT_FORMAT}

반드시 JSON만 출력하세요. 다른 텍스트는 포함하지 마세요."""
    return [
        {
            "type": "text",
            "text": text,
            "cache_control": {"type": "ephemeral"},
        }
    ]


def _run_editor(
    client: anthropic.Anthropic,
    record: dict,
    planner_analysis: str,
    investor_analysis: str,
    resident_analysis: str,
) -> tuple[dict, object]:
    """편집장이 3개 분석을 통합해 최종 OUTPUT_FORMAT JSON 반환."""
    system_blocks = _build_editor_system()
    user_content = f"""## 고시문 정보
{_record_summary(record)}

## 고시 내용
{record.get('content', '내용 없음')}

---

## [도시계획 교수 분석]
{planner_analysis}

## [실전 투자자 분석]
{investor_analysis}

## [생활 전문가 분석]
{resident_analysis}

---

위 세 전문가의 분석을 통합하여 OUTPUT_FORMAT JSON을 작성해주세요."""

    message = client.messages.create(
        model=EDITOR_MODEL,
        max_tokens=16000,
        system=system_blocks,
        messages=[{"role": "user", "content": user_content}],
    )
    return _response_text(message), message.usage


# ─── 사용량 로깅 ─────────────────────────────────────────────────────────────

def _log_usage(record: dict, usage, specialist_calls: int) -> None:
    """토큰 사용량을 콘솔에 출력하고 data/usage_log.jsonl 에 append."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "notice_no": record.get("notice_no", ""),
        "specialist_model": SPECIALIST_MODEL,
        "editor_model": EDITOR_MODEL,
        "specialist_calls": specialist_calls,
        "editor_input_tokens": getattr(usage, "input_tokens", 0),
        "editor_output_tokens": getattr(usage, "output_tokens", 0),
        "editor_cache_creation": getattr(usage, "cache_creation_input_tokens", 0),
        "editor_cache_read": getattr(usage, "cache_read_input_tokens", 0),
    }
    print(
        f"    [편집장] in={entry['editor_input_tokens']} out={entry['editor_output_tokens']} "
        f"cache(w/r)={entry['editor_cache_creation']}/{entry['editor_cache_read']}"
    )
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(USAGE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"    사용량 로그 기록 실패: {e}")


# ─── 공개 인터페이스 ─────────────────────────────────────────────────────────

def generate_insight(record: dict) -> dict | None:
    """고시문 레코드에 대해 멀티에이전트 인사이트를 생성합니다.

    1단계: 도시계획 교수·실전 투자자·생활 전문가 각각 분석 (Haiku)
    2단계: 편집장이 세 분석을 OUTPUT_FORMAT JSON으로 통합 (Sonnet)

    Returns:
        OUTPUT_FORMAT 스키마를 따르는 dict. 실패 시 None.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("    ANTHROPIC_API_KEY 미설정 — 인사이트 생략")
        return None

    client = anthropic.Anthropic(api_key=api_key)

    # ── 1단계: 전문가 패널 ──────────────────────────────────────────────────
    specialists = [
        "persona_urban_planner.md",
        "persona_investor.md",
        "persona_resident.md",
    ]
    analyses = {}
    for persona_file in specialists:
        label = persona_file.replace("persona_", "").replace(".md", "")
        try:
            print(f"    [{label}] 분석 중...")
            analyses[persona_file] = _run_specialist(client, record, persona_file)
        except Exception as e:
            print(f"    [{label}] 분석 실패: {e}")
            analyses[persona_file] = "(분석 실패)"

    # ── 2단계: 편집장 통합 ──────────────────────────────────────────────────
    try:
        print("    [편집장] 통합 중...")
        raw, usage = _run_editor(
            client,
            record,
            planner_analysis=analyses["persona_urban_planner.md"],
            investor_analysis=analyses["persona_investor.md"],
            resident_analysis=analyses["persona_resident.md"],
        )
        _log_usage(record, usage, specialist_calls=len(specialists))

        # 마크다운 코드블록 제거
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            raw = raw.rsplit("```", 1)[0].strip()
        insight = json.loads(raw)

        # 필수 필드 검증
        for key in ("summary", "impact_residents", "impact_realestate", "keywords", "faq", "expert_quotes"):
            if key not in insight:
                print(f"    인사이트 필드 누락: {key}")
                return None

        return insight

    except json.JSONDecodeError as e:
        print(f"    편집장 JSON 파싱 실패: {e}")
        return None
    except Exception as e:
        print(f"    편집장 통합 실패: {e}")
        return None
