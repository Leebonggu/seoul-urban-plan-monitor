import fs from "fs";
import path from "path";
import { GosiRecord, AggregatedData } from "./types";
import { CENTERS } from "./centers";

const DATA_DIR =
  process.env.DATA_DIR || path.join(process.cwd(), "..", "data");

let _cachedRecords: GosiRecord[] | null = null;
let _cachedIndex: Map<string, GosiRecord> | null = null;

export function loadAllData(): GosiRecord[] {
  if (_cachedRecords) return _cachedRecords;

  const files = fs
    .readdirSync(DATA_DIR)
    .filter((f) => f.endsWith(".json") && f !== "latest.json" && f !== "posted.json" && f !== "wp_published.json")
    .sort()
    .reverse();

  const records: GosiRecord[] = [];
  for (const file of files) {
    const content = fs.readFileSync(path.join(DATA_DIR, file), "utf-8");
    const items: GosiRecord[] = JSON.parse(content);
    records.push(...items);
  }

  records.sort(
    (a, b) =>
      new Date(b.notice_date).getTime() - new Date(a.notice_date).getTime()
  );

  _cachedRecords = records;
  return records;
}

function getIndex(): Map<string, GosiRecord> {
  if (_cachedIndex) return _cachedIndex;
  _cachedIndex = new Map(loadAllData().map((r) => [r.notice_code, r]));
  return _cachedIndex;
}

export function loadAllNoticeCodes(): string[] {
  return loadAllData().map((r) => r.notice_code);
}

export function loadRecordByCode(code: string): GosiRecord | undefined {
  return getIndex().get(code);
}

export function computeAggregatedData(records: GosiRecord[]): AggregatedData {
  const centerCounts: Record<string, number> = {};
  const byMonth: Record<string, number> = {};
  const gradeCounts: Record<string, number> = {};
  const centerNameCounts: Record<string, number> = {};
  let centerMatchedCount = 0;

  for (const r of records) {
    // 중심지 카운트
    if (r.center_name) {
      centerCounts[r.center_name] = (centerCounts[r.center_name] || 0) + 1;
      centerNameCounts[r.center_name] = (centerNameCounts[r.center_name] || 0) + 1;
    }
    // 등급 카운트
    const grade = r.center_grade || "미매칭";
    gradeCounts[grade] = (gradeCounts[grade] || 0) + 1;
    if (r.center_grade) centerMatchedCount++;
    // 월별 카운트
    const month = r.notice_date.slice(0, 7);
    byMonth[month] = (byMonth[month] || 0) + 1;
  }

  const centerToGrade: Record<string, string> = {};
  for (const c of CENTERS) {
    centerToGrade[c.name] = c.grade;
  }

  const centerRanking = Object.entries(centerNameCounts)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 15)
    .map(([name, count]) => ({ name, count, grade: centerToGrade[name] || "" }));

  const monthlyData = Object.entries(byMonth)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([month, count]) => ({ month, count }));

  const gradeData = Object.entries(gradeCounts)
    .map(([name, value]) => ({ name, value }));

  return {
    totalCount: records.length,
    centerMatchedCount,
    latestDate: records.length > 0 ? records[0].notice_date : "-",
    oldestDate: records.length > 0 ? records[records.length - 1].notice_date : "-",
    centerCounts,
    monthlyData,
    gradeData,
    centerRanking,
  };
}

export interface FilterParams {
  category?: string;
  grade?: string;
  centerName?: string;
  keyword?: string;
  page?: number;
  pageSize?: number;
}

export function filterRecords(records: GosiRecord[], params: FilterParams) {
  let result = records;

  if (params.category) {
    result = result.filter((r) => (r.category || "결정고시") === params.category);
  }
  if (params.grade) {
    if (params.grade === "미매칭") {
      result = result.filter((r) => !r.center_grade);
    } else {
      result = result.filter((r) => r.center_grade === params.grade);
    }
  }
  if (params.centerName) {
    result = result.filter((r) => r.center_name === params.centerName);
  }
  if (params.keyword) {
    const kw = params.keyword.toLowerCase();
    result = result.filter(
      (r) =>
        r.title.toLowerCase().includes(kw) ||
        r.content.toLowerCase().includes(kw) ||
        (r.location && r.location.toLowerCase().includes(kw))
    );
  }

  const total = result.length;
  const page = params.page || 0;
  const pageSize = params.pageSize || 30;
  const paged = result.slice(page * pageSize, (page + 1) * pageSize);

  return { records: paged, total, aggregated: computeAggregatedData(result) };
}
