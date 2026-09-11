"""서울시 보도자료(주택) 일일 수집 스크립트 — GitHub Actions용.

Usage:
  python fetch_news_daily.py              # 신규만 수집
  python fetch_news_daily.py --backfill   # 최초 1회 백필 (수집만, 발행 스킵 마킹)
"""
import os
import sys
import json
import logging
from datetime import datetime
from collections import defaultdict

from news_crawler import fetch_first_page_records, DEFAULT_CTGRY, DEFAULT_PAGE_SIZE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "news")
LATEST_PATH = os.path.join(DATA_DIR, "latest.json")
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


def load_existing_ntt_nos() -> set:
    """data/news/{date}.json 전체를 훑어 이미 저장된 ntt_no 수집."""
    nos = set()
    if not os.path.isdir(DATA_DIR):
        return nos
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".json"):
            continue
        if fname in ("latest.json", "wp_published.json", "naver_posted.json"):
            continue
        for r in _load_json(os.path.join(DATA_DIR, fname), []):
            nos.add(r["ntt_no"])
    return nos


def save_records_by_date(records: list[dict]) -> int:
    """등록일별 JSON 파일에 append (중복 ntt_no 스킵). 새로 저장된 건수 반환."""
    by_date = defaultdict(list)
    for r in records:
        date_key = r.get("reg_date") or "unknown"
        by_date[date_key].append(r)

    new_total = 0
    for date_key, recs in by_date.items():
        path = os.path.join(DATA_DIR, f"{date_key}.json")
        existing = _load_json(path, [])
        existing_nos = {r["ntt_no"] for r in existing}
        for r in recs:
            if r["ntt_no"] not in existing_nos:
                existing.append(r)
                new_total += 1
        existing.sort(key=lambda r: r["ntt_no"], reverse=True)
        _save_json(path, existing)
    return new_total


def main():
    backfill = "--backfill" in sys.argv

    os.makedirs(DATA_DIR, exist_ok=True)
    latest = _load_json(LATEST_PATH, {"baseline_done": False, "total_records": 0})
    baseline_done = latest.get("baseline_done", False)

    if backfill and baseline_done:
        logger.info("백필이 이미 완료된 상태입니다 (latest.json baseline_done=true). 종료.")
        return
    if not backfill and not baseline_done:
        logger.warning("백필이 아직 수행되지 않았습니다. 먼저 --backfill로 한 번 실행하세요.")
        return

    existing_nos = load_existing_ntt_nos()
    logger.info(f"기존 저장 ntt_no: {len(existing_nos)}건")

    logger.info(f"보도자료 첫 페이지 수집 (ctgry={DEFAULT_CTGRY}, size={DEFAULT_PAGE_SIZE})")
    records = fetch_first_page_records(ctgry=DEFAULT_CTGRY, size=DEFAULT_PAGE_SIZE)
    logger.info(f"수집 완료: {len(records)}건")

    new_records = [r for r in records if r["ntt_no"] not in existing_nos]
    logger.info(f"신규 ntt_no: {len(new_records)}건")

    new_count = save_records_by_date(new_records)
    logger.info(f"파일 저장: 신규 {new_count}건")

    if backfill:
        # 모든 백필 ntt_no를 wp_published에 더미로 마킹 → 발행 스킵
        wp_published = _load_json(WP_PUBLISHED_PATH, {})
        for r in records:
            wp_published.setdefault(r["ntt_no"], "BACKFILL")
        _save_json(WP_PUBLISHED_PATH, wp_published)
        logger.info(f"백필 마킹 완료: wp_published.json에 {len(records)}건 BACKFILL 추가")

    latest_dates = [r["reg_date"] for r in records if r.get("reg_date")]
    last_fetched = max(latest_dates) if latest_dates else latest.get("last_fetched", "")
    new_total_records = latest.get("total_records", 0) + new_count
    _save_json(LATEST_PATH, {
        "last_fetched": last_fetched,
        "total_records": new_total_records,
        "last_run": datetime.now().isoformat(timespec="seconds"),
        "baseline_done": True if backfill else baseline_done,
    })

    print(f"::set-output name=new_count::{new_count}")


if __name__ == "__main__":
    main()
