"use client";

import Script from "next/script";
import { useEffect, useRef } from "react";

interface Props {
  id: number;
  trackingCode?: string;
  className?: string;
}

declare global {
  interface Window {
    PartnersCoupang?: { G: new (opts: object) => void };
  }
}

export default function CoupangBanner({ id, trackingCode = "AF1900878", className = "" }: Props) {
  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current || !window.PartnersCoupang) return;
    initialized.current = true;
    new window.PartnersCoupang.G({
      id,
      template: "carousel",
      trackingCode,
      width: "100%",
      height: "140",
      tsource: "",
    });
  });

  return (
    <div className={className}>
      <p className="text-xs text-gray-400 mb-1">
        이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
      </p>
      <Script
        src="https://ads-partners.coupang.com/g.js"
        strategy="afterInteractive"
        onLoad={() => {
          if (initialized.current || !window.PartnersCoupang) return;
          initialized.current = true;
          new window.PartnersCoupang.G({
            id,
            template: "carousel",
            trackingCode,
            width: "100%",
            height: "140",
            tsource: "",
          });
        }}
      />
    </div>
  );
}
