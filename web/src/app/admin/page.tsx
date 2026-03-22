import { loadAllData } from "@/lib/data";
import AdminDashboard from "./AdminDashboard";

export const dynamic = "force-static";

export default function AdminPage() {
  const records = loadAllData();
  const plainRecords = JSON.parse(JSON.stringify(records));
  return <AdminDashboard records={plainRecords} />;
}
