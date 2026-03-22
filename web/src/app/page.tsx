import { loadAllData } from "@/lib/data";
import Dashboard from "@/components/Dashboard";

export const dynamic = "force-static";

export default function Home() {
  const records = loadAllData();

  return <Dashboard records={records} />;
}
