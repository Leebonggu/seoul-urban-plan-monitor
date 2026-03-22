# 1-3. 대시보드 사이트 애드센스 구현 플랜

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 대시보드 사이트에 구글 애드센스를 삽입하고, 승인에 필요한 개인정보처리방침/이용약관 페이지를 추가한다.

**Architecture:** `AdBanner` 공통 컴포넌트를 만들어 각 페이지에 배치. 애드센스 스크립트는 `layout.tsx`에 삽입. `/privacy`, `/terms` 정적 페이지 추가.

**Tech Stack:** Next.js, Google AdSense

**Spec:** `docs/superpowers/specs/2026-03-22-monetization-design.md` 1-3 참조

---

## 파일 구조

| 파일 | 역할 |
|------|------|
| `web/src/components/AdBanner.tsx` | 애드센스 광고 슬롯 공통 컴포넌트 |
| `web/src/app/layout.tsx` | 애드센스 스크립트 삽입 (수정) |
| `web/src/components/Dashboard.tsx` | 광고 배치 (수정) |
| `web/src/components/SeoulPlan.tsx` | 광고 배치 (수정) |
| `web/src/components/GangbukPlan.tsx` | 광고 배치 (수정) |
| `web/src/app/privacy/page.tsx` | 개인정보처리방침 페이지 |
| `web/src/app/terms/page.tsx` | 이용약관 페이지 |
| `web/src/components/Nav.tsx` | 하단 푸터 링크 추가 (수정) 또는 별도 Footer 컴포넌트 |
| `web/src/components/Footer.tsx` | 푸터 (개인정보/약관 링크, 저작권) |

---

## Task 1: AdBanner 공통 컴포넌트

**Files:**
- Create: `web/src/components/AdBanner.tsx`

- [ ] **Step 1: 구현**

```tsx
// web/src/components/AdBanner.tsx
"use client";

import { useEffect } from "react";

interface Props {
  slot: string;           // 애드센스 광고 슬롯 ID
  format?: string;        // auto, horizontal, vertical 등
  className?: string;
}

export default function AdBanner({ slot, format = "auto", className = "" }: Props) {
  useEffect(() => {
    try {
      // @ts-expect-error adsbygoogle is injected by external script
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch {
      // 애드센스 스크립트 미로드 시 무시
    }
  }, []);

  return (
    <div className={`ad-container ${className}`}>
      <ins
        className="adsbygoogle"
        style={{ display: "block" }}
        data-ad-client={process.env.NEXT_PUBLIC_ADSENSE_ID || ""}
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive="true"
      />
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/components/AdBanner.tsx
git commit -m "feat: AdBanner 공통 컴포넌트 추가"
```

---

## Task 2: layout.tsx에 애드센스 스크립트 삽입

**Files:**
- Modify: `web/src/app/layout.tsx`

- [ ] **Step 1: `<head>`에 애드센스 스크립트 추가**

`layout.tsx`의 `<html>` 태그 안에 `<head>` 추가:

```tsx
import Script from "next/script";

// ... 기존 코드 ...

return (
  <html lang="ko">
    <head>
      {process.env.NEXT_PUBLIC_ADSENSE_ID && (
        <Script
          async
          src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${process.env.NEXT_PUBLIC_ADSENSE_ID}`}
          crossOrigin="anonymous"
          strategy="afterInteractive"
        />
      )}
    </head>
    <body className="bg-gray-50 text-gray-900 antialiased">
      <Nav />
      {children}
      <Footer />
    </body>
  </html>
);
```

환경변수 `NEXT_PUBLIC_ADSENSE_ID`가 없으면 스크립트를 삽입하지 않으므로, 애드센스 승인 전에도 안전하게 배포 가능.

- [ ] **Step 2: Commit**

```bash
git add web/src/app/layout.tsx
git commit -m "feat: 애드센스 스크립트 조건부 삽입"
```

---

## Task 3: Footer 컴포넌트

**Files:**
- Create: `web/src/components/Footer.tsx`
- Modify: `web/src/app/layout.tsx` (Footer import 추가)

- [ ] **Step 1: 구현**

```tsx
// web/src/components/Footer.tsx
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-white mt-12">
      <div className="max-w-7xl mx-auto px-4 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
        <p className="text-xs text-gray-400">
          데이터 출처: 서울도시공간포털 (urban.seoul.go.kr)
        </p>
        <div className="flex gap-4 text-xs text-gray-400">
          <Link href="/privacy" className="hover:text-gray-600">
            개인정보처리방침
          </Link>
          <Link href="/terms" className="hover:text-gray-600">
            이용약관
          </Link>
        </div>
      </div>
    </footer>
  );
}
```

- [ ] **Step 2: layout.tsx에 Footer import 및 배치**

`layout.tsx`에서 `<Footer />`를 `{children}` 아래에 추가. (Task 2에서 이미 포함.)

- [ ] **Step 3: Commit**

```bash
git add web/src/components/Footer.tsx web/src/app/layout.tsx
git commit -m "feat: Footer 컴포넌트 추가 (개인정보/약관 링크)"
```

---

## Task 4: 개인정보처리방침 페이지

**Files:**
- Create: `web/src/app/privacy/page.tsx`

- [ ] **Step 1: 구현**

```tsx
// web/src/app/privacy/page.tsx
export const dynamic = "force-static";

export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-bold mb-6">개인정보처리방침</h1>
      <div className="prose prose-sm text-gray-600 space-y-4">
        <p>
          서울 결정고시 모니터(이하 &quot;서비스&quot;)는 이용자의 개인정보를
          중요시하며, 관련 법령을 준수합니다.
        </p>

        <h2 className="text-lg font-bold mt-6">1. 수집하는 개인정보</h2>
        <p>
          본 서비스는 별도의 회원가입 없이 이용할 수 있으며, 개인정보를 직접
          수집하지 않습니다.
        </p>

        <h2 className="text-lg font-bold mt-6">2. 쿠키 및 광고</h2>
        <p>
          본 서비스는 Google AdSense를 통해 광고를 게재하며, 이 과정에서
          쿠키가 사용될 수 있습니다. Google의 쿠키 사용에 대한 자세한 내용은{" "}
          <a
            href="https://policies.google.com/technologies/ads"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            Google 광고 정책
          </a>
          을 참조하세요.
        </p>

        <h2 className="text-lg font-bold mt-6">3. 데이터 출처</h2>
        <p>
          본 서비스에서 제공하는 고시문 데이터는 서울도시공간포털
          (urban.seoul.go.kr)에서 공개한 공공데이터를 활용합니다.
        </p>

        <h2 className="text-lg font-bold mt-6">4. 문의</h2>
        <p>
          개인정보 관련 문의사항은 서비스 운영자에게 연락해 주세요.
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/app/privacy/page.tsx
git commit -m "feat: 개인정보처리방침 페이지 추가"
```

---

## Task 5: 이용약관 페이지

**Files:**
- Create: `web/src/app/terms/page.tsx`

- [ ] **Step 1: 구현**

```tsx
// web/src/app/terms/page.tsx
export const dynamic = "force-static";

export default function TermsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-bold mb-6">이용약관</h1>
      <div className="prose prose-sm text-gray-600 space-y-4">
        <h2 className="text-lg font-bold mt-6">1. 서비스 개요</h2>
        <p>
          서울 결정고시 모니터는 서울시 도시계획 결정고시를 수집·분석하여
          제공하는 정보 서비스입니다.
        </p>

        <h2 className="text-lg font-bold mt-6">2. 데이터 정확성</h2>
        <p>
          본 서비스는 서울도시공간포털의 공공데이터를 기반으로 하며, 데이터의
          정확성을 보장하지 않습니다. 정확한 정보는 원문을 확인해 주세요.
        </p>

        <h2 className="text-lg font-bold mt-6">3. 분석 콘텐츠</h2>
        <p>
          본 서비스에서 제공하는 분석 및 인사이트는 참고용이며, 투자 판단의
          근거로 사용하기에 부적합합니다. 투자 결정은 이용자 본인의 판단과
          책임 하에 이루어져야 합니다.
        </p>

        <h2 className="text-lg font-bold mt-6">4. 저작권</h2>
        <p>
          고시문 원문은 공공저작물로서 출처 표시 시 자유 이용이 가능합니다.
          본 서비스의 분석 콘텐츠 및 디자인에 대한 저작권은 서비스 운영자에게
          있습니다.
        </p>

        <h2 className="text-lg font-bold mt-6">5. 면책</h2>
        <p>
          본 서비스 이용으로 발생하는 직·간접적 손해에 대해 서비스 운영자는
          책임을 지지 않습니다.
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/app/terms/page.tsx
git commit -m "feat: 이용약관 페이지 추가"
```

---

## Task 6: 각 페이지에 광고 슬롯 배치

**Files:**
- Modify: `web/src/components/Dashboard.tsx`
- Modify: `web/src/components/SeoulPlan.tsx`
- Modify: `web/src/components/GangbukPlan.tsx`

- [ ] **Step 1: Dashboard 하단에 광고 배치**

`Dashboard.tsx`의 마지막 `</div>` 직전에 추가:

```tsx
import AdBanner from "./AdBanner";

// ... 컴포넌트 끝 부분, 하단 탭 div 아래에:
<AdBanner slot="SLOT_ID_1" className="mt-6" />
```

- [ ] **Step 2: SeoulPlan 섹션 사이에 광고 배치**

`SeoulPlan.tsx`의 "도시공간구조" 섹션과 "중심지 체계" 섹션 사이에:

```tsx
import AdBanner from "./AdBanner";

// 도시공간구조 섹션 끝과 중심지 체계 섹션 시작 사이에:
<AdBanner slot="SLOT_ID_2" className="my-6" />
```

- [ ] **Step 3: GangbukPlan 섹션 사이에 광고 배치**

`GangbukPlan.tsx`의 "핵심 교통 사업" 섹션과 "성장거점" 섹션 사이에:

```tsx
import AdBanner from "./AdBanner";

// 교통 사업 섹션 끝과 성장거점 섹션 시작 사이에:
<AdBanner slot="SLOT_ID_3" className="my-6" />
```

- [ ] **Step 4: 빌드 확인**

```bash
cd web && npx next build
```

Expected: 빌드 성공. 애드센스 ID 없이도 에러 없이 동작.

- [ ] **Step 5: Commit**

```bash
git add web/src/components/Dashboard.tsx web/src/components/SeoulPlan.tsx web/src/components/GangbukPlan.tsx
git commit -m "feat: 각 페이지에 애드센스 광고 슬롯 배치"
```

---

## Task 7: 환경변수 설정 가이드

- [ ] **Step 1: Vercel에 환경변수 설정 (수동)**

Vercel 대시보드 → Settings → Environment Variables:
- `NEXT_PUBLIC_ADSENSE_ID`: 구글 애드센스 Publisher ID (예: `ca-pub-XXXXXXXXXX`)

애드센스 승인 완료 후 설정. 승인 전에는 비워두면 광고 코드가 렌더링되지 않음.

- [ ] **Step 2: 각 AdBanner의 `slot` prop을 실제 광고 단위 ID로 교체 (수동)**

애드센스 대시보드에서 광고 단위 생성 후, `SLOT_ID_1`, `SLOT_ID_2`, `SLOT_ID_3`을 실제 값으로 교체.
