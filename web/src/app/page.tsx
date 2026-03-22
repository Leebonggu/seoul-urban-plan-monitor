import { loadAllData } from "@/lib/data";
import Dashboard from "@/components/Dashboard";

export const dynamic = "force-static";

export default function Home() {
  const records = loadAllData();

  // 서버→클라이언트 직렬화를 위해 plain object로 변환
  const plainRecords = JSON.parse(JSON.stringify(records));

  return <Dashboard records={plainRecords} />;
}
