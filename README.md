# 서울 도시계획 결정고시 모니터

서울시 도시계획 결정고시 데이터를 자동 수집하고, 2040 서울플랜 중심지체계와 매칭하여 분석하는 대시보드입니다.

## 주요 기능

- **자동 수집** — GitHub Actions로 매일 KST 09:00에 신규 고시문 수집
- **중심지 매칭** — 2040 서울플랜 중심지체계(3도심·7광역중심·12지역중심)와 자동 매칭
- **대시보드** — 중심지 지도, 최신 고시문 목록, 월별 추이, 중심지별 분석
- **원문 링크** — 고시문 원문(PDF) 및 상세 페이지 바로가기

## 데이터 소스

[서울도시공간포털](https://urban.seoul.go.kr) 내부 API (`/ntfc/getNtfcList.json`)

### 수집 필드

| 필드 | 설명 |
|------|------|
| `notice_code` | 고시 고유코드 |
| `notice_date` | 고시일자 |
| `title` | 제목 |
| `content` | 본문 |
| `organ_name` | 고시기관 (서울특별시, 자치구 등) |
| `location` | 위치 (구·동·번지) |
| `notice_type` | 고시유형 (결정, 변경 등) |
| `doc_url` | 원문 파일 URL |
| `page_url` | 웹 상세페이지 URL |
| `center_grade` | 2040플랜 중심지 등급 |
| `center_name` | 매칭된 중심지명 |

## 2040 서울플랜 중심지체계

| 등급 | 중심지 |
|------|--------|
| **도심** | 한양도성(서울도심), 여의도·영등포, 강남 |
| **광역중심** | 용산, 청량리·왕십리, 창동·상계, 상암·수색, 마곡, 가산·대림, 잠실 |
| **지역중심** | 동대문, 망우, 미아, 성수, 신촌, 마포, 공덕, 연신내·불광, 목동, 봉천, 사당·이수, 수서·문정, 천호·길동 |

## 프로젝트 구조

```
├── data/                  # 날짜별 고시문 JSON
│   ├── 2024-03-27.json
│   ├── ...
│   └── latest.json
├── web/                   # Next.js 대시보드
│   └── src/
├── .github/workflows/
│   └── fetch-daily.yml    # 일일 자동 수집
├── fetch_daily.py         # 수집 스크립트
├── centers.py             # 중심지체계 매핑 + 좌표
├── crawler.py             # API 호출/파싱
├── main.py                # CLI
└── config.py              # 설정
```

## 사용법

### CLI

```bash
# 의존성 설치
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 데이터 수집
python main.py fetch              # 전체 수집
python main.py fetch --max-pages 5 # 5페이지만

# 조회
python main.py list                # 최신 목록
python main.py list --center 도심   # 도심 중심지 필터
python main.py list --keyword 재개발 # 키워드 검색
python main.py stats               # 통계
```

### 대시보드 (로컬)

```bash
cd web
npm install
npm run dev
# http://localhost:3000
```

## 자동 수집

GitHub Actions가 매일 KST 09:00에 실행됩니다.

- 신규 고시문만 감지하여 `data/YYYY-MM-DD.json`에 추가
- 변경사항이 있을 때만 자동 커밋
- Actions 탭에서 수동 실행(`Run workflow`)도 가능

## 라이선스

데이터 출처: [서울도시공간포털](https://urban.seoul.go.kr) (서울특별시)
