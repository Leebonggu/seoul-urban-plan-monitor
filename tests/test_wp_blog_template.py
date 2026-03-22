from wp_blog_template import generate_wp_content

def test_basic_post():
    record = {
        "notice_code": "TEST001",
        "notice_no": "2026-100",
        "notice_date": "2026-03-20",
        "title": "테스트 고시문",
        "content": "테스트 본문 내용입니다.",
        "organ_name": "서울특별시",
        "notice_type": "결정",
        "location": "강남구 삼성동 일대",
        "center_grade": "도심",
        "center_name": "강남",
        "doc_url": "https://example.com/test.pdf",
        "page_url": "https://example.com/page",
    }
    result = generate_wp_content(record)
    assert "title" in result
    assert "html" in result
    assert "강남구" in result["title"]
    assert "2026-03-20" in result["html"]
    assert "도심" in result["html"]
    assert "테스트 본문 내용입니다." in result["html"]

def test_no_center():
    record = {
        "notice_code": "TEST002",
        "notice_no": "2026-101",
        "notice_date": "2026-03-21",
        "title": "미매칭 고시문",
        "content": "본문",
        "organ_name": "서울특별시",
        "notice_type": "결정",
        "location": "",
        "center_grade": None,
        "center_name": None,
        "doc_url": "",
        "page_url": "https://example.com/page2",
    }
    result = generate_wp_content(record)
    assert "title" in result
    assert "중심지" not in result["html"]

def test_no_doc_url():
    record = {
        "notice_code": "TEST003",
        "notice_no": "2026-102",
        "notice_date": "2026-03-22",
        "title": "원문 없는 고시문",
        "content": "본문",
        "organ_name": "강남구",
        "notice_type": "변경",
        "location": "강남구",
        "center_grade": "도심",
        "center_name": "강남",
        "doc_url": "",
        "page_url": "https://example.com/page3",
    }
    result = generate_wp_content(record)
    assert "원문 다운로드" not in result["html"]
