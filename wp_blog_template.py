def generate_wp_content(record: dict) -> dict:
    """고시문 레코드를 WordPress HTML 포스트로 변환."""
    location = record.get("location") or ""
    center_grade = record.get("center_grade")
    center_name = record.get("center_name")
    doc_url = record.get("doc_url") or ""
    page_url = record.get("page_url") or ""
    content = record.get("content") or "상세 내용은 원문을 확인해주세요."

    # SEO 최적화 제목: [지역] 키워드 결정고시 (날짜)
    title_location = location.split(" ")[0] if location else record.get("organ_name", "서울")
    title = f"{title_location} {record['notice_type']} 결정고시 ({record['notice_date']}) — {record['title']}"
    if len(title) > 100:
        title = title[:97] + "..."

    # HTML 본문 생성
    parts = []

    # 기본정보 테이블
    parts.append('<div style="background:#f8f9fa;padding:16px;border-radius:8px;margin-bottom:20px;">')
    parts.append(f'<p><strong>고시번호:</strong> {record["notice_no"]}</p>')
    parts.append(f'<p><strong>고시일자:</strong> {record["notice_date"]}</p>')
    parts.append(f'<p><strong>고시기관:</strong> {record["organ_name"]}</p>')
    if location:
        parts.append(f'<p><strong>위치:</strong> {location}</p>')
    parts.append(f'<p><strong>고시유형:</strong> {record["notice_type"]}</p>')
    if center_grade and center_name:
        parts.append(f'<p><strong>2040 서울플랜 중심지:</strong> {center_grade} — {center_name}</p>')
    parts.append('</div>')

    # 고시 내용
    parts.append('<h2>고시 내용</h2>')
    # 줄바꿈을 <br>로 변환
    formatted_content = content.replace("\n", "<br>")
    parts.append(f'<div style="line-height:1.8;">{formatted_content}</div>')

    # 이미지 삽입 위치 (placeholder — publish_daily.py에서 교체)
    parts.append('<!-- IMAGES_PLACEHOLDER -->')

    # 관련 링크
    parts.append('<h2>관련 링크</h2>')
    parts.append('<ul>')
    if page_url:
        parts.append(f'<li><a href="{page_url}" target="_blank">상세 페이지 (서울도시공간포털)</a></li>')
    if doc_url:
        parts.append(f'<li><a href="{doc_url}" target="_blank">원문 다운로드</a></li>')
    parts.append('</ul>')

    # 출처
    parts.append('<hr>')
    parts.append('<p style="font-size:12px;color:#999;">출처: 서울도시공간포털 (urban.seoul.go.kr)</p>')

    html = "\n".join(parts)
    return {"title": title, "html": html}
