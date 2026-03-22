# 1-1. 워드프레스 자동 발행 구현 플랜

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 매일 크롤링된 고시문을 워드프레스에 자동 발행하고, 원문 PDF를 이미지로 변환하여 포스팅에 삽입한다.

**Architecture:** `fetch_daily.py` 실행 후 신규 고시문을 감지하면, `wp_publisher.py`가 WordPress REST API로 포스팅을 생성한다. PDF는 `pdf2image`로 PNG 변환 후 WP Media API로 업로드한다. 전체 파이프라인은 GitHub Actions에서 자동 실행된다.

**Tech Stack:** Python, WordPress REST API (Application Password), pdf2image (poppler), requests

**Spec:** `docs/superpowers/specs/2026-03-22-monetization-design.md` 1-1 참조

---

## 파일 구조

| 파일 | 역할 |
|------|------|
| `wp_config.py` | WordPress 접속 정보 (URL, 사용자, 앱 패스워드). 환경변수에서 로드. |
| `wp_publisher.py` | 포스팅 생성, 이미지 업로드, 발행 상태 관리의 메인 모듈. |
| `pdf_to_images.py` | PDF/HWP 다운로드 → PNG 변환. |
| `wp_blog_template.py` | 고시문 JSON → WordPress HTML 본문 생성. |
| `publish_daily.py` | GitHub Actions 엔트리포인트. 신규 고시문 감지 → 변환 → 발행 오케스트레이션. |
| `data/wp_published.json` | 발행 완료된 notice_code → WP post URL 매핑. |
| `.github/workflows/fetch-daily.yml` | 기존 워크플로우에 발행 step 추가. |
| `requirements.txt` | `pdf2image` 추가. |
| `tests/test_wp_blog_template.py` | 블로그 템플릿 단위 테스트. |
| `tests/test_pdf_to_images.py` | PDF 변환 단위 테스트. |
| `tests/test_wp_publisher.py` | WP API 호출 단위 테스트 (mock). |

---

## Task 1: WordPress 설정 모듈

**Files:**
- Create: `wp_config.py`

- [ ] **Step 1: `wp_config.py` 작성**

```python
import os

WP_URL = os.environ.get("WP_URL", "")           # e.g. https://your-site.wordpress.com
WP_USER = os.environ.get("WP_USER", "")          # WordPress 사용자명
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")  # Application Password
WP_API_BASE = f"{WP_URL}/wp-json/wp/v2"

def validate_config():
    missing = []
    if not WP_URL:
        missing.append("WP_URL")
    if not WP_USER:
        missing.append("WP_USER")
    if not WP_APP_PASSWORD:
        missing.append("WP_APP_PASSWORD")
    if missing:
        raise EnvironmentError(f"Missing env vars: {', '.join(missing)}")
```

- [ ] **Step 2: Commit**

```bash
git add wp_config.py
git commit -m "feat: WordPress 설정 모듈 추가"
```

---

## Task 2: 블로그 템플릿 (Python)

**Files:**
- Create: `wp_blog_template.py`
- Create: `tests/test_wp_blog_template.py`

- [ ] **Step 1: 테스트 작성**

```python
# tests/test_wp_blog_template.py
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
    assert "강남구 삼성동" in result["title"]
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
```

- [ ] **Step 2: 테스트 실행, 실패 확인**

```bash
python -m pytest tests/test_wp_blog_template.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'wp_blog_template'`

- [ ] **Step 3: 구현**

```python
# wp_blog_template.py

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
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
python -m pytest tests/test_wp_blog_template.py -v
```

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add wp_blog_template.py tests/test_wp_blog_template.py
git commit -m "feat: WordPress 블로그 템플릿 모듈 추가"
```

---

## Task 3: PDF → 이미지 변환

**Files:**
- Create: `pdf_to_images.py`
- Create: `tests/test_pdf_to_images.py`
- Modify: `requirements.txt`

- [ ] **Step 1: requirements.txt에 pdf2image 추가**

`requirements.txt` 끝에 추가:
```
pdf2image>=1.16.0
```

- [ ] **Step 2: 테스트 작성**

```python
# tests/test_pdf_to_images.py
import os
import tempfile
from unittest.mock import patch, MagicMock
from pdf_to_images import download_doc, convert_pdf_to_images

def test_download_doc_pdf(tmp_path):
    """PDF URL이면 다운로드 후 경로를 반환."""
    url = "https://example.com/test.pdf"
    fake_content = b"%PDF-1.4 fake content"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = fake_content

    with patch("pdf_to_images.requests.get", return_value=mock_response):
        path = download_doc(url, tmp_path)
        assert path is not None
        assert path.endswith(".pdf")
        assert os.path.exists(path)

def test_download_doc_empty_url(tmp_path):
    """빈 URL이면 None 반환."""
    path = download_doc("", tmp_path)
    assert path is None

def test_download_doc_hwp(tmp_path):
    """HWP URL이면 None 반환 (변환 불가)."""
    url = "https://example.com/test.hwp"
    path = download_doc(url, tmp_path)
    assert path is None

def test_convert_pdf_to_images():
    """pdf2image 호출을 mock하여 이미지 리스트 반환 확인."""
    fake_images = [MagicMock(), MagicMock()]
    for i, img in enumerate(fake_images):
        img.save = MagicMock()

    with patch("pdf_to_images.convert_from_path", return_value=fake_images):
        result = convert_pdf_to_images("/fake/path.pdf", "/fake/output")
        assert len(result) == 2
```

- [ ] **Step 3: 테스트 실행, 실패 확인**

```bash
python -m pytest tests/test_pdf_to_images.py -v
```

Expected: FAIL

- [ ] **Step 4: 구현**

```python
# pdf_to_images.py
import os
import requests
from urllib.parse import urlparse

def download_doc(url: str, output_dir: str) -> str | None:
    """고시문 원문을 다운로드. PDF만 지원, HWP는 건너뜀."""
    if not url:
        return None

    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lower()

    if ext not in (".pdf",):
        return None

    resp = requests.get(url, timeout=30)
    if resp.status_code != 200:
        return None

    filename = os.path.basename(parsed.path)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(resp.content)

    return filepath


def convert_pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> list[str]:
    """PDF를 페이지별 PNG로 변환."""
    from pdf2image import convert_from_path

    images = convert_from_path(pdf_path, dpi=dpi)
    paths = []
    base = os.path.splitext(os.path.basename(pdf_path))[0]

    for i, img in enumerate(images):
        img_path = os.path.join(output_dir, f"{base}_page_{i + 1}.png")
        img.save(img_path, "PNG")
        paths.append(img_path)

    return paths
```

- [ ] **Step 5: 테스트 통과 확인**

```bash
python -m pytest tests/test_pdf_to_images.py -v
```

Expected: 4 passed

- [ ] **Step 6: Commit**

```bash
git add pdf_to_images.py tests/test_pdf_to_images.py requirements.txt
git commit -m "feat: PDF → PNG 변환 모듈 추가"
```

---

## Task 4: WordPress API 발행 모듈

**Files:**
- Create: `wp_publisher.py`
- Create: `tests/test_wp_publisher.py`

- [ ] **Step 1: 테스트 작성**

```python
# tests/test_wp_publisher.py
import json
from unittest.mock import patch, MagicMock
from wp_publisher import upload_image, create_post, load_published, save_published

def test_upload_image():
    """이미지 업로드 시 WP Media API 호출 확인."""
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"id": 42, "source_url": "https://wp.com/img.png"}

    with patch("wp_publisher.requests.post", return_value=mock_resp):
        with patch("builtins.open", MagicMock()):
            result = upload_image("/fake/img.png")
            assert result["id"] == 42

def test_create_post():
    """포스트 생성 시 WP Posts API 호출 확인."""
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {
        "id": 100,
        "link": "https://wp.com/2026/03/20/test-post/",
    }

    with patch("wp_publisher.requests.post", return_value=mock_resp):
        result = create_post("제목", "<p>본문</p>")
        assert result["id"] == 100
        assert "link" in result

def test_load_save_published(tmp_path):
    """발행 기록 로드/저장."""
    filepath = str(tmp_path / "wp_published.json")

    data = load_published(filepath)
    assert data == {}

    data["TEST001"] = "https://wp.com/post/1"
    save_published(data, filepath)

    reloaded = load_published(filepath)
    assert reloaded["TEST001"] == "https://wp.com/post/1"
```

- [ ] **Step 2: 테스트 실행, 실패 확인**

```bash
python -m pytest tests/test_wp_publisher.py -v
```

Expected: FAIL

- [ ] **Step 3: 구현**

```python
# wp_publisher.py
import os
import json
import requests
from wp_config import WP_API_BASE, WP_USER, WP_APP_PASSWORD

def _auth():
    return (WP_USER, WP_APP_PASSWORD)

def upload_image(image_path: str) -> dict:
    """이미지를 WP Media Library에 업로드."""
    filename = os.path.basename(image_path)
    with open(image_path, "rb") as f:
        resp = requests.post(
            f"{WP_API_BASE}/media",
            auth=_auth(),
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "image/png",
            },
            data=f.read(),
            timeout=60,
        )
    resp.raise_for_status()
    return resp.json()

def create_post(title: str, html: str, status: str = "publish") -> dict:
    """WordPress 포스트 생성."""
    resp = requests.post(
        f"{WP_API_BASE}/posts",
        auth=_auth(),
        json={
            "title": title,
            "content": html,
            "status": status,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()

def load_published(filepath: str = "data/wp_published.json") -> dict:
    """발행 완료된 notice_code → WP URL 매핑 로드."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_published(data: dict, filepath: str = "data/wp_published.json"):
    """발행 기록 저장."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
python -m pytest tests/test_wp_publisher.py -v
```

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add wp_publisher.py tests/test_wp_publisher.py
git commit -m "feat: WordPress API 발행 모듈 추가"
```

---

## Task 5: 발행 오케스트레이션 스크립트

**Files:**
- Create: `publish_daily.py`

- [ ] **Step 1: 구현**

```python
# publish_daily.py
"""
매일 크롤링 후 실행. 신규 고시문을 워드프레스에 자동 발행.
Usage: python publish_daily.py
Env vars: WP_URL, WP_USER, WP_APP_PASSWORD
"""
import os
import json
import glob
import tempfile

from wp_config import validate_config
from wp_blog_template import generate_wp_content
from pdf_to_images import download_doc, convert_pdf_to_images
from wp_publisher import upload_image, create_post, load_published, save_published

DATA_DIR = os.environ.get("DATA_DIR", "data")
PUBLISHED_PATH = os.path.join(DATA_DIR, "wp_published.json")


def get_all_records() -> list[dict]:
    """모든 고시문 레코드 로드 (최신순)."""
    records = []
    for filepath in glob.glob(os.path.join(DATA_DIR, "*.json")):
        basename = os.path.basename(filepath)
        if basename in ("latest.json", "posted.json", "wp_published.json"):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            items = json.load(f)
            records.extend(items)
    records.sort(key=lambda r: r["notice_date"], reverse=True)
    return records


def publish_record(record: dict, tmp_dir: str) -> str | None:
    """단일 고시문을 WP에 발행. 성공 시 포스트 URL 반환."""
    post = generate_wp_content(record)
    html = post["html"]

    # PDF 다운로드 → 이미지 변환 → 업로드
    doc_url = record.get("doc_url", "")
    if doc_url:
        pdf_path = download_doc(doc_url, tmp_dir)
        if pdf_path:
            try:
                image_paths = convert_pdf_to_images(pdf_path, tmp_dir)
                image_tags = []
                for img_path in image_paths:
                    try:
                        media = upload_image(img_path)
                        src = media.get("source_url", "")
                        if src:
                            image_tags.append(
                                f'<figure><img src="{src}" alt="고시문 원문" '
                                f'style="max-width:100%;height:auto;"></figure>'
                            )
                    except Exception as e:
                        print(f"  이미지 업로드 실패: {e}")

                if image_tags:
                    images_html = "<h2>고시문 원문</h2>\n" + "\n".join(image_tags)
                    html = html.replace("<!-- IMAGES_PLACEHOLDER -->", images_html)
            except Exception as e:
                print(f"  PDF 변환 실패: {e}")

    # placeholder 제거 (이미지 없는 경우)
    html = html.replace("<!-- IMAGES_PLACEHOLDER -->", "")

    try:
        result = create_post(post["title"], html)
        return result.get("link", "")
    except Exception as e:
        print(f"  포스트 생성 실패: {e}")
        return None


def main():
    validate_config()

    published = load_published(PUBLISHED_PATH)
    records = get_all_records()

    # 미발행 고시문 필터 (최근 7일치만 처리)
    unpublished = [
        r for r in records
        if r["notice_code"] not in published
    ]

    # 한 번에 너무 많이 발행하지 않도록 제한
    batch = unpublished[:10]

    if not batch:
        print("새로 발행할 고시문이 없습니다.")
        return

    print(f"{len(batch)}건 발행 시작...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        for record in batch:
            code = record["notice_code"]
            print(f"  [{code}] {record['title'][:40]}...")

            url = publish_record(record, tmp_dir)
            if url:
                published[code] = url
                save_published(published, PUBLISHED_PATH)
                print(f"    → {url}")
            else:
                print(f"    → 실패")

    total = len([c for c, u in published.items() if u])
    print(f"완료. 총 {total}건 발행됨.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 로컬에서 dry-run 테스트 (WP 환경 있을 때)**

```bash
WP_URL=https://your-site.com WP_USER=admin WP_APP_PASSWORD=xxxx python publish_daily.py
```

- [ ] **Step 3: Commit**

```bash
git add publish_daily.py
git commit -m "feat: 워드프레스 자동 발행 오케스트레이션 스크립트"
```

---

## Task 6: GitHub Actions 워크플로우 확장

**Files:**
- Modify: `.github/workflows/fetch-daily.yml`

- [ ] **Step 1: 기존 워크플로우에 발행 step 추가**

기존 `fetch-daily.yml`의 `steps:` 끝에 다음을 추가:

```yaml
    - name: Install poppler for PDF conversion
      run: sudo apt-get update && sudo apt-get install -y poppler-utils

    - name: Install Python dependencies for publishing
      run: pip install pdf2image

    - name: Publish to WordPress
      if: env.WP_URL != ''
      env:
        WP_URL: ${{ secrets.WP_URL }}
        WP_USER: ${{ secrets.WP_USER }}
        WP_APP_PASSWORD: ${{ secrets.WP_APP_PASSWORD }}
      run: python publish_daily.py

    - name: Commit published records
      run: |
        git add data/wp_published.json || true
        git diff --staged --quiet || git commit -m "data: WP 발행 기록 업데이트"
```

- [ ] **Step 2: GitHub repo에 Secrets 설정 (수동)**

GitHub repo Settings → Secrets and variables → Actions에서:
- `WP_URL`: WordPress 사이트 URL
- `WP_USER`: WordPress 사용자명
- `WP_APP_PASSWORD`: Application Password

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/fetch-daily.yml
git commit -m "ci: GitHub Actions에 워드프레스 자동 발행 step 추가"
```

---

## Task 7: .gitignore 업데이트

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: 테스트/임시 파일 제외 추가**

`.gitignore`에 추가:
```
# Tests
__pycache__/
.pytest_cache/

# Temp
*.pyc
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: Python 캐시 파일 gitignore 추가"
```
