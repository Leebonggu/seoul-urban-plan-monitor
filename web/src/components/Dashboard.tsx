"use client";

import { useState, useMemo, useEffect, useCallback } from "react";
import dynamic from "next/dynamic";
import { GosiRecord, Center, AggregatedData } from "@/lib/types";
import { CENTERS, GRADE_COLORS } from "@/lib/centers";
import MetricCards from "./MetricCards";
import GosiList from "./GosiList";
import { MonthlyChart, GradeChart, CenterRanking } from "./Charts";
import AdBanner from "./AdBanner";

const CenterMap = dynamic(() => import("./CenterMap"), { ssr: false });

type LightRecord = Omit<GosiRecord, "content">;

interface Props {
  initialRecords: LightRecord[];
  initialTotal: number;
  aggregated: AggregatedData;
}

type Tab = "list" | "chart" | "center";

const PAGE_SIZE = 30;

export default function Dashboard({
  initialRecords,
  initialTotal,
  aggregated: initialAggregated,
}: Props) {
  const [mounted, setMounted] = useState(false);
  const [grade, setGrade] = useState("");
  const [centerName, setCenterName] = useState("");
  const [keyword, setKeyword] = useState("");
  const [category, setCategory] = useState("");
  const [tab, setTab] = useState<Tab>("list");

  // 필터/페이지네이션이 적용된 목록 데이터
  const [records, setRecords] = useState<LightRecord[]>(initialRecords);
  const [totalCount, setTotalCount] = useState(initialTotal);
  const [aggregated, setAggregated] = useState(initialAggregated);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(false);

  const isFiltered = !!(grade || centerName || keyword || category);

  useEffect(() => setMounted(true), []);

  const fetchData = useCallback(
    async (p: number, resetAgg = false) => {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (category) params.set("category", category);
        if (grade) params.set("grade", grade);
        if (centerName) params.set("centerName", centerName);
        if (keyword) params.set("keyword", keyword);
        params.set("page", String(p));
        params.set("pageSize", String(PAGE_SIZE));

        const res = await fetch(`/api/gosi?${params}`);
        const data = await res.json();

        setRecords(data.records);
        setTotalCount(data.total);
        if (resetAgg) {
          setAggregated(data.aggregated);
        }
        setPage(p);
      } finally {
        setLoading(false);
      }
    },
    [category, grade, centerName, keyword]
  );

  // 필터 변경 시 첫 페이지부터 다시 fetch
  useEffect(() => {
    if (!mounted) return;
    fetchData(0, true);
  }, [category, grade, centerName, mounted]); // eslint-disable-line react-hooks/exhaustive-deps

  // 키워드 검색은 디바운스
  const [debouncedKeyword, setDebouncedKeyword] = useState(keyword);
  useEffect(() => {
    const t = setTimeout(() => setDebouncedKeyword(keyword), 300);
    return () => clearTimeout(t);
  }, [keyword]);

  useEffect(() => {
    if (!mounted) return;
    fetchData(0, true);
  }, [debouncedKeyword]); // eslint-disable-line react-hooks/exhaustive-deps

  // 선택된 등급에 해당하는 중심지 목록
  const centerOptions = useMemo(() => {
    if (!grade || grade === "미매칭") return [];
    return CENTERS.filter((c) => c.grade === grade);
  }, [grade]);

  // 지도용 중심지 데이터 (집계 기반)
  const centers: Center[] = useMemo(() => {
    return CENTERS.map((c) => ({
      name: c.name,
      grade: c.grade,
      lat: c.lat,
      lng: c.lng,
      count: aggregated.centerCounts[c.name] || 0,
    }));
  }, [aggregated]);

  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  const tabs: { key: Tab; label: string }[] = [
    { key: "list", label: "전체 목록" },
    { key: "chart", label: "추이/분석" },
    { key: "center", label: "중심지 상세" },
  ];

  if (!mounted) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        <div>
          <div className="h-8 w-56 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-80 bg-gray-100 rounded animate-pulse mt-1.5" />
        </div>
        <div className="flex flex-wrap gap-3">
          <div className="h-9 w-28 bg-gray-100 rounded-lg animate-pulse" />
          <div className="h-9 w-24 bg-gray-100 rounded-lg animate-pulse" />
          <div className="h-9 w-64 bg-gray-100 rounded-lg animate-pulse" />
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="bg-white rounded-xl border border-gray-200 p-4 h-24 animate-pulse" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl border border-gray-200 p-4 h-[480px] animate-pulse" />
          <div className="bg-white rounded-xl border border-gray-200 p-4 h-[480px] animate-pulse" />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      {/* 헤더 */}
      <div>
        <h1 className="text-2xl font-bold">서울 결정고시 모니터</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          2040 서울플랜 중심지체계 기반 분석 · urban.seoul.go.kr
        </p>
      </div>

      {/* 필터 */}
      <div className="flex flex-wrap gap-3">
        <label className="sr-only" htmlFor="filter-category">범주 필터</label>
        <select
          id="filter-category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white"
        >
          <option value="">전체 범주</option>
          <option value="결정고시">결정고시</option>
          <option value="지구단위계획">지구단위계획</option>
          <option value="도시계획시설">도시계획시설</option>
          <option value="정비사업구역계">정비사업구역계</option>
        </select>
        <label className="sr-only" htmlFor="filter-grade">등급 필터</label>
        <select
          id="filter-grade"
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
          <>
            <label className="sr-only" htmlFor="filter-center">중심지 필터</label>
            <select
              id="filter-center"
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
          </>
        )}
        <label className="sr-only" htmlFor="filter-keyword">키워드 검색</label>
        <input
          id="filter-keyword"
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="키워드 검색 (재개발, 용적률...)"
          className="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white min-w-[250px]"
        />
        {isFiltered && (
          <button
            onClick={() => {
              setGrade("");
              setCenterName("");
              setKeyword("");
              setCategory("");
            }}
            className="text-sm text-gray-400 hover:text-gray-600 px-2"
          >
            초기화
          </button>
        )}
      </div>

      {/* 지표 카드 */}
      <MetricCards
        total={aggregated.totalCount}
        centerMatched={aggregated.centerMatchedCount}
        latestDate={aggregated.latestDate}
        oldestDate={aggregated.oldestDate}
        dailyAvg={aggregated.totalCount / 90}
      />

      {/* 메인: 지도 + 최신 목록 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-semibold">중심지 현황</h2>
            <div className="flex gap-3 text-xs text-gray-400">
              <span>
                <span style={{ color: GRADE_COLORS["도심"] }}>●</span> 도심
              </span>
              <span>
                <span style={{ color: GRADE_COLORS["광역중심"] }}>●</span>{" "}
                광역중심
              </span>
              <span>
                <span style={{ color: GRADE_COLORS["지역중심"] }}>●</span>{" "}
                지역중심
              </span>
            </div>
          </div>
          <div className="h-[420px]">
            <CenterMap centers={centers} />
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <h2 className="font-semibold mb-3">최신 고시문</h2>
          <div className="overflow-y-auto max-h-[440px]">
            <GosiList records={records as GosiRecord[]} maxItems={15} />
          </div>
        </div>
      </div>

      {/* 하단 탭 */}
      <div className="bg-white rounded-xl border border-gray-200">
        <div className="flex border-b border-gray-200">
          {tabs.map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`px-5 py-3 text-sm font-medium transition-colors ${
                tab === t.key
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        <div className="p-4">
          {tab === "list" && (
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
                  <tbody className={loading ? "opacity-50" : ""}>
                    {records.map((r) => (
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
                          <a
                            href={`/gosi/${r.notice_code}`}
                            className="hover:text-blue-600 transition-colors"
                          >
                            {r.title}
                          </a>
                        </td>
                        <td className="py-2 px-2 whitespace-nowrap">
                          {r.page_url && (
                            <a
                              href={r.page_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs text-blue-600 hover:underline mr-2"
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
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="flex items-center justify-between mt-4 text-sm text-gray-500">
                <span>
                  총 {totalCount.toLocaleString()}건 중{" "}
                  {page * PAGE_SIZE + 1}-
                  {Math.min((page + 1) * PAGE_SIZE, totalCount)}
                </span>
                <div className="flex gap-2">
                  <button
                    onClick={() => fetchData(Math.max(0, page - 1))}
                    disabled={page === 0 || loading}
                    className="px-3 py-1 rounded border border-gray-200 disabled:opacity-30 hover:bg-gray-100"
                  >
                    이전
                  </button>
                  <button
                    onClick={() =>
                      fetchData(Math.min(totalPages - 1, page + 1))
                    }
                    disabled={page >= totalPages - 1 || loading}
                    className="px-3 py-1 rounded border border-gray-200 disabled:opacity-30 hover:bg-gray-100"
                  >
                    다음
                  </button>
                </div>
              </div>
            </div>
          )}
          {tab === "chart" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <MonthlyChart aggregatedData={aggregated.monthlyData} />
              <GradeChart aggregatedData={aggregated.gradeData} />
            </div>
          )}
          {tab === "center" && (
            <CenterRanking aggregatedData={aggregated.centerRanking} />
          )}
        </div>
      </div>

      <AdBanner slot="SLOT_DASHBOARD" className="mt-6" />
    </div>
  );
}
