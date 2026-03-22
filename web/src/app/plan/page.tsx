import type { Metadata } from "next";
import SeoulPlan from "@/components/SeoulPlan";

export const dynamic = "force-static";

export const metadata: Metadata = {
  title: "2040 서울도시기본계획 요약",
  description:
    "2040 서울도시기본계획의 7대 목표, 도시공간구조, 중심지체계(3도심·7광역·12지역), 4대 혁신축을 핵심 요약합니다.",
  openGraph: {
    title: "2040 서울도시기본계획 요약 | 서울 결정고시 모니터",
    description:
      "서울플랜 2040의 도시공간구조, 중심지체계, 혁신축을 한눈에 정리.",
  },
};

export default function PlanPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <SeoulPlan />
    </div>
  );
}
