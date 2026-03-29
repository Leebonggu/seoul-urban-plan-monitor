# Dashboard SEO Optimization & Individual Notice Pages

**Date:** 2026-03-29
**Domain:** https://seoul-urban-plan-monitor.2lee.kr

## Background

대시보드가 커스텀 도메인에 연결됨. 현재 6개 정적 페이지로는 검색 노출이 제한적.
에드센스 승인 대기 중 — 페이지 수와 콘텐츠 품질 확보가 승인에도 유리.

## Goals

1. 검색 엔진 노출 극대화 (구글 + 네이버)
2. 에드센스 승인을 위한 콘텐츠 볼륨 확보
3. WordPress(2lee.kr)와 콘텐츠 차별화 (대시보드=데이터 중심, WP=읽을거리 중심)

## Design

### 1. 도메인 & 기본 SEO 인프라

하드코딩된 `seoul-gosi-monitor.vercel.app`을 전체 교체:

| 파일 | 변경 내용 |
|------|----------|
| `layout.tsx` | SITE_URL → `https://seoul-urban-plan-monitor.2lee.kr` |
| `sitemap.ts` | BASE_URL 교체 + 전체 페이지 URL 포함 (고시문 2,800+개) |
| `robots.ts` | sitemap URL 교체 |
| `page.tsx` (home) | OG url 자동 반영 (metadataBase에서 상속) |

누락된 메타데이터 추가:
- `/southwest` → sitemap에 추가
- `/privacy`, `/terms` → title + description metadata export 추가

### 2. 개별 고시문 페이지

**라우트:** `web/src/app/gosi/[notice_code]/page.tsx`

**데이터 로딩:**
- `generateStaticParams()` → 전체 notice_code 목록 반환 (SSG)
- `loadAllData()`에서 notice_code로 단일 레코드 조회

**페이지 구성:**
```
┌─────────────────────────────────┐
│ [등급 배지] 위치                 │
│ 고시문 제목                      │
├─────────────────────────────────┤
│ 메타데이터 테이블                │
│ - 고시번호, 고시일, 기관, 위치   │
├─────────────────────────────────┤
│ 고시 원문 내용 (content 전문)    │
├─────────────────────────────────┤
│ 원문 PDF 링크 | 출처 페이지 링크 │
├─────────────────────────────────┤
│ AdBanner                        │
└─────────────────────────────────┘
```

**SEO 메타데이터 (generateMetadata):**
- title: `"{location} {title 앞 50자}" | 서울 결정고시 모니터`
- description: content 앞 150자 + "서울시 도시계획 결정고시 원문"
- OG: title, description, url 자동 생성
- canonical: `https://seoul-urban-plan-monitor.2lee.kr/gosi/{notice_code}`

**데이터 유틸:**
- `lib/data.ts`에 `loadRecordByCode(code: string)` 함수 추가
- `lib/data.ts`에 `loadAllNoticeCodes()` 함수 추가

### 3. JSON-LD 구조화 데이터

**layout.tsx — WebSite 스키마:**
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "서울 결정고시 모니터",
  "url": "https://seoul-urban-plan-monitor.2lee.kr",
  "description": "서울시 도시계획 결정고시를 매일 수집·분석합니다."
}
```

**개별 고시문 — Article 스키마:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "고시문 제목",
  "datePublished": "2026-03-19",
  "author": { "@type": "Organization", "name": "고시기관명" },
  "publisher": { "@type": "Organization", "name": "서울 결정고시 모니터" },
  "description": "content 앞 150자"
}
```

**정책 페이지 (plan, gangbuk, southwest) — Article 스키마:**
- 각 페이지 주제에 맞는 headline + description

### 4. Sitemap 확장

`sitemap.ts`를 동적으로 변경:
- 정적 페이지 6개 (home, plan, gangbuk, southwest, privacy, terms)
- 개별 고시문 2,800+개 (`/gosi/{notice_code}`)
- 각 고시문의 lastModified = notice_date

### 5. 에드센스 배치

개별 고시문 페이지 하단에 AdBanner 컴포넌트 배치.
승인 전이므로 슬롯은 플레이스홀더 값 사용, 승인 후 실제 슬롯 ID로 교체.

## Out of Scope

- AI 분석/인사이트 표시 (WordPress와 차별화를 위해 제외)
- 지도 임베드 (개별 페이지에서는 불필요, 메인 대시보드에 이미 있음)
- favicon/manifest (별도 작업)

## Implementation Order

1. 도메인 교체 (layout, sitemap, robots)
2. `lib/data.ts` 유틸 함수 추가
3. `/gosi/[notice_code]/page.tsx` 생성
4. sitemap 동적 확장
5. JSON-LD 구조화 데이터 추가
6. 누락 메타데이터 보완 (privacy, terms, southwest)
7. 빌드 테스트
