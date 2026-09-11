"""서울시 보도자료(news_report) HTML 크롤러.

목록 페이지에서 nttNo를 추출하고, 상세 페이지를 파싱해 레코드 dict를 만든다.
"""
import re
import time
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

LIST_URL = "https://www.seoul.go.kr/news/news_report.do"
BBS_NO = "158"
DEFAULT_CTGRY = "465"  # 주택
DEFAULT_PAGE_SIZE = 20
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
REQUEST_TIMEOUT = 30
SLEEP_BETWEEN_REQUESTS = 0.5

_NTTNO_RE = re.compile(r"fnTbbsView\('(\d+)'\)")


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def fetch_list(page: int = 1, ctgry: str = DEFAULT_CTGRY,
               size: int = DEFAULT_PAGE_SIZE,
               session: requests.Session | None = None) -> list[str]:
    """목록 페이지에서 nttNo 리스트 추출 (위→아래 = 최신→과거)."""
    sess = session or _session()
    params = {
        "bbsNo": BBS_NO,
        "srchCtgryType": ctgry,
        "cntPerPage": size,
        "curPage": page,
    }
    resp = sess.get(LIST_URL, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return _NTTNO_RE.findall(resp.text)


def fetch_detail(ntt_no: str, session: requests.Session | None = None) -> dict:
    """상세 페이지를 파싱해 레코드 dict 반환."""
    sess = session or _session()
    params = {"bbsNo": BBS_NO, "nttNo": ntt_no}
    resp = sess.get(LIST_URL, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    view = soup.select_one("#viewTable")
    if view is None:
        raise ValueError(f"#viewTable not found for nttNo={ntt_no}")

    title_el = view.select_one("h3")
    title = title_el.get_text(strip=True) if title_el else ""

    meta = {}
    for dl in view.select(".view-column dl"):
        dt = dl.find("dt")
        dd = dl.find("dd")
        if dt and dd:
            meta[dt.get_text(strip=True)] = dd.get_text(" ", strip=True)

    body_el = view.select_one("#scrabArea")
    body_html = body_el.decode_contents().strip() if body_el else ""

    attachments = []
    for file_div in view.select(".sib-viw-file"):
        a = file_div.find("a", href=True)
        if not a:
            continue
        attachments.append({
            "name": a.get_text(strip=True),
            "url": a["href"],
        })

    page_url = f"{LIST_URL}?bbsNo={BBS_NO}&nttNo={ntt_no}"

    return {
        "ntt_no": ntt_no,
        "title": title,
        "dept": meta.get("담당부서", ""),
        "contact": meta.get("문의", ""),
        "category": meta.get("분류", ""),
        "reg_date": meta.get("등록일", ""),
        "mod_date": meta.get("수정일", ""),
        "body_html": body_html,
        "attachments": attachments,
        "page_url": page_url,
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
    }


def fetch_first_page_records(ctgry: str = DEFAULT_CTGRY,
                             size: int = DEFAULT_PAGE_SIZE) -> list[dict]:
    """첫 페이지의 모든 보도자료를 상세까지 수집해 레코드 리스트로 반환."""
    sess = _session()
    ntt_nos = fetch_list(page=1, ctgry=ctgry, size=size, session=sess)
    logger.info(f"목록에서 {len(ntt_nos)}건의 nttNo 발견")
    records = []
    for i, ntt_no in enumerate(ntt_nos, 1):
        try:
            r = fetch_detail(ntt_no, session=sess)
            records.append(r)
            logger.info(f"[{i}/{len(ntt_nos)}] {ntt_no}: {r['title'][:40]}")
        except Exception as e:
            logger.error(f"[{i}/{len(ntt_nos)}] {ntt_no} 상세 수집 실패: {e}")
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return records
