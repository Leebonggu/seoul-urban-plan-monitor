"use client";

import { useState, useMemo, useCallback } from "react";
import { GosiRecord } from "@/lib/types";
import { CENTERS, GRADE_COLORS } from "@/lib/centers";
import {
  isPosted,
  markAsPosted,
  unmarkPosted,
  getPostedCount,
  exportPosted,
} from "@/lib/posted";
import { generateBlogContent } from "@/lib/blogTemplate";

const ADMIN_PW = "gosi2026";
const NAVER_BLOG_WRITE_URL = "https://blog.naver.com/GoBlogWrite.naver";

interface Props {
  records: GosiRecord[];
}

export default function AdminDashboard({ records }: Props) {
  const [authenticated, setAuthenticated] = useState(false);
  const [pwInput, setPwInput] = useState("");
  const [grade, setGrade] = useState("");
  const [centerName, setCenterName] = useState("");
  const [keyword, setKeyword] = useState("");
  const [showPosted, setShowPosted] = useState<"all" | "unposted" | "posted">(
    "unposted"
  );
  const [, setRefresh] = useState(0);

  const forceRefresh = useCallback(
    () => setRefresh((n) => n + 1),
    []
  );

  const centerOptions = useMemo(() => {
    if (!grade || grade === "미매칭") return [];
    return CENTERS.filter((c) => c.grade === grade);
  }, [grade]);

  const filtered = useMemo(() => {
    let result = records;

    if (grade) {
      if (grade === "미매칭") {
        result = result.filter((r) => !r.center_grade);
      } else {
        result = result.filter((r) => r.center_grade === grade);
      }
    }
    if (centerName) {
      result = result.filter((r) => r.center_name === centerName);
    }
    if (keyword) {
      const kw = keyword.toLowerCase();
      result = result.filter(
        (r) =>
          r.title.toLowerCase().includes(kw) ||
          r.content.toLowerCase().includes(kw) ||
          (r.location && r.location.toLowerCase().includes(kw))
      );
    }
    if (showPosted === "unposted") {
      result = result.filter((r) => !isPosted(r.notice_code));
    } else if (showPosted === "posted") {
      result = result.filter((r) => isPosted(r.notice_code));
    }

    return result;
  }, [records, grade, centerName, keyword, showPosted]);

  const handleWriteBlog = (record: GosiRecord) => {
    const { title, body } = generateBlogContent(record);

    // 클립보드에 본문 복사
    navigator.clipboard.writeText(body).then(() => {
      alert(
        `📋 블로그 본문이 클립보드에 복사되었습니다.\n\n제목: ${title}\n\n네이버 블로그 글쓰기 페이지가 열립니다.\n제목을 입력하고 본문을 붙여넣기(Ctrl+V) 하세요.`
      );

      // 네이버 블로그 글쓰기 페이지 열기
      window.open(NAVER_BLOG_WRITE_URL, "_blank");
    });
  };

  const handleMarkPosted = (noticeCode: string) => {
    const blogUrl = prompt("블로그 글 URL (선택, 없으면 빈칸):");
    markAsPosted(noticeCode, blogUrl || "");
    forceRefresh();
  };

  const handleUnmark = (noticeCode: string) => {
    if (confirm("작성 완료 표시를 해제할까요?")) {
      unmarkPosted(noticeCode);
      forceRefresh();
    }
  };

  const handleExport = () => {
    const data = exportPosted();
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "posted.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  const postedCount = getPostedCount();

  // 인증
  if (!authenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-xl border border-gray-200 p-8 w-80">
          <h1 className="text-lg font-bold mb-4">관리자 인증</h1>
          <input
            type="password"
            value={pwInput}
            onChange={(e) => setPwInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && pwInput === ADMIN_PW)
                setAuthenticated(true);
            }}
            placeholder="비밀번호"
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-3"
          />
          <button
            onClick={() => {
              if (pwInput === ADMIN_PW) setAuthenticated(true);
              else alert("비밀번호가 틀렸습니다.");
            }}
            className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-700"
          >
            확인
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">블로그 관리</h1>
          <p className="text-sm text-gray-400 mt-0.5">
            고시문 → 네이버 블로그 포스팅 관리
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-400">
            작성 {postedCount}건 / 전체 {records.length}건
          </span>
          <button
            onClick={handleExport}
            className="text-xs border border-gray-200 rounded-lg px-3 py-1.5 hover:bg-gray-50"
          >
            내보내기
          </button>
        </div>
      </div>

      {/* 필터 */}
      <div className="flex flex-wrap gap-3">
        <select
          value={showPosted}
          onChange={(e) =>
            setShowPosted(e.target.value as "all" | "unposted" | "posted")
          }
          className="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white"
        >
          <option value="unposted">미작성만</option>
          <option value="posted">작성완료만</option>
          <option value="all">전체</option>
        </select>
        <select
          value={grade}
          onChange={(e) => {
            setGrade(e.target.value);
            setCenterName("");
          }}
          className="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white"
        >
          <option value="">전체 등급</option>
          <option value="도심">도심</option>
          <option value="광역중심">광역중심</option>
          <option value="지역중심">지역중심</option>
          <option value="미매칭">미매칭</option>
        </select>
        {centerOptions.length > 0 && (
          <select
            value={centerName}
            onChange={(e) => setCenterName(e.target.value)}
            className="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white"
          >
            <option value="">전체 중심지</option>
            {centerOptions.map((c) => (
              <option key={c.name} value={c.name}>
                {c.name}
              </option>
            ))}
          </select>
        )}
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="키워드 검색"
          className="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white min-w-[200px]"
        />
        {(grade || centerName || keyword) && (
          <button
            onClick={() => {
              setGrade("");
              setCenterName("");
              setKeyword("");
            }}
            className="text-sm text-gray-400 hover:text-gray-600"
          >
            초기화
          </button>
        )}
      </div>

      {/* 결과 수 */}
      <p className="text-sm text-gray-400">{filtered.length}건</p>

      {/* 목록 */}
      <div className="space-y-2">
        {filtered.length === 0 && (
          <p className="text-center text-gray-300 py-12">
            조건에 맞는 고시문이 없습니다.
          </p>
        )}
        {filtered.map((r) => {
          const posted = isPosted(r.notice_code);
          return (
            <div
              key={r.notice_code}
              className={`bg-white rounded-xl border p-4 ${
                posted
                  ? "border-green-200 bg-green-50/30"
                  : "border-gray-200"
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-1.5 mb-1">
                    <span className="text-xs font-mono text-gray-400">
                      {r.notice_date}
                    </span>
                    {r.center_grade && (
                      <span
                        className="text-xs px-1.5 py-0.5 rounded text-white font-medium"
                        style={{
                          backgroundColor:
                            GRADE_COLORS[r.center_grade] || "#999",
                        }}
                      >
                        {r.center_grade}·{r.center_name}
                      </span>
                    )}
                    <span className="text-xs text-gray-400">
                      {r.organ_name}
                    </span>
                    {posted && (
                      <span className="text-xs px-1.5 py-0.5 rounded bg-green-100 text-green-700 font-medium">
                        작성완료
                      </span>
                    )}
                  </div>
                  <p className="text-sm font-medium">{r.title}</p>
                  {r.location && (
                    <p className="text-xs text-gray-400 mt-1">
                      📍 {r.location}
                    </p>
                  )}
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  {!posted ? (
                    <>
                      <button
                        onClick={() => handleWriteBlog(r)}
                        className="text-xs bg-blue-600 text-white rounded-lg px-3 py-1.5 hover:bg-blue-700 font-medium whitespace-nowrap"
                      >
                        블로그 쓰기
                      </button>
                      <button
                        onClick={() => handleMarkPosted(r.notice_code)}
                        className="text-xs border border-gray-200 rounded-lg px-3 py-1.5 hover:bg-gray-50 whitespace-nowrap"
                      >
                        작성완료
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={() => handleUnmark(r.notice_code)}
                      className="text-xs text-gray-400 hover:text-red-500 whitespace-nowrap"
                    >
                      해제
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
