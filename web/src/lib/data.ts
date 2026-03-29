import fs from "fs";
import path from "path";
import { GosiRecord } from "./types";

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
