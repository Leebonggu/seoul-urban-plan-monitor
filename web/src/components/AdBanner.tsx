"use client";

import { useEffect } from "react";

interface Props {
  slot: string;
  format?: string;
  className?: string;
}

export default function AdBanner({ slot, format = "auto", className = "" }: Props) {
  useEffect(() => {
    try {
      // @ts-expect-error adsbygoogle is injected by external script
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch {
      // ignore when adsense script not loaded
    }
  }, []);

  if (!process.env.NEXT_PUBLIC_ADSENSE_ID) return null;

  return (
    <div className={`ad-container ${className}`}>
      <ins
        className="adsbygoogle"
        style={{ display: "block" }}
        data-ad-client={process.env.NEXT_PUBLIC_ADSENSE_ID}
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive="true"
      />
    </div>
  );
}
