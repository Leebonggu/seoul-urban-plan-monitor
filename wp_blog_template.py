import re as _re


def _bold_numbers(text: str) -> str:
    """숫자+단위 조합을 <strong>으로 강조."""
    return _re.sub(
        r'(\d[\d,\.]*\s*(?:년|개월|개|층|㎡|만㎡|km|m|%|조|억|만|세대|호|차로|개역|거점|곳))',
        r'<strong>\1</strong>',
        text,
    )


def _h2(text: str) -> str:
    return (
        f'<h2 style="font-size:19px;font-weight:700;color:#111827;margin:0 0 16px;'
        f'padding-left:12px;border-left:4px solid #3b82f6;line-height:1.4;">{text}</h2>'
    )


def _divider() -> str:
    return '<hr style="border:none;border-top:1px solid #e5e7eb;margin:0 0 36px;">'


def generate_wp_content(record: dict, insight: dict | None = None) -> dict:
    """고시문 레코드를 WordPress HTML 포스트로 변환."""
    location    = record.get("location") or ""
    center_grade = record.get("center_grade")
    center_name  = record.get("center_name")
    doc_url  = record.get("doc_url") or ""
    page_url = record.get("page_url") or ""
    content      = record.get("content") or "상세 내용은 원문을 확인해주세요."
    notice_type  = record.get("notice_type") or "도시계획"

    title_location = location.split(" ")[0] if location else record.get("organ_name", "서울")
    raw_title = record["title"]
    if len(raw_title) > 50:
        raw_title = raw_title[:47] + "..."
    title = f"{title_location} {raw_title} — 핵심 분석과 영향 정리 ({record['notice_date']})"

    if insight and insight.get("hook"):
        excerpt = insight["hook"]
    else:
        parts_ex = [f"{record['notice_date']} {record['organ_name']} {notice_type} 고시."]
        if location:
            parts_ex.append(f"위치: {location}.")
        if center_grade and center_name:
            parts_ex.append(f"2040 서울플랜 {center_grade} — {center_name}.")
        excerpt = " ".join(parts_ex)

    p = []   # HTML parts

    # ── Hook 배너 ────────────────────────────────────────────────────────────
    if insight and insight.get("hook"):
        p.append(
            '<div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;'
            'padding:26px 30px;border-radius:10px;margin-bottom:40px;">'
            f'<p style="margin:0;font-size:18px;line-height:1.8;font-weight:500;">'
            f'{insight["hook"]}</p>'
            '</div>'
        )

    # ── 핵심 수치 카드 ────────────────────────────────────────────────────────
    stats = insight.get("key_stats") if insight else None
    if stats:
        p.append(_h2("📊 핵심 수치"))
        p.append(
            '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));'
            'gap:10px;margin-bottom:40px;">'
        )
        for s in stats:
            p.append(
                '<div style="background:#f0f7ff;border:1px solid #bfdbfe;border-radius:8px;'
                'padding:16px 12px;text-align:center;">'
                f'<div style="font-size:11px;color:#6b7280;text-transform:uppercase;'
                f'letter-spacing:.04em;margin-bottom:8px;">{s["label"]}</div>'
                f'<div style="font-size:17px;font-weight:800;color:#1e40af;line-height:1.3;">'
                f'{s["value"]}</div>'
                '</div>'
            )
        p.append('</div>')
        p.append(_divider())

    # ── 요약 ─────────────────────────────────────────────────────────────────
    if insight and insight.get("summary"):
        p.append(_h2("🔍 한눈에 보는 고시 내용"))
        p.append(
            f'<p style="font-size:15px;line-height:1.95;color:#374151;margin-bottom:40px;">'
            f'{_bold_numbers(insight["summary"])}</p>'
        )
        p.append(_divider())

    # ── 배경 ─────────────────────────────────────────────────────────────────
    if insight and insight.get("background"):
        p.append(_h2("📌 이 고시가 나온 배경"))
        p.append(
            f'<p style="font-size:15px;line-height:1.95;color:#374151;margin-bottom:40px;">'
            f'{_bold_numbers(insight["background"])}</p>'
        )
        p.append(_divider())

    # ── 핵심 변경 ────────────────────────────────────────────────────────────
    if insight and insight.get("key_changes"):
        p.append(_h2("⚡ 무엇이 달라지나?"))
        p.append(
            f'<p style="font-size:15px;line-height:1.95;color:#374151;margin-bottom:40px;">'
            f'{_bold_numbers(insight["key_changes"])}</p>'
        )
        p.append(_divider())

    # ── 주민 영향 (bullet) ────────────────────────────────────────────────────
    if insight and insight.get("impact_residents"):
        p.append(_h2("🏘️ 주민 생활에 미치는 영향"))
        items = insight["impact_residents"]
        if isinstance(items, list):
            p.append('<ul style="padding-left:0;list-style:none;margin-bottom:40px;">')
            for item in items:
                p.append(
                    '<li style="display:flex;gap:10px;align-items:flex-start;'
                    'margin-bottom:12px;font-size:15px;line-height:1.8;color:#374151;">'
                    '<span style="color:#3b82f6;font-weight:700;flex-shrink:0;margin-top:2px;">▸</span>'
                    f'<span>{_bold_numbers(item)}</span></li>'
                )
            p.append('</ul>')
        else:
            p.append(
                f'<p style="font-size:15px;line-height:1.95;color:#374151;margin-bottom:40px;">'
                f'{_bold_numbers(items)}</p>'
            )
        p.append(_divider())

    # ── 부동산 영향 (bullet) ──────────────────────────────────────────────────
    if insight and insight.get("impact_realestate"):
        p.append(_h2("🏢 부동산 시장 영향 분석"))
        items = insight["impact_realestate"]
        if isinstance(items, list):
            p.append('<ul style="padding-left:0;list-style:none;margin-bottom:40px;">')
            for item in items:
                p.append(
                    '<li style="display:flex;gap:10px;align-items:flex-start;'
                    'margin-bottom:12px;font-size:15px;line-height:1.8;color:#374151;">'
                    '<span style="color:#10b981;font-weight:700;flex-shrink:0;margin-top:2px;">▸</span>'
                    f'<span>{_bold_numbers(item)}</span></li>'
                )
            p.append('</ul>')
        else:
            p.append(
                f'<p style="font-size:15px;line-height:1.95;color:#374151;margin-bottom:40px;">'
                f'{_bold_numbers(items)}</p>'
            )
        p.append(_divider())

    # ── 전문가 인용구 ─────────────────────────────────────────────────────────
    expert_quotes = insight.get("expert_quotes") if insight else None
    if expert_quotes:
        p.append(_h2("💬 전문가 3인의 한 마디"))
        styles = [
            ("#eff6ff", "#2563eb", "#dbeafe"),
            ("#f0fdf4", "#16a34a", "#bbf7d0"),
            ("#fefce8", "#ca8a04", "#fde68a"),
        ]
        for i, eq in enumerate(expert_quotes):
            bg, accent, border_c = styles[i % len(styles)]
            p.append(
                f'<div style="background:{bg};border:1px solid {border_c};border-radius:10px;'
                f'padding:20px 22px;margin-bottom:14px;">'
                f'<p style="margin:0 0 10px;font-size:15px;line-height:1.8;color:#1e293b;">'
                f'&ldquo;{eq["quote"]}&rdquo;</p>'
                f'<span style="font-size:13px;font-weight:700;color:{accent};">— {eq["role"]}</span>'
                '</div>'
            )
        p.append('<div style="margin-bottom:40px;"></div>')
        p.append(_divider())

    # ── 정책 연결 ─────────────────────────────────────────────────────────────
    if insight and insight.get("policy_context"):
        p.append(_h2("🗺️ 서울 도시계획과의 연결"))
        p.append(
            '<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;'
            'padding:22px 24px;margin-bottom:40px;">'
            f'<p style="font-size:15px;line-height:1.95;color:#374151;margin:0;">'
            f'{_bold_numbers(insight["policy_context"])}</p>'
            '</div>'
        )
        p.append(_divider())

    # ── 향후 일정 ─────────────────────────────────────────────────────────────
    if insight and insight.get("timeline"):
        p.append(_h2("📅 앞으로의 일정"))
        p.append(
            f'<p style="font-size:15px;line-height:1.95;color:#374151;margin-bottom:40px;">'
            f'{_bold_numbers(insight["timeline"])}</p>'
        )
        p.append(_divider())

    # ── FAQ ──────────────────────────────────────────────────────────────────
    faq = insight.get("faq") if insight else None
    if faq:
        p.append(_h2("❓ 자주 묻는 질문"))
        for i, qa in enumerate(faq):
            p.append(
                '<div style="border:1px solid #e5e7eb;border-radius:10px;'
                'margin-bottom:12px;overflow:hidden;">'
                '<div style="background:#f9fafb;padding:14px 18px;border-bottom:1px solid #e5e7eb;">'
                f'<p style="margin:0;font-weight:700;font-size:15px;color:#111827;">Q.  {qa["q"]}</p>'
                '</div>'
                '<div style="padding:16px 18px;">'
                f'<p style="margin:0;font-size:14px;line-height:1.9;color:#4b5563;">A.  {qa["a"]}</p>'
                '</div>'
                '</div>'
            )
        p.append('<div style="margin-bottom:40px;"></div>')

    # ── 키워드 태그 ───────────────────────────────────────────────────────────
    if insight and insight.get("keywords"):
        tags = " ".join(
            f'<a style="display:inline-block;background:#f3f4f6;color:#4b5563;'
            f'padding:5px 14px;border-radius:20px;font-size:13px;margin:3px;'
            f'text-decoration:none;">#{kw}</a>'
            for kw in insight["keywords"]
        )
        p.append(f'<p style="margin-bottom:40px;">{tags}</p>')
        p.append(_divider())

    # ── 기본정보 테이블 ───────────────────────────────────────────────────────
    p.append(_h2("📋 고시 기본정보"))
    p.append('<table style="width:100%;border-collapse:collapse;margin-bottom:36px;font-size:14px;">')
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
        p.append(
            '<tr>'
            f'<td style="padding:10px 14px;border:1px solid #e5e7eb;background:#f9fafb;'
            f'font-weight:600;width:140px;color:#374151;">{label}</td>'
            f'<td style="padding:10px 14px;border:1px solid #e5e7eb;color:#374151;">{value}</td>'
            '</tr>'
        )
    p.append('</table>')
    p.append(_divider())

    # ── 고시 원문 ─────────────────────────────────────────────────────────────
    p.append(_h2("📄 고시 원문"))
    formatted_content = content.replace("\n", "<br>")
    p.append(
        '<div style="font-size:14px;line-height:1.95;padding:20px 22px;background:#fafafa;'
        'border:1px solid #e5e7eb;border-radius:8px;margin-bottom:36px;color:#4b5563;">'
        f'{formatted_content}</div>'
    )

    # ── 지도 ─────────────────────────────────────────────────────────────────
    if location:
        map_query = location.replace(" ", "+")
        p.append(_h2("🗺️ 위치"))
        p.append(
            f'<iframe src="https://maps.google.com/maps?q={map_query}&output=embed&hl=ko&z=17" '
            'width="100%" height="380" style="border:0;border-radius:8px;margin-bottom:36px;" '
            'allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade">'
            '</iframe>'
        )

    # ── 관련 링크 ─────────────────────────────────────────────────────────────
    if page_url or doc_url:
        p.append(_h2("🔗 관련 링크"))
        p.append('<ul style="margin-bottom:24px;line-height:2.2;font-size:14px;">')
        if page_url:
            p.append(
                f'<li><a href="{page_url}" target="_blank" rel="noopener">'
                '📌 상세 페이지 (서울도시공간포털)</a></li>'
            )
        if doc_url:
            p.append(
                f'<li><a href="{doc_url}" target="_blank" rel="noopener">'
                '📎 원문 다운로드 (PDF)</a></li>'
            )
        p.append('</ul>')

    # ── 출처 ─────────────────────────────────────────────────────────────────
    p.append('<hr style="margin:32px 0 16px;border:none;border-top:1px solid #e5e7eb;">')
    p.append(
        '<p style="font-size:12px;color:#9ca3af;">데이터 출처: '
        '<a href="https://urban.seoul.go.kr" target="_blank" rel="noopener">'
        '서울도시공간포털</a> (urban.seoul.go.kr)</p>'
    )

    html = "\n".join(p)
    return {"title": title, "html": html, "excerpt": excerpt}
