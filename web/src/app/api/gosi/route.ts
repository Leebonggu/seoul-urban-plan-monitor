import { NextRequest, NextResponse } from "next/server";
import { loadAllData, filterRecords } from "@/lib/data";

export async function GET(req: NextRequest) {
  const sp = req.nextUrl.searchParams;

  const params = {
    category: sp.get("category") || undefined,
    grade: sp.get("grade") || undefined,
    centerName: sp.get("centerName") || undefined,
    keyword: sp.get("keyword") || undefined,
    page: Number(sp.get("page") || "0"),
    pageSize: Number(sp.get("pageSize") || "30"),
  };

  const allRecords = loadAllData();
  const result = filterRecords(allRecords, params);

  // content 필드는 목록에서 불필요 → 제외하여 payload 줄임
  const lightRecords = result.records.map(({ content, ...rest }) => rest);

  return NextResponse.json({
    records: lightRecords,
    total: result.total,
    aggregated: result.aggregated,
  });
}
