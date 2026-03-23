def generate_wp_content(record: dict, insight: dict | None = None) -> dict:
    """고시문 레코드를 WordPress HTML 포스트로 변환.

    Args:
        record: 고시문 레코드
        insight: LLM 인사이트 (summary, impact, policy_context, keywords)
    """
    location = record.get("location") or ""
    center_grade = record.get("center_grade")
    center_name = record.get("center_name")
    doc_url = record.get("doc_url") or ""
    page_url = record.get("page_url") or ""
    content = record.get("content") or "상세 내용은 원문을 확인해주세요."
    notice_type = record.get("notice_type") or "도시계획"

    # SEO 최적화 제목: [범주·지역] 고시제목 (날짜)
    title_location = location.split(" ")[0] if location else record.get("organ_name", "서울")
    record_category = record.get("category", "결정고시")
    category_prefix = "지구단위" if record_category == "지구단위계획" else ""
    raw_title = record["title"]
    if len(raw_title) > 50:
        raw_title = raw_title[:47] + "..."
    if category_prefix:
        title = f"[{category_prefix}·{title_location}] {raw_title} ({record['notice_date']})"
    else:
        title = f"[{title_location}] {raw_title} ({record['notice_date']})"

    # 요약문 (excerpt)
    excerpt_parts = []
    category_label = f"[{record_category}] " if record_category != "결정고시" else ""
    excerpt_parts.append(f"{category_label}{record['notice_date']} {record['organ_name']} {notice_type} 고시.")
    if location:
        excerpt_parts.append(f"위치: {location}.")
    if center_grade and center_name:
        excerpt_parts.append(f"2040 서울플랜 {center_grade} — {center_name}.")
    excerpt = " ".join(excerpt_parts)

    # HTML 본문 생성
    parts = []

    # 요약 박스
    parts.append('<div style="background:#f0f7ff;border-left:4px solid #3b82f6;padding:16px;border-radius:4px;margin-bottom:24px;">')
    parts.append(f'<p style="margin:0;font-size:15px;line-height:1.6;">{excerpt}</p>')
    parts.append('</div>')

    # AI 인사이트 섹션
    if insight:
        parts.append('<div style="background:#fffbeb;border-left:4px solid #f59e0b;padding:16px;border-radius:4px;margin-bottom:24px;">')
        parts.append('<h2 style="margin:0 0 12px;font-size:18px;color:#92400e;">💡 AI 해설</h2>')

        if insight.get("summary"):
            parts.append(f'<p style="margin:0 0 10px;line-height:1.7;font-size:15px;">{insight["summary"]}</p>')

        if insight.get("impact"):
            parts.append(f'<p style="margin:0 0 10px;line-height:1.7;font-size:15px;"><strong>영향 분석:</strong> {insight["impact"]}</p>')

        if insight.get("policy_context"):
            parts.append(f'<p style="margin:0 0 10px;line-height:1.7;font-size:15px;"><strong>관련 정책:</strong> {insight["policy_context"]}</p>')

        if insight.get("keywords"):
            tags = " ".join(f'<span style="display:inline-block;background:#fef3c7;color:#92400e;padding:2px 8px;border-radius:12px;font-size:13px;margin:2px;">{kw}</span>' for kw in insight["keywords"])
            parts.append(f'<p style="margin:0;">{tags}</p>')

        parts.append('</div>')

    # 기본정보 테이블
    parts.append('<h2>📋 고시 기본정보</h2>')
    parts.append('<table style="width:100%;border-collapse:collapse;margin-bottom:24px;">')
    info_rows = [
        ("고시번호", record["notice_no"]),
        ("고시일자", record["notice_date"]),
        ("고시기관", record["organ_name"]),
        ("고시유형", notice_type),
    ]
    if location:
        info_rows.append(("위치", location))
    if center_grade and center_name:
        info_rows.append(("2040 서울플랜 중심지", f"{center_grade} — {center_name}"))

    for label, value in info_rows:
        parts.append(
            f'<tr>'
            f'<td style="padding:8px 12px;border:1px solid #e5e7eb;background:#f9fafb;font-weight:bold;width:140px;">{label}</td>'
            f'<td style="padding:8px 12px;border:1px solid #e5e7eb;">{value}</td>'
            f'</tr>'
        )
    parts.append('</table>')

    # 고시 내용
    parts.append('<h2>📄 고시 내용</h2>')
    formatted_content = content.replace("\n", "<br>")
    parts.append(f'<div style="line-height:1.8;padding:16px;background:#fafafa;border-radius:4px;margin-bottom:24px;">{formatted_content}</div>')

    # 관련 링크
    if page_url or doc_url:
        parts.append('<h2>🔗 관련 링크</h2>')
        parts.append('<ul style="margin-bottom:24px;">')
        if page_url:
            parts.append(f'<li><a href="{page_url}" target="_blank" rel="noopener">📌 상세 페이지 (서울도시공간포털)</a></li>')
        if doc_url:
            parts.append(f'<li><a href="{doc_url}" target="_blank" rel="noopener">📎 원문 다운로드 (PDF)</a></li>')
        parts.append('</ul>')

    # 출처
    parts.append('<hr style="margin:32px 0 16px;">')
    parts.append('<p style="font-size:12px;color:#999;">데이터 출처: <a href="https://urban.seoul.go.kr" target="_blank" rel="noopener">서울도시공간포털</a> (urban.seoul.go.kr)</p>')

    html = "\n".join(parts)
    return {"title": title, "html": html, "excerpt": excerpt}
