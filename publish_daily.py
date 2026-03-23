"""
워드프레스 자동/수동 발행 스크립트.

Usage:
  python publish_daily.py              # 당일 수집분만 발행 (GitHub Actions용)
  python publish_daily.py --backfill   # 미발행 전체 중 최신 10건 발행 (수동)
  python publish_daily.py --backfill --count 20  # 미발행 20건 발행

Env vars: WP_URL, WP_USER, WP_APP_PASSWORD
"""
import os
import sys
import json
import glob
import tempfile
from datetime import date

from wp_config import validate_config
from wp_blog_template import generate_wp_content
from pdf_to_images import download_doc, convert_pdf_to_images
from thumbnail import create_thumbnail
from wp_publisher import upload_image, create_post, load_published, save_published

DATA_DIR = os.environ.get("DATA_DIR", "data")
PUBLISHED_PATH = os.path.join(DATA_DIR, "wp_published.json")

# WordPress 카테고리 ID 매핑 (서울 중심지체계)
CATEGORY_MAP = {
    "도심": [2, 3],        # 서울 > 도심
    "광역중심": [2, 4],    # 서울 > 광역중심
    "지역중심": [2, 5],    # 서울 > 지역중심
}
DEFAULT_CATEGORIES = [2, 6]  # 서울 > 기타


def get_today_records() -> list[dict]:
    """오늘 날짜 파일의 고시문만 로드."""
    today = date.today().isoformat()
    filepath = os.path.join(DATA_DIR, f"{today}.json")
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


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

    # 중심지 등급에 따라 카테고리 매핑
    center_grade = record.get("center_grade") or ""
    categories = CATEGORY_MAP.get(center_grade, DEFAULT_CATEGORIES)

    # 썸네일 생성
    featured_image_id = None
    try:
        pdf_first_page = None
        doc_url = record.get("doc_url", "")
        if doc_url:
            pdf_path = download_doc(doc_url, tmp_dir)
            if pdf_path:
                try:
                    pages = convert_pdf_to_images(pdf_path, tmp_dir, dpi=72)
                    if pages:
                        pdf_first_page = pages[0]
                except Exception:
                    pass  # PDF 변환 실패 시 단색 배경으로 대체

        thumb_path = os.path.join(tmp_dir, f"{record['notice_code']}_thumb.png")
        create_thumbnail(record, thumb_path, pdf_first_page)
        media = upload_image(thumb_path)
        featured_image_id = media.get("id")
    except Exception as e:
        print(f"    썸네일 생성/업로드 실패: {e}")

    # 고시 날짜를 포스트 날짜로 설정 (백필 시 시간순 정렬)
    post_date = f"{record['notice_date']}T09:00:00"

    try:
        result = create_post(
            post["title"], html,
            categories=categories,
            featured_image_id=featured_image_id,
            post_date=post_date,
        )
        return result.get("link", "")
    except Exception as e:
        print(f"  포스트 생성 실패: {e}")
        return None


def publish_batch(records: list[dict], published: dict, limit: int = 10):
    """미발행 레코드를 배치로 발행."""
    unpublished = [r for r in records if r["notice_code"] not in published]

    batch = unpublished[:limit]

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


def main():
    validate_config()
    published = load_published(PUBLISHED_PATH)

    args = sys.argv[1:]
    backfill = "--backfill" in args

    # 배치 크기
    count = 10
    if "--count" in args:
        idx = args.index("--count")
        if idx + 1 < len(args):
            count = int(args[idx + 1])

    if backfill:
        # 수동: 미발행 전체에서 최신순으로 발행
        print(f"[백필 모드] 미발행 고시문 최대 {count}건 발행")
        records = get_all_records()
    else:
        # 자동: 오늘 수집분만 발행
        print("[일일 모드] 오늘 수집된 고시문만 발행")
        records = get_today_records()

    publish_batch(records, published, limit=count)


if __name__ == "__main__":
    main()
