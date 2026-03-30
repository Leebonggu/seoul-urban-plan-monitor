"use client";

import Link from "next/link";
import { GosiRecord } from "@/lib/types";
import { GRADE_COLORS } from "@/lib/centers";

interface Props {
  records: GosiRecord[];
  maxItems?: number;
}

export default function GosiList({ records, maxItems = 20 }: Props) {
  const items = records.slice(0, maxItems);

  if (items.length === 0) {
    return (
      <p className="text-gray-400 text-center py-8">
        조건에 맞는 고시문이 없습니다.
      </p>
    );
  }

  return (
    <div className="space-y-1">
      {items.map((r) => (
        <div
          key={r.notice_code}
          className="border-b border-gray-100 py-3 last:border-0"
        >
          <div className="flex flex-wrap items-center gap-1.5 mb-1">
            <span className="text-xs text-gray-500 font-mono">
              {r.notice_date}
            </span>
            {r.center_grade && (
              <span
                className="text-xs px-1.5 py-0.5 rounded font-medium text-white"
                style={{
                  backgroundColor: GRADE_COLORS[r.center_grade] || "#999",
                }}
              >
                {r.center_grade}·{r.center_name}
              </span>
            )}
            {r.category && r.category !== "결정고시" && (
              <span className="text-xs px-1.5 py-0.5 rounded bg-purple-100 text-purple-700 font-medium">
                {r.category}
              </span>
            )}
            <span className="text-xs text-gray-500">{r.organ_name}</span>
          </div>
          <Link
            href={`/gosi/${r.notice_code}`}
            className="text-sm font-medium leading-snug hover:text-blue-600 transition-colors block"
          >
            {r.title.length > 65 ? r.title.slice(0, 65) + "..." : r.title}
          </Link>
          <div className="flex items-center gap-2 mt-1">
            {r.location && (
              <span className="text-xs text-gray-500">📍 {r.location}</span>
            )}
            {r.page_url && (
              <a
                href={r.page_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-blue-600 hover:underline"
                aria-label={`${r.title} 상세 페이지`}
              >
                상세
              </a>
            )}
            {r.doc_url && (
              <a
                href={r.doc_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-blue-600 hover:underline"
                aria-label={`${r.title} 원문 PDF`}
              >
                원문
              </a>
            )}
          </div>
        </div>
      ))}
      {records.length > maxItems && (
        <p className="text-xs text-gray-400 text-center pt-2">
          외 {(records.length - maxItems).toLocaleString()}건
        </p>
      )}
    </div>
  );
}
