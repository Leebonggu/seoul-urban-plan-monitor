# 1-2. 네이버 블로그 SEO 최적화 구현 플랜

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 네이버 블로그 반자동 발행의 제목과 본문을 SEO 최적화하여 검색 유입을 극대화한다.

**Architecture:** 기존 `web/src/lib/blogTemplate.ts`의 제목 생성 로직을 SEO 패턴으로 변경하고, 본문 하단에 대시보드 사이트 링크를 추가한다. admin 페이지 UX는 기존 그대로 유지.

**Tech Stack:** TypeScript (Next.js)

**Spec:** `docs/superpowers/specs/2026-03-22-monetization-design.md` 1-2 참조

---

## 파일 구조

| 파일 | 역할 |
|------|------|
| `web/src/lib/blogTemplate.ts` | 블로그 제목/본문 생성 (수정) |

---

## Task 1: 블로그 제목 SEO 최적화

**Files:**
- Modify: `web/src/lib/blogTemplate.ts`

- [ ] **Step 1: 현재 blogTemplate.ts 읽기**

```bash
cat web/src/lib/blogTemplate.ts
```

현재 제목 패턴: `[서울 도시계획] {record.title}`

- [ ] **Step 2: 제목 패턴 변경**

기존 제목 생성 로직을 다음으로 교체:

```typescript
// SEO 최적화 제목: [지역구] 키워드 결정고시 (날짜) — 상세
function generateTitle(record: GosiRecord): string {
  const location = record.location?.split(" ")[0] || record.organ_name || "서울";
  const date = record.notice_date;
  const titleText = record.title.length > 40
    ? record.title.substring(0, 40) + "..."
    : record.title;
  return `${location} ${record.notice_type || "도시계획"} 결정고시 (${date}) — ${titleText}`;
}
```

- [ ] **Step 3: 본문 하단에 대시보드 링크 추가**

`generateBlogContent` 함수의 본문 끝에 추가:

```typescript
// 대시보드 링크
body += `\n\n---\n`;
body += `더 많은 서울시 결정고시를 한눈에 보려면:\n`;
body += `👉 서울 결정고시 모니터: https://seoul-gosi-monitor.vercel.app\n`;
```

주의: Vercel 배포 URL은 실제 도메인 확정 후 수정 필요.

- [ ] **Step 4: 빌드 확인**

```bash
cd web && npx next build
```

Expected: 빌드 성공

- [ ] **Step 5: Commit**

```bash
git add web/src/lib/blogTemplate.ts
git commit -m "feat: 네이버 블로그 제목 SEO 최적화 + 대시보드 링크 추가"
```
