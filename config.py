import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

# urban.seoul.go.kr 내부 API (인증키 불필요)
API_BASE_URL = "https://urban.seoul.go.kr"
GOSI_LIST_ENDPOINT = "/ntfc/getNtfcList.json"
GOSI_DETAIL_ENDPOINT = "/ntfc/getNtfcDt.json"

# 페이지당 조회 건수 (최대)
PAGE_SIZE = 100

# DB 설정
DB_PATH = BASE_DIR / "gosi.db"

# 스케줄러 설정
SCHEDULE_HOUR = 9  # 매일 오전 9시
SCHEDULE_MINUTE = 0
