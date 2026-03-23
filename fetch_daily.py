"""GitHub Actions용 일일 수집 스크립트.
신규 고시문만 JSON 파일로 저장."""

import json
import os
import logging
from datetime import datetime
from collections import defaultdict
from urllib.parse import quote

import requests

from centers import match_center

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

API_URL = "https://urban.seoul.go.kr/ntfc/getNtfcList.json"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
LATEST_FILE = os.path.join(DATA_DIR, "latest.json")


def load_latest() -> dict:
    if os.path.exists(LATEST_FILE):
        with open(LATEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_fetched": "2020-01-01", "total_records": 0}


def load_existing_codes() -> set:
    """이미 저장된 모든 notice_code를 수집"""
    codes = set()
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".json") or fname in ("latest.json", "wp_published.json"):
            continue
        filepath = os.path.join(DATA_DIR, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            records = json.load(f)
            for r in records:
                codes.add(r["notice_code"])
    return codes


def fetch_page(page_no: int, page_size: int = 100) -> dict:
    resp = requests.post(
        API_URL,
        json={
            "pageNo": page_no,
            "pageSize": page_size,
            "keywordList": [],
            "pubSiteCode": "",
            "organCode": "",
            "bgnDate": "",
            "endDate": "",
            "srchType": "title",
            "noticeCode": "",
        },
        headers={"Content-Type": "application/json; charset=UTF-8"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def parse_item(item: dict) -> dict:
    organ = item.get("organ") or {}
    notice_classify = item.get("noticeClassifyNm") or {}
    classify_g = item.get("classifyGnm") or {}
    classify_m = item.get("classifyMnm") or {}
    site_cd = item.get("siteCd") or {}
    plan_pub = item.get("planPrjctPub") or {}
    ntfc_img = item.get("tnNtfcImage") or {}

    title = item.get("title") or ""
    content = item.get("content") or ""
    location = plan_pub.get("location") or ""

    match_text = location if location else f"{title} {content} {organ.get('insttName', '')}"
    center_grade, center_name = match_center(match_text)

    notice_date_raw = item.get("noticeDate") or ""
    notice_date = notice_date_raw[:10] if notice_date_raw else ""

    # 원문 URL
    doc_url = ""
    img_path = ntfc_img.get("aImagePath", "")
    img_name = ntfc_img.get("aImageName", "")
    if img_path and img_name:
        encoded_name = quote(img_name, safe="")
        doc_url = f"https://urban.seoul.go.kr/{img_path}/{encoded_name}"

    return {
        "notice_code": item.get("noticeCode", ""),
        "notice_no": item.get("noticeNo", ""),
        "notice_date": notice_date,
        "title": title,
        "content": content,
        "organ_code": organ.get("insttCode", ""),
        "organ_name": organ.get("insttName", ""),
        "notice_type": notice_classify.get("cmnName", ""),
        "classify_g": classify_g.get("classifyCodeName", "") if isinstance(classify_g, dict) else "",
        "classify_m": classify_m.get("classifyCodeName", "") if isinstance(classify_m, dict) else "",
        "site_code": site_cd.get("siteCode", "") if isinstance(site_cd, dict) else "",
        "site_name": site_cd.get("siteName", "") if isinstance(site_cd, dict) else "",
        "location": location,
        "doc_url": doc_url,
        "page_url": f"https://urban.seoul.go.kr/view/html/PMNU4030100001?noticeCode={item.get('noticeCode', '')}",
        "center_grade": center_grade,
        "center_name": center_name,
    }


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    latest = load_latest()
    existing_codes = load_existing_codes()
    logger.info(f"기존 데이터: {len(existing_codes)}건, 마지막 수집일: {latest['last_fetched']}")

    new_records = defaultdict(list)
    page_no = 1
    consecutive_existing = 0

    while True:
        logger.info(f"Fetching page {page_no}...")
        data = fetch_page(page_no)
        items = data.get("content", [])

        if not items:
            break

        for item in items:
            record = parse_item(item)
            if record["notice_code"] in existing_codes:
                consecutive_existing += 1
            else:
                consecutive_existing = 0
                new_records[record["notice_date"]].append(record)
                existing_codes.add(record["notice_code"])

        # 연속 200건이 모두 기존 데이터면 중단
        if consecutive_existing >= 200:
            logger.info("신규 데이터 없음, 중단.")
            break

        total_pages = data.get("totalPages", 1)
        if page_no >= total_pages:
            break
        page_no += 1

    # 신규분 JSON 저장
    total_new = 0
    for date, records in new_records.items():
        filepath = os.path.join(DATA_DIR, f"{date}.json")

        # 기존 파일이 있으면 병합
        existing = []
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)

        existing_codes_in_file = {r["notice_code"] for r in existing}
        for r in records:
            if r["notice_code"] not in existing_codes_in_file:
                existing.append(r)
                total_new += 1

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

    # latest.json 업데이트
    all_dates = [f.replace(".json", "") for f in os.listdir(DATA_DIR)
                 if f.endswith(".json") and f not in ("latest.json", "wp_published.json")]
    latest_date = max(all_dates) if all_dates else latest["last_fetched"]
    total_records = latest.get("total_records", 0) + total_new

    with open(LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "last_fetched": latest_date,
            "total_records": total_records,
            "last_run": datetime.now().isoformat(),
        }, f, ensure_ascii=False, indent=2)

    logger.info(f"완료: 신규 {total_new}건 저장")
    # GitHub Actions 출력용
    print(f"::set-output name=new_count::{total_new}")


if __name__ == "__main__":
    main()
