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

    # 미발행 고시문 필터
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
