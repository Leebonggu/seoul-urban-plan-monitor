import fs from "fs";
import path from "path";
import { GosiRecord } from "./types";

const DATA_DIR =
  process.env.DATA_DIR || path.join(process.cwd(), "..", "data");

export function loadAllData(): GosiRecord[] {
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

  return records;
}
