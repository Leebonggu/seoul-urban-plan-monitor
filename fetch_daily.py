"""GitHub Actions용 일일 수집 스크립트.
신규 고시문만 JSON 파일로 저장."""

import json
import os
import re
import sys
import logging
import time
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

API_SOURCES = {
    "결정고시": {
        "url": "https://urban.seoul.go.kr/ntfc/getNtfcList.json",
        "page_url_base": "https://urban.seoul.go.kr/view/html/PMNU4030100001",
    },
    "지구단위계획": {
        "url": "https://urban.seoul.go.kr/dstplan/getDstplanList.json",
        "page_url_base": "https://urban.seoul.go.kr/view/html/PMNU4030200001",
    },
}
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
LATEST_FILE = os.path.join(DATA_DIR, "latest.json")


def load_latest() -> dict:
    if os.path.exists(LATEST_FILE):
        with open(LATEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_fetched": "2020-01-01", "total_records": 0}


def load_existing_codes() -> set:
    """이미 저장된 모든 notice_code를 수집"""
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\.json$")
    codes = set()
    for fname in os.listdir(DATA_DIR):
        if not date_pattern.match(fname):
            continue
        filepath = os.path.join(DATA_DIR, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            records = json.load(f)
            for r in records:
                codes.add(r["notice_code"])
    return codes


MAX_PAGES = 30
MAX_RETRIES = 3


def fetch_page(api_url: str, page_no: int, page_size: int = 100,
               bgn_date: str = "") -> dict:
    for attempt in range(1, MAX_RETRIES + 1):
        resp = requests.post(
            api_url,
            json={
                "pageNo": page_no,
                "pageSize": page_size,
                "keywordList": [],
                "pubSiteCode": "",
                "organCode": "",
                "bgnDate": bgn_date,
                "endDate": "",
                "srchType": "title",
                "noticeCode": "",
            },
            headers={"Content-Type": "application/json; charset=UTF-8"},
            timeout=60,
        )
        resp.raise_for_status()
        try:
            return resp.json()
        except requests.exceptions.JSONDecodeError:
            if attempt < MAX_RETRIES:
                logger.warning(f"JSON 파싱 실패 (시도 {attempt}/{MAX_RETRIES}), 재시도...")
                time.sleep(2 * attempt)
            else:
                logger.error(f"JSON 파싱 {MAX_RETRIES}회 실패, 건너뜀")
                return {"content": [], "totalPages": 0}


def parse_ntfc_item(item: dict, category: str, page_url_base: str) -> dict:
    """결정고시 API 응답 아이템 파싱."""
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
        "page_url": f"{page_url_base}?noticeCode={item.get('noticeCode', '')}",
        "center_grade": center_grade,
        "center_name": center_name,
        "category": category,
    }


def parse_dstplan_item(item: dict, page_url_base: str) -> dict:
    """지구단위계획 API 응답 아이템 파싱."""
    ntfc = item.get("tnNtfc") or {}
    organ = ntfc.get("organ") or {}
    ntfc_img = ntfc.get("tnNtfcImage") or {}

    title = ntfc.get("title") or item.get("zoneName") or ""
    content = ntfc.get("content") or ""
    location = item.get("locationName") or ""

    match_text = location if location else f"{title} {content}"
    center_grade, center_name = match_center(match_text)

    notice_date_raw = ntfc.get("noticeDate") or ""
    notice_date = notice_date_raw[:10] if notice_date_raw else ""

    notice_code = ntfc.get("noticeCode") or item.get("recordCode", "")

    # 원문 URL
    doc_url = ""
    img_path = ntfc_img.get("aImagePath", "")
    img_name = ntfc_img.get("aImageName", "")
    if img_path and img_name:
        encoded_name = quote(img_name, safe="")
        doc_url = f"https://urban.seoul.go.kr/{img_path}/{encoded_name}"

    return {
        "notice_code": notice_code,
        "notice_no": ntfc.get("noticeNo", ""),
        "notice_date": notice_date,
        "title": title,
        "content": content,
        "organ_code": organ.get("insttCode", ""),
        "organ_name": organ.get("insttName", ""),
        "notice_type": "지구단위계획",
        "classify_g": "",
        "classify_m": "",
        "site_code": item.get("siteCode", ""),
        "site_name": "",
        "location": location,
        "doc_url": doc_url,
        "page_url": f"{page_url_base}?noticeCode={notice_code}",
        "center_grade": center_grade,
        "center_name": center_name,
        "category": "지구단위계획",
        "zone_name": (item.get("zoneName") or "").strip(),
        "area": item.get("areaAfter"),
    }


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fetch_source(source_name: str, api_url: str, page_url_base: str,
                  existing_codes: set, bgn_date: str = "") -> dict[str, list]:
    """단일 API 소스에서 신규 레코드 수집."""
    new_records = defaultdict(list)
    page_no = 1
    consecutive_existing = 0
    is_dstplan = "dstplan" in api_url

    while True:
        logger.info(f"[{source_name}] Fetching page {page_no}...")
        data = fetch_page(api_url, page_no, bgn_date=bgn_date)
        items = data.get("content", [])

        if not items:
            break

        for item in items:
            if is_dstplan:
                record = parse_dstplan_item(item, page_url_base)
            else:
                record = parse_ntfc_item(item, source_name, page_url_base)

            if not record["notice_code"] or record["notice_code"] in existing_codes:
                consecutive_existing += 1
            elif not _DATE_RE.match(record["notice_date"]):
                logger.warning(f"[{source_name}] 비정상 날짜 건너뜀: {record['notice_date']!r}")
                consecutive_existing += 1
            else:
                consecutive_existing = 0
                new_records[record["notice_date"]].append(record)
                existing_codes.add(record["notice_code"])

        if consecutive_existing >= 100:
            logger.info(f"[{source_name}] 신규 데이터 없음, 중단.")
            break

        total_pages = data.get("totalPages", 1)
        if page_no >= total_pages:
            break
        if page_no >= MAX_PAGES:
            logger.warning(f"[{source_name}] 최대 페이지({MAX_PAGES}) 도달, 중단.")
            break
        page_no += 1

    return new_records


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    full_mode = "--full" in sys.argv
    latest = load_latest()
    existing_codes = load_existing_codes()

    if full_mode:
        logger.info(f"[전체 수집 모드] 기존 데이터: {len(existing_codes)}건")
    else:
        logger.info(f"기존 데이터: {len(existing_codes)}건, 마지막 수집일: {latest['last_fetched']}")

    all_new_records = defaultdict(list)

    for source_name, source_cfg in API_SOURCES.items():
        new_records = fetch_source(
            source_name,
            source_cfg["url"],
            source_cfg["page_url_base"],
            existing_codes,
        )
        for date_key, records in new_records.items():
            all_new_records[date_key].extend(records)

    # 신규분 JSON 저장
    total_new = 0
    for date, records in all_new_records.items():
        filepath = os.path.join(DATA_DIR, f"{date}.json")

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
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    all_dates = [f.replace(".json", "") for f in os.listdir(DATA_DIR)
                 if f.endswith(".json") and date_pattern.match(f.replace(".json", ""))]
    latest_date = max(all_dates) if all_dates else latest["last_fetched"]
    total_records = latest.get("total_records", 0) + total_new

    with open(LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "last_fetched": latest_date,
            "total_records": total_records,
            "last_run": datetime.now().isoformat(),
        }, f, ensure_ascii=False, indent=2)

    logger.info(f"완료: 신규 {total_new}건 저장")
    print(f"::set-output name=new_count::{total_new}")


if __name__ == "__main__":
    main()
