import type { Metadata } from "next";
import { loadAllData, computeAggregatedData } from "@/lib/data";
import Dashboard from "@/components/Dashboard";

export const dynamic = "force-static";

const INITIAL_PAGE_SIZE = 30;

export const metadata: Metadata = {
  title: "서울 결정고시 모니터 — 도시계획 결정고시 매일 분석",
  description:
    "서울시 도시계획 결정고시를 매일 수집하여 중심지체계별로 분석합니다. 재개발·용적률·용도변경 등 핵심 고시문을 한눈에 확인하세요.",
  openGraph: {
    title: "서울 결정고시 모니터",
    description:
      "서울시 도시계획 결정고시를 매일 수집·분석. 2040 서울플랜 중심지체계 기반 투자 인사이트.",
  },
};

export default function Home() {
  const records = loadAllData();
  const aggregated = computeAggregatedData(records);

  // 초기에는 최근 N건만 + content 제외
  const initialRecords = records.slice(0, INITIAL_PAGE_SIZE).map(
    ({ content, ...rest }) => rest
  );

  return (
    <Dashboard
      initialRecords={initialRecords}
      initialTotal={records.length}
      aggregated={aggregated}
    />
  );
}
