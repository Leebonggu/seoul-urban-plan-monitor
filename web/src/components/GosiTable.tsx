"use client";

import { useState } from "react";
import { GosiRecord } from "@/lib/types";
import { GRADE_COLORS } from "@/lib/centers";

interface Props {
  records: GosiRecord[];
}

const PAGE_SIZE = 30;

export default function GosiTable({ records }: Props) {
  const [page, setPage] = useState(0);
  const totalPages = Math.ceil(records.length / PAGE_SIZE);
  const paged = records.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  return (
    <div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 text-left text-gray-500">
              <th className="py-2 px-2 font-medium">고시일</th>
              <th className="py-2 px-2 font-medium">기관</th>
              <th className="py-2 px-2 font-medium">위치</th>
              <th className="py-2 px-2 font-medium">등급</th>
              <th className="py-2 px-2 font-medium">제목</th>
              <th className="py-2 px-2 font-medium">링크</th>
            </tr>
          </thead>
          <tbody>
            {paged.map((r) => (
              <tr
                key={r.notice_code}
                className="border-b border-gray-50 hover:bg-gray-50"
              >
                <td className="py-2 px-2 font-mono text-xs whitespace-nowrap">
                  {r.notice_date}
                </td>
                <td className="py-2 px-2 text-xs whitespace-nowrap">
                  {r.organ_name}
                </td>
                <td className="py-2 px-2 text-xs max-w-[150px] truncate">
                  {r.location || "-"}
                </td>
                <td className="py-2 px-2">
                  {r.center_grade ? (
                    <span
                      className="text-xs px-1.5 py-0.5 rounded text-white whitespace-nowrap"
                      style={{
                        backgroundColor:
                          GRADE_COLORS[r.center_grade] || "#999",
                      }}
                    >
                      {r.center_name}
                    </span>
                  ) : (
                    <span className="text-xs text-gray-300">-</span>
                  )}
                </td>
                <td className="py-2 px-2 max-w-[300px] truncate">
                  {r.title}
                </td>
                <td className="py-2 px-2 whitespace-nowrap">
                  {r.page_url && (
                    <a
                      href={r.page_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-blue-500 hover:underline mr-2"
                    >
                      상세
                    </a>
                  )}
                  {r.doc_url && (
                    <a
                      href={r.doc_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-blue-500 hover:underline"
                    >
                      원문
                    </a>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center justify-between mt-4 text-sm text-gray-500">
        <span>
          총 {records.length.toLocaleString()}건 중 {page * PAGE_SIZE + 1}-
          {Math.min((page + 1) * PAGE_SIZE, records.length)}
        </span>
        <div className="flex gap-2">
          <button
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="px-3 py-1 rounded border border-gray-200 disabled:opacity-30 hover:bg-gray-100"
          >
            이전
          </button>
          <button
            onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1}
            className="px-3 py-1 rounded border border-gray-200 disabled:opacity-30 hover:bg-gray-100"
          >
            다음
          </button>
        </div>
      </div>
    </div>
  );
}
