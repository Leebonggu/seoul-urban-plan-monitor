import type { Metadata } from "next";
import "./globals.css";
import Nav from "@/components/Nav";

const SITE_URL = "https://seoul-gosi-monitor.vercel.app";
const SITE_NAME = "서울 결정고시 모니터";
const SITE_DESC =
  "서울시 도시계획 결정고시를 매일 수집·분석합니다. 2040 서울도시기본계획 중심지체계(3도심·7광역·12지역) 기반 투자 인사이트를 제공합니다.";

export const metadata: Metadata = {
  title: {
    default: SITE_NAME,
    template: `%s | ${SITE_NAME}`,
  },
  description: SITE_DESC,
  keywords: [
    "서울 결정고시",
    "도시계획",
    "2040 서울플랜",
    "서울도시기본계획",
    "재개발",
    "용적률",
    "중심지체계",
    "강북전성시대",
    "도시계획 결정고시",
  ],
  metadataBase: new URL(SITE_URL),
  openGraph: {
    title: SITE_NAME,
    description: SITE_DESC,
    url: SITE_URL,
    siteName: SITE_NAME,
    locale: "ko_KR",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: SITE_NAME,
    description: SITE_DESC,
  },
  robots: {
    index: true,
    follow: true,
  },
  alternates: {
    canonical: SITE_URL,
  },
  verification: {
    google: "GNwhpS0tCSNTNo8f0iLZ3bTFm521Tz_rBeasgp_h-co",
    other: {
      "naver-site-verification": "c59be0669f84e9039132d0112b50f484d3fa5f44",
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className="bg-gray-50 text-gray-900 antialiased">
        <Nav />
        {children}
      </body>
    </html>
  );
}
