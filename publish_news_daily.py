"""서울시 보도자료 → WordPress 발행 스크립트.

Usage:
  python publish_news_daily.py                    # 미발행 최대 5건 발행
  python publish_news_daily.py --limit 3          # 최대 3건
  python publish_news_daily.py --limit 1 --dry-run  # 렌더만, 실제 발행 X
  python publish_news_daily.py --ntt 456500       # 특정 nttNo만 강제 재발행

Env vars: WP_URL, WP_USER, WP_APP_PASSWORD, ANTHROPIC_API_KEY
Optional: WP_NEWS_CATEGORY_ID (보도자료용 WP 카테고리 ID)
"""
import os
import sys
import json
import argparse
import logging

from wp_config import validate_config
from wp_publisher import create_post
from news_template import render, generate_intro

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "news")
WP_PUBLISHED_PATH = os.path.join(DATA_DIR, "wp_published.json")


def _load_json(path: str, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_all_records() -> list[dict]:
    """data/news/{date}.json 전부를 로드 (등록일 내림차순)."""
    records = []
    if not os.path.isdir(DATA_DIR):
        return records
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".json"):
            continue
        if fname in ("latest.json", "wp_published.json", "naver_posted.json"):
            continue
        records.extend(_load_json(os.path.join(DATA_DIR, fname), []))
    records.sort(key=lambda r: (r.get("reg_date", ""), r.get("ntt_no", "")), reverse=True)
    return records


def _wp_categories() -> list[int] | None:
    raw = os.environ.get("WP_NEWS_CATEGORY_ID", "").strip()
    if not raw:
        return None
    try:
        return [int(x) for x in raw.split(",") if x.strip()]
    except ValueError:
        logger.warning(f"WP_NEWS_CATEGORY_ID 파싱 실패: {raw!r}")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--ntt", type=str, default=None,
                        help="특정 nttNo만 발행 (이미 발행됐어도 강제)")
    args = parser.parse_args()

    if not args.dry_run:
        validate_config()

    records = load_all_records()
    published = _load_json(WP_PUBLISHED_PATH, {})

    if args.ntt:
        candidates = [r for r in records if r["ntt_no"] == args.ntt]
        if not candidates:
            logger.error(f"nttNo={args.ntt} 레코드를 찾을 수 없음")
            sys.exit(1)
    else:
        candidates = [r for r in records if r["ntt_no"] not in published]
        candidates = candidates[: args.limit]

    if not candidates:
        logger.info("발행할 신규 보도자료 없음")
        return

    logger.info(f"발행 대상: {len(candidates)}건 (dry_run={args.dry_run})")
    categories = _wp_categories()

    success = 0
    for i, record in enumerate(candidates, 1):
        ntt = record["ntt_no"]
        logger.info(f"[{i}/{len(candidates)}] {ntt} {record['title'][:40]}")

        intro = generate_intro(record)
        rendered = render(record, intro=intro)

        if args.dry_run:
            print("=" * 70)
            print("TITLE:", rendered["title"])
            print("EXCERPT:", rendered["excerpt"])
            print("HTML LEN:", len(rendered["html"]))
            print(rendered["html"][:1200])
            print("...")
            continue

        try:
            post_date = None
            if record.get("reg_date"):
                post_date = f"{record['reg_date']}T09:00:00"
            res = create_post(
                title=rendered["title"],
                html=rendered["html"],
                status="publish",
                categories=categories,
                post_date=post_date,
            )
            url = res.get("link") or res.get("guid", {}).get("rendered", "")
            published[ntt] = url
            _save_json(WP_PUBLISHED_PATH, published)  # 1건마다 저장 (중간 실패 안전)
            logger.info(f"  발행 성공: {url}")
            success += 1
        except Exception as e:
            logger.error(f"  발행 실패: {e}")

    logger.info(f"완료: 성공 {success}/{len(candidates)}")


if __name__ == "__main__":
    main()
