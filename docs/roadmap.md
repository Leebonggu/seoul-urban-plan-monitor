# 수익화 로드맵

## 완료

| 항목 | 내용 |
|------|------|
| 쿠팡파트너스 동적 배너 | WordPress + Next.js 대시보드에 carousel 배너 2개 삽입 |
| 직방/호갱노노 URL 개선 | 구 이름만 추출해 검색 쿼리 정확도 향상 |
| GitHub Actions 정리 | 미사용 COUPANG_* env var 4개 제거 |

---

## Phase 3 — 네이버 블로그 크로스포스팅

**목적**: 네이버 검색 유입 확보 (동일 콘텐츠 자동 이중 발행)

### 현재 상태
- `naver_publisher.py` 구현 완료 (`post_to_naver_blog()`)
- `publish_daily.py`에 WordPress 발행 후 자동 호출 코드 존재
- GitHub Actions env var 선언 완료 (`NAVER_*` 5개)
- **단, GitHub Secrets 값이 비어 있어 현재는 스킵 처리됨**

### 남은 작업

**코드 수정 (1곳)**
- `naver_publisher.py`에 `_clean_for_naver()` 함수 추가
- WordPress HTML의 `<script>` 태그(쿠팡 배너) 제거 후 발행

**사용자 직접 수행 (최초 1회)**

1. [네이버 개발자 센터](https://developers.naver.com) → 애플리케이션 등록
   - 사용 API: **블로그 (글쓰기)**
   - 서비스 URL: `https://2lee.kr`
2. Client ID / Secret 발급
3. 로컬에서 OAuth 인증 실행:
   ```bash
   export NAVER_CLIENT_ID=발급받은값
   export NAVER_CLIENT_SECRET=발급받은값
   python naver_publisher.py --auth
   ```
4. 출력된 토큰을 GitHub Secrets에 저장:
   - `NAVER_CLIENT_ID`
   - `NAVER_CLIENT_SECRET`
   - `NAVER_ACCESS_TOKEN`
   - `NAVER_REFRESH_TOKEN`
   - `NAVER_BLOG_ID` — 네이버 아이디와 동일

### 검증
```bash
python publish_daily.py --backfill --count 1
# → 네이버 블로그 관리 > 내 글 목록에서 확인
# → GitHub Actions 로그: "[네이버] 발행 완료"
```

---

## Phase 2 — 텔레그램 알림봇

**목적**: 고시문 발행 시 지역별 채널 알림 → 구독자 모집 → 유료 전환 가능

### 구현 필요 항목
- `telegram_notifier.py` 신규 작성
- `publish_daily.py`의 `publish_record()` 성공 후 호출 추가
- GitHub Secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_ID`

### 사용자 직접 수행
- 텔레그램 @BotFather 에서 봇 생성 → 토큰 발급
- 지역별 채널 개설 (강남, 마포, 성동 등)

---

## Phase 4 — Next.js 대시보드 SEO/UX 개선

**목적**: `seoul-urban-plan-monitor.2lee.kr` 직접 트래픽 증가

| 항목 | 내용 |
|------|------|
| 사이트맵 자동 생성 | `next-sitemap` 패키지 → 고시 상세 URL 구글 색인 |
| 지역별 필터 페이지 | `/gu/강남구` 등 정적 생성 → 지역 키워드 SEO |
| 관련 고시문 추천 | 같은 구·유형 최근 5개 → 페이지 체류 시간 증가 |
