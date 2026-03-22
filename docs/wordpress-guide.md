# 워드프레스 자동 발행 가이드

## 구조

- `publish_daily.py` — 발행 스크립트 (일일/백필 모드)
- `wp_config.py` — WP 접속 설정 (환경변수)
- `wp_blog_template.py` — 고시문 → HTML 변환
- `wp_publisher.py` — WP REST API 호출
- `thumbnail.py` — 썸네일 자동 생성
- `pdf_to_images.py` — PDF → PNG 변환
- `data/wp_published.json` — 발행 기록

## 환경변수

| 변수 | 설명 |
|---|---|
| `WP_URL` | 워드프레스 사이트 URL |
| `WP_USER` | 워드프레스 관리자 아이디 |
| `WP_APP_PASSWORD` | Application Password (wp-admin → 사용자 → 프로필 → 하단) |

## 발행 모드

### 일일 모드 (기본 — GitHub Actions 자동)

당일 수집된 고시문만 발행.

```bash
python publish_daily.py
```

### 백필 모드 (수동)

과거 미발행 고시문을 최신순으로 발행.

```bash
# 미발행 10건 (기본)
python publish_daily.py --backfill

# 미발행 30건
python publish_daily.py --backfill --count 30
```

### 로컬 실행 예시

```bash
WP_URL=https://사이트주소 WP_USER=아이디 WP_APP_PASSWORD="앱 비밀번호" python3 publish_daily.py --backfill
```

### GitHub Actions 백필

1. GitHub → **Actions** 탭 → "결정고시 일일 수집"
2. **Run workflow** 클릭
3. "과거 미발행 고시문 백필 발행" 체크 ✅
4. "백필 시 발행 건수" 입력 (기본 10)
5. **Run workflow**

## 카테고리 매핑

| 중심지 등급 | WP 카테고리 | ID |
|---|---|---|
| 도심 | 서울 > 도심 | 2, 3 |
| 광역중심 | 서울 > 광역중심 | 2, 4 |
| 지역중심 | 서울 > 지역중심 | 2, 5 |
| 기타/없음 | 서울 > 기타 | 2, 6 |

## 썸네일

- PDF 원문이 있으면: PDF 첫 페이지 배경 + 등급별 컬러 오버레이 + 텍스트
- PDF 없으면: 등급별 단색 배경 + 텍스트
- 색상: 도심=파랑, 광역중심=초록, 지역중심=주황, 기타=회색
- 크기: 800x800 (정사각형, 테마 크롭에 강함)

## GitHub Secrets 설정

> https://github.com/Leebonggu/seoul-urban-plan-monitor/settings/secrets/actions

| Secret | 값 |
|---|---|
| `WP_URL` | 워드프레스 사이트 URL |
| `WP_USER` | 관리자 아이디 |
| `WP_APP_PASSWORD` | Application Password |
