import type { Metadata } from "next";
import Script from "next/script";
import "./globals.css";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";

const SITE_URL = "https://seoul-urban-plan-monitor.2lee.kr";
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
  icons: {
    icon: [
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
    ],
    apple: "/apple-touch-icon.png",
  },
  openGraph: {
    title: SITE_NAME,
    description: SITE_DESC,
    url: SITE_URL,
    siteName: SITE_NAME,
    locale: "ko_KR",
    type: "website",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: SITE_NAME,
      },
    ],
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
    google: "FXncF_H5GbKmmq5_GngTbwnNCljEHwJirfkI5F104ag",
    other: {
      "naver-site-verification": "1d61bc5963d50d4b2ca6d5338399b1a7b8256736",
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
      <body className="bg-gray-50 text-gray-900 antialiased">
        <Nav />
        {children}
        <Footer />
      </body>
    </html>
  );
}
