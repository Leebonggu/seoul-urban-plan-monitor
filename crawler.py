"""urban.seoul.go.kr 내부 API를 통한 결정고시 데이터 수집"""

import logging
from datetime import datetime
from urllib.parse import quote

import requests

import config
from centers import match_center
from db import upsert_gosi

logger = logging.getLogger(__name__)


def _build_doc_url(item: dict) -> str:
    """고시문 원문(PDF/HWP) URL 생성"""
    ntfc_img = item.get("tnNtfcImage") or {}
    path = ntfc_img.get("aImagePath", "")
    name = ntfc_img.get("aImageName", "")
    if path and name:
        encoded_name = quote(name, safe="")
        return f"https://urban.seoul.go.kr/{path}/{encoded_name}"
    return ""


def _build_payload(page_no: int = 1, page_size: int = config.PAGE_SIZE, **kwargs) -> dict:
    return {
        "pageNo": page_no,
        "pageSize": page_size,
        "keywordList": kwargs.get("keywords", []),
        "pubSiteCode": kwargs.get("pub_site_code", ""),
        "organCode": kwargs.get("organ_code", ""),
        "bgnDate": kwargs.get("bgn_date", ""),
        "endDate": kwargs.get("end_date", ""),
        "srchType": "title",
        "noticeCode": kwargs.get("notice_code", ""),
    }


def fetch_page(page_no: int = 1, page_size: int = config.PAGE_SIZE, **kwargs) -> dict:
    url = config.API_BASE_URL + config.GOSI_LIST_ENDPOINT
    payload = _build_payload(page_no, page_size, **kwargs)

    resp = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def parse_item(item: dict) -> dict:
    """API 응답의 개별 항목을 DB 레코드로 변환"""
    organ = item.get("organ") or {}
    notice_classify = item.get("noticeClassifyNm") or {}
    classify_g = item.get("classifyGnm") or {}
    classify_m = item.get("classifyMnm") or {}
    site_cd = item.get("siteCd") or {}
    plan_pub = item.get("planPrjctPub") or {}

    title = item.get("title") or ""
    content = item.get("content") or ""
    location = plan_pub.get("location") or ""

    # 중심지체계 매칭 (location 우선, 없으면 제목+내용에서 키워드 검색)
    match_text = location if location else f"{title} {content} {organ.get('insttName', '')}"
    center_grade, center_name = match_center(match_text)

    notice_date_raw = item.get("noticeDate") or ""
    if notice_date_raw:
        notice_date = notice_date_raw[:10]  # "2026-03-19T09:00:00.000" → "2026-03-19"
    else:
        notice_date = ""

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
        "doc_url": _build_doc_url(item),
        "page_url": f"https://urban.seoul.go.kr/view/html/PMNU4030100001?noticeCode={item.get('noticeCode', '')}",
        "center_grade": center_grade,
        "center_name": center_name,
        "fetched_at": datetime.now().isoformat(),
    }


def fetch_and_save(max_pages: int | None = None, **kwargs) -> dict:
    """고시문을 수집하여 DB에 저장.

    Args:
        max_pages: 최대 페이지 수 제한 (None이면 전체)
        **kwargs: fetch_page에 전달할 추가 파라미터

    Returns:
        {"total_fetched": int, "new_count": int, "updated_count": int}
    """
    page_no = 1
    total_fetched = 0
    new_count = 0

    while True:
        logger.info(f"Fetching page {page_no}...")
        try:
            data = fetch_page(page_no, **kwargs)
        except requests.RequestException as e:
            logger.error(f"API 호출 실패 (page {page_no}): {e}")
            break

        items = data.get("content", [])
        if not items:
            logger.info("더 이상 데이터가 없습니다.")
            break

        for item in items:
            record = parse_item(item)
            is_new = upsert_gosi(record)
            if is_new:
                new_count += 1
            total_fetched += 1

        total_pages = data.get("totalPages", 1)
        logger.info(f"Page {page_no}/{total_pages} 완료 ({len(items)}건)")

        if page_no >= total_pages:
            break
        if max_pages and page_no >= max_pages:
            logger.info(f"max_pages({max_pages}) 도달, 중단.")
            break

        page_no += 1

    return {
        "total_fetched": total_fetched,
        "new_count": new_count,
        "updated_count": total_fetched - new_count,
    }
