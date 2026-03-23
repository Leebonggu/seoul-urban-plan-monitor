import type { Metadata } from "next";
import SouthwestPlan from "@/components/SouthwestPlan";

export const dynamic = "force-static";

export const metadata: Metadata = {
  title: "서남권 대개조 2.0 요약",
  description:
    "서울시 서남권 대개조 2.0 정책 핵심 요약. 7.3조 투자, 준공업지역 용적률 400%, 남부순환 지하도로, 마곡·G밸리 산업 거점 혁신.",
  openGraph: {
    title: "서남권 대개조 2.0 요약 | 서울 결정고시 모니터",
    description:
      "서남권 7.3조 투자, 용적률 400%, 남부순환 지하도로 15km — 2040 서울플랜과 교차 분석.",
  },
};

export default function SouthwestPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <SouthwestPlan />
    </div>
  );
}
