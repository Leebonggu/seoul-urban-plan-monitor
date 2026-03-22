import type { Metadata } from "next";
import GangbukPlan from "@/components/GangbukPlan";

export const dynamic = "force-static";

export const metadata: Metadata = {
  title: "다시강북전성시대 2.0 요약",
  description:
    "서울시 다시강북전성시대 2.0 정책 핵심 요약. 16조 투자, 10대 성장거점, 용적률 1300%, 핵심 교통사업과 2040 서울플랜 교차 인사이트.",
  openGraph: {
    title: "다시강북전성시대 2.0 요약 | 서울 결정고시 모니터",
    description:
      "강북 16조 투자, 10대 성장거점, 용적률 1300% — 2040 서울플랜과 교차 분석.",
  },
};

export default function GangbukPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <GangbukPlan />
    </div>
  );
}
