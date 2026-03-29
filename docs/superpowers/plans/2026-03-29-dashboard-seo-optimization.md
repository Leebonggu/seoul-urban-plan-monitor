# Dashboard SEO Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Maximize search engine exposure for the Next.js dashboard by switching to the custom domain, creating 2,800+ individual notice pages, and adding structured data.

**Architecture:** Replace hardcoded Vercel domain with `seoul-urban-plan-monitor.2lee.kr` across all SEO files. Add a dynamic route `/gosi/[notice_code]` that statically generates a page per notice at build time. Extend sitemap to include all pages. Add JSON-LD structured data for search engine rich snippets.

**Tech Stack:** Next.js 16 (App Router, SSG), TypeScript, Tailwind CSS

---

### Task 1: Replace domain across all SEO files

**Files:**
- Modify: `web/src/app/layout.tsx:7`
- Modify: `web/src/app/sitemap.ts:3`
- Modify: `web/src/app/robots.ts:8`

- [ ] **Step 1: Update layout.tsx SITE_URL**

In `web/src/app/layout.tsx`, change line 7:

```typescript
// Before
const SITE_URL = "https://seoul-gosi-monitor.vercel.app";

// After
const SITE_URL = "https://seoul-urban-plan-monitor.2lee.kr";
```

- [ ] **Step 2: Update sitemap.ts BASE_URL**

In `web/src/app/sitemap.ts`, change line 3:

```typescript
// Before
const BASE_URL = "https://seoul-gosi-monitor.vercel.app";

// After
const BASE_URL = "https://seoul-urban-plan-monitor.2lee.kr";
```

- [ ] **Step 3: Update robots.ts sitemap URL**

In `web/src/app/robots.ts`, change the sitemap value:

```typescript
// Before
sitemap: "https://seoul-gosi-monitor.vercel.app/sitemap.xml",

// After
sitemap: "https://seoul-urban-plan-monitor.2lee.kr/sitemap.xml",
```

- [ ] **Step 4: Verify no other hardcoded references remain**

Run: `grep -r "seoul-gosi-monitor.vercel.app" web/src/`
Expected: No matches

- [ ] **Step 5: Commit**

```bash
git add web/src/app/layout.tsx web/src/app/sitemap.ts web/src/app/robots.ts
git commit -m "fix: 대시보드 도메인 seoul-urban-plan-monitor.2lee.kr로 교체"
```

---

### Task 2: Add data utility functions

**Files:**
- Modify: `web/src/lib/data.ts`

- [ ] **Step 1: Add loadRecordByCode and loadAllNoticeCodes to data.ts**

Append to `web/src/lib/data.ts` after the existing `loadAllData()` function:

```typescript
export function loadAllNoticeCodes(): string[] {
  return loadAllData().map((r) => r.notice_code);
}

export function loadRecordByCode(code: string): GosiRecord | undefined {
  return loadAllData().find((r) => r.notice_code === code);
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/lib/data.ts
git commit -m "feat: 고시문 단건 조회 유틸 함수 추가"
```

---

### Task 3: Create individual notice page route

**Files:**
- Create: `web/src/app/gosi/[notice_code]/page.tsx`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p web/src/app/gosi/\[notice_code\]
```

- [ ] **Step 2: Create the page component**

Create `web/src/app/gosi/[notice_code]/page.tsx`:

```tsx
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { loadAllNoticeCodes, loadRecordByCode } from "@/lib/data";
import { GRADE_COLORS } from "@/lib/centers";
import AdBanner from "@/components/AdBanner";

export const dynamic = "force-static";

interface Props {
  params: Promise<{ notice_code: string }>;
}

export async function generateStaticParams() {
  const codes = loadAllNoticeCodes();
  return codes.map((code) => ({ notice_code: code }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { notice_code } = await params;
  const record = loadRecordByCode(notice_code);
  if (!record) return {};

  const location = record.location || record.site_name || "";
  const titleText = record.title.length > 50
    ? record.title.slice(0, 50) + "..."
    : record.title;
  const title = location
    ? `${location} ${titleText}`
    : titleText;

  const description =
    record.content.slice(0, 150).replace(/\n/g, " ") +
    "... 서울시 도시계획 결정고시 원문";

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      type: "article",
    },
  };
}

export default async function GosiDetailPage({ params }: Props) {
  const { notice_code } = await params;
  const record = loadRecordByCode(notice_code);
  if (!record) notFound();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: record.title,
    datePublished: record.notice_date,
    author: {
      "@type": "Organization",
      name: record.organ_name,
    },
    publisher: {
      "@type": "Organization",
      name: "서울 결정고시 모니터",
    },
    description: record.content.slice(0, 150).replace(/\n/g, " "),
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Header */}
      <div className="mb-6">
        <div className="flex flex-wrap items-center gap-2 mb-2">
          {record.center_grade && (
            <span
              className="text-xs px-2 py-1 rounded font-medium text-white"
              style={{
                backgroundColor: GRADE_COLORS[record.center_grade] || "#999",
              }}
            >
              {record.center_grade}·{record.center_name}
            </span>
          )}
          {record.category && record.category !== "결정고시" && (
            <span className="text-xs px-2 py-1 rounded bg-purple-100 text-purple-700 font-medium">
              {record.category}
            </span>
          )}
          {record.location && (
            <span className="text-sm text-gray-500">{record.location}</span>
          )}
        </div>
        <h1 className="text-xl font-bold leading-tight">{record.title}</h1>
      </div>

      {/* Metadata Table */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <table className="w-full text-sm">
          <tbody>
            <tr className="border-b border-gray-200">
              <td className="py-2 pr-4 text-gray-500 font-medium w-24">고시번호</td>
              <td className="py-2">{record.notice_no}</td>
            </tr>
            <tr className="border-b border-gray-200">
              <td className="py-2 pr-4 text-gray-500 font-medium">고시일</td>
              <td className="py-2">{record.notice_date}</td>
            </tr>
            <tr className="border-b border-gray-200">
              <td className="py-2 pr-4 text-gray-500 font-medium">고시기관</td>
              <td className="py-2">{record.organ_name}</td>
            </tr>
            {record.location && (
              <tr className="border-b border-gray-200">
                <td className="py-2 pr-4 text-gray-500 font-medium">위치</td>
                <td className="py-2">{record.location}</td>
              </tr>
            )}
            <tr>
              <td className="py-2 pr-4 text-gray-500 font-medium">유형</td>
              <td className="py-2">{record.notice_type}</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Content */}
      <div className="prose prose-sm max-w-none mb-6">
        <h2 className="text-lg font-bold mb-3">고시 원문</h2>
        <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
          {record.content}
        </div>
      </div>

      {/* Links */}
      <div className="flex flex-wrap gap-3 mb-8">
        {record.doc_url && (
          <a
            href={record.doc_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm px-4 py-2 rounded-lg bg-blue-50 text-blue-700 hover:bg-blue-100 transition-colors"
          >
            원문 PDF
          </a>
        )}
        {record.page_url && (
          <a
            href={record.page_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm px-4 py-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
          >
            출처 페이지
          </a>
        )}
      </div>

      {/* Back link */}
      <div className="border-t border-gray-200 pt-4 mb-6">
        <Link
          href="/"
          className="text-sm text-blue-600 hover:underline"
        >
          &larr; 전체 고시문 목록
        </Link>
      </div>

      <AdBanner slot="SLOT_GOSI_DETAIL" className="mt-4" />
    </div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add web/src/app/gosi/\[notice_code\]/page.tsx
git commit -m "feat: 개별 고시문 상세 페이지 (/gosi/[notice_code])"
```

---

### Task 4: Expand sitemap with all notice URLs

**Files:**
- Modify: `web/src/app/sitemap.ts`

- [ ] **Step 1: Rewrite sitemap.ts to include all pages**

Replace the entire content of `web/src/app/sitemap.ts`:

```typescript
import type { MetadataRoute } from "next";
import { loadAllData } from "@/lib/data";

const BASE_URL = "https://seoul-urban-plan-monitor.2lee.kr";

export default function sitemap(): MetadataRoute.Sitemap {
  const records = loadAllData();

  const staticPages: MetadataRoute.Sitemap = [
    {
      url: BASE_URL,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1,
    },
    {
      url: `${BASE_URL}/plan`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/gangbuk`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/southwest`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/privacy`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "yearly",
      priority: 0.3,
    },
    {
      url: `${BASE_URL}/terms`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "yearly",
      priority: 0.3,
    },
  ];

  const gosiPages: MetadataRoute.Sitemap = records.map((r) => ({
    url: `${BASE_URL}/gosi/${r.notice_code}`,
    lastModified: new Date(r.notice_date),
    changeFrequency: "never" as const,
    priority: 0.6,
  }));

  return [...staticPages, ...gosiPages];
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/app/sitemap.ts
git commit -m "feat: sitemap 확장 — 전체 고시문 2800+ URL 포함"
```

---

### Task 5: Add JSON-LD structured data to layout

**Files:**
- Modify: `web/src/app/layout.tsx`

- [ ] **Step 1: Add WebSite JSON-LD to the `<head>` in layout.tsx**

In `web/src/app/layout.tsx`, add the JSON-LD script inside the `<head>` tag, right before the AdSense Script:

```tsx
<head>
  <script
    type="application/ld+json"
    dangerouslySetInnerHTML={{
      __html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "WebSite",
        name: SITE_NAME,
        url: SITE_URL,
        description: SITE_DESC,
      }),
    }}
  />
  {process.env.NEXT_PUBLIC_ADSENSE_ID && (
    <Script
      async
      src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${process.env.NEXT_PUBLIC_ADSENSE_ID}`}
      crossOrigin="anonymous"
      strategy="afterInteractive"
    />
  )}
</head>
```

- [ ] **Step 2: Commit**

```bash
git add web/src/app/layout.tsx
git commit -m "feat: WebSite JSON-LD 구조화 데이터 추가"
```

---

### Task 6: Add missing metadata to privacy and terms pages

**Files:**
- Modify: `web/src/app/privacy/page.tsx`
- Modify: `web/src/app/terms/page.tsx`

- [ ] **Step 1: Add metadata export to privacy/page.tsx**

Add at the top of `web/src/app/privacy/page.tsx`, before the component:

```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "개인정보처리방침",
  description:
    "서울 결정고시 모니터의 개인정보처리방침. 수집하는 개인정보, 쿠키 및 광고, 데이터 출처 안내.",
};
```

- [ ] **Step 2: Add metadata export to terms/page.tsx**

Add at the top of `web/src/app/terms/page.tsx`, before the component:

```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "이용약관",
  description:
    "서울 결정고시 모니터 이용약관. 서비스 개요, 데이터 정확성, 분석 콘텐츠, 저작권 안내.",
};
```

- [ ] **Step 3: Commit**

```bash
git add web/src/app/privacy/page.tsx web/src/app/terms/page.tsx
git commit -m "feat: privacy, terms 페이지 메타데이터 추가"
```

---

### Task 7: Link GosiList items to detail pages

**Files:**
- Modify: `web/src/components/GosiList.tsx`

- [ ] **Step 1: Add Link import and wrap titles**

In `web/src/components/GosiList.tsx`:

1. Add import at line 2: `import Link from "next/link";`
2. Wrap the title `<p>` tag (line 51) with a Link to the detail page:

Replace:
```tsx
<p className="text-sm font-medium leading-snug">
  {r.title.length > 65 ? r.title.slice(0, 65) + "..." : r.title}
</p>
```

With:
```tsx
<Link
  href={`/gosi/${r.notice_code}`}
  className="text-sm font-medium leading-snug hover:text-blue-600 transition-colors block"
>
  {r.title.length > 65 ? r.title.slice(0, 65) + "..." : r.title}
</Link>
```

- [ ] **Step 2: Commit**

```bash
git add web/src/components/GosiList.tsx
git commit -m "feat: 고시문 목록에서 상세 페이지 링크 연결"
```

---

### Task 8: Build test

- [ ] **Step 1: Run the Next.js build**

```bash
cd web && npm run build
```

Expected: Build succeeds. Static pages generated including `/gosi/[notice_code]` entries.
Note: The build will take longer than usual due to 2,800+ static pages.

- [ ] **Step 2: Spot-check the build output**

Look for lines like:
```
├ ○ /gosi/[notice_code]    (2834 entries)
```

- [ ] **Step 3: Commit any build-related fixes if needed**
