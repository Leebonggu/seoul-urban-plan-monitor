"""보도자료 → WordPress HTML 렌더러.

상단: LLM 인트로(요약) | 본문: 원문 #scrabArea HTML | 하단: 첨부/출처/쿠팡 배너
"""
import os
import logging

import anthropic

from wp_blog_template import _COUPANG_BANNER_2

logger = logging.getLogger(__name__)

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
INTRO_MODEL = "claude-sonnet-5"
INTRO_MAX_TOKENS = 700


def _read_intro_prompt() -> str:
    path = os.path.join(PROMPTS_DIR, "press_release_intro.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _strip_html_to_text(body_html: str) -> str:
    """LLM 입력용 단순 텍스트 추출 (BeautifulSoup 사용)."""
    from bs4 import BeautifulSoup
    return BeautifulSoup(body_html, "lxml").get_text("\n", strip=True)


def generate_intro(record: dict) -> str | None:
    """LLM으로 인트로 문단 생성. 실패 시 None."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        logger.warning("ANTHROPIC_API_KEY 미설정 — 인트로 생략")
        return None

    body_text = _strip_html_to_text(record.get("body_html", ""))
    if not body_text:
        return None

    user_content = (
        f"## 보도자료 메타\n"
        f"제목: {record.get('title', '')}\n"
        f"등록일: {record.get('reg_date', '')}\n"
        f"담당부서: {record.get('dept', '')}\n"
        f"분류: {record.get('category', '')}\n\n"
        f"## 본문\n{body_text}"
    )

    try:
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model=INTRO_MODEL,
            max_tokens=INTRO_MAX_TOKENS,
            system=_read_intro_prompt(),
            messages=[{"role": "user", "content": user_content}],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        logger.error(f"인트로 생성 실패: {e}")
        return None


def _h2(text: str) -> str:
    return (
        f'<h2 style="font-size:19px;font-weight:700;color:#111827;margin:0 0 16px;'
        f'padding-left:12px;border-left:4px solid #3b82f6;line-height:1.4;">{text}</h2>'
    )


def _divider() -> str:
    return '<hr style="border:none;border-top:1px solid #e5e7eb;margin:0 0 36px;">'


def render(record: dict, intro: str | None = None) -> dict:
    """보도자료 레코드 → {title, html, excerpt} 반환."""
    title_raw = record.get("title", "").strip()
    # 머리말 정리: (석간), (조간), (자료제공), (엠바고...) 등 제거
    import re
    title_clean = re.sub(r"^\(?[가-힣\d시분 ]{1,12}\)\s*", "", title_raw).strip() or title_raw
    title_clean = re.sub(r"^\([^)]+\)\s*", "", title_clean).strip() or title_raw
    if len(title_clean) > 60:
        title_display = title_clean[:57] + "..."
    else:
        title_display = title_clean
    title = f"[서울시 보도자료] {title_display} ({record.get('reg_date','')})"

    p = []

    # ── 인트로 (LLM 요약) ───────────────────────────────────────────────────
    if intro:
        p.append(
            '<div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;'
            'padding:22px 26px;border-radius:10px;margin-bottom:36px;">'
            f'<p style="margin:0;font-size:16px;line-height:1.85;font-weight:500;">'
            f'{intro}</p>'
            '</div>'
        )
        excerpt = intro[:160]
    else:
        excerpt = (
            f"{record.get('reg_date','')} 서울시 보도자료. "
            f"{record.get('dept','')} | 분류: {record.get('category','')}"
        )

    # ── 메타 박스 ───────────────────────────────────────────────────────────
    p.append('<table style="width:100%;border-collapse:collapse;margin-bottom:32px;font-size:14px;">')
    rows = [
        ("등록일", record.get("reg_date", "")),
        ("담당부서", record.get("dept", "")),
        ("분류", record.get("category", "")),
    ]
    if record.get("contact"):
        rows.append(("문의", record["contact"]))
    for label, value in rows:
        p.append(
            '<tr>'
            f'<td style="padding:10px 14px;border:1px solid #e5e7eb;background:#f9fafb;'
            f'font-weight:600;width:120px;color:#374151;">{label}</td>'
            f'<td style="padding:10px 14px;border:1px solid #e5e7eb;color:#374151;">{value}</td>'
            '</tr>'
        )
    p.append('</table>')
    p.append(_divider())

    # ── 본문 (원문 HTML) ───────────────────────────────────────────────────
    p.append(_h2("📰 보도자료 전문"))
    p.append(
        '<div style="font-size:15px;line-height:1.95;color:#374151;'
        'padding:24px 26px;background:#fafafa;border:1px solid #e5e7eb;'
        'border-radius:8px;margin-bottom:36px;">'
        f'{record.get("body_html", "")}'
        '</div>'
    )

    # ── 첨부파일 ───────────────────────────────────────────────────────────
    attachments = record.get("attachments", [])
    if attachments:
        p.append(_h2("📎 첨부파일"))
        p.append('<ul style="margin-bottom:32px;line-height:2.0;font-size:14px;">')
        for a in attachments:
            p.append(
                f'<li><a href="{a["url"]}" target="_blank" rel="noopener">{a["name"]}</a></li>'
            )
        p.append('</ul>')
        p.append(_divider())

    # ── 관련 링크 ───────────────────────────────────────────────────────────
    p.append(_h2("🔗 관련 링크"))
    p.append(
        '<ul style="margin-bottom:24px;line-height:2.2;font-size:14px;">'
        f'<li><a href="{record.get("page_url","")}" target="_blank" rel="noopener">'
        '📌 서울시 원문 보기</a></li>'
        '<li><a href="https://2lee.kr/category/seoul-gosi/" target="_blank" rel="noopener">'
        '📚 관련 고시문 모음</a></li>'
        '</ul>'
    )

    # ── 쿠팡 배너 ───────────────────────────────────────────────────────────
    p.append(
        '<div style="margin-bottom:16px;">'
        '<p style="font-size:12px;color:#9ca3af;margin:0 0 8px;">'
        '이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.'
        '</p>'
        f'{_COUPANG_BANNER_2}'
        '</div>'
    )

    # ── 출처 ───────────────────────────────────────────────────────────────
    p.append('<hr style="margin:32px 0 16px;border:none;border-top:1px solid #e5e7eb;">')
    p.append(
        '<p style="font-size:12px;color:#9ca3af;">출처: 서울특별시 보도자료 '
        f'(등록일 {record.get("reg_date","")} | {record.get("dept","")}) — '
        f'<a href="{record.get("page_url","")}" target="_blank" rel="noopener">원문 보기</a></p>'
    )

    return {"title": title, "html": "\n".join(p), "excerpt": excerpt}
