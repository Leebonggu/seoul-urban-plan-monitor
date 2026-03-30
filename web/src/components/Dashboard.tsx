"use client";

import { useState, useMemo, useEffect } from "react";
import dynamic from "next/dynamic";
import { GosiRecord, Center } from "@/lib/types";
import { CENTERS, GRADE_COLORS } from "@/lib/centers";
import MetricCards from "./MetricCards";
import GosiList from "./GosiList";
import GosiTable from "./GosiTable";
import { MonthlyChart, GradeChart, CenterRanking } from "./Charts";
import AdBanner from "./AdBanner";

const CenterMap = dynamic(() => import("./CenterMap"), { ssr: false });

interface Props {
  records: GosiRecord[];
}

type Tab = "list" | "chart" | "center";

export default function Dashboard({ records }: Props) {
  const [mounted, setMounted] = useState(false);
  const [grade, setGrade] = useState("");
  const [centerName, setCenterName] = useState("");
  const [keyword, setKeyword] = useState("");
  const [category, setCategory] = useState("");
  const [tab, setTab] = useState<Tab>("list");

  useEffect(() => setMounted(true), []);

  // 선택된 등급에 해당하는 중심지 목록
  const centerOptions = useMemo(() => {
    if (!grade || grade === "미매칭") return [];
    return CENTERS.filter((c) => c.grade === grade);
  }, [grade]);

  const filtered = useMemo(() => {
    let result = records;
    if (category) {
      result = result.filter((r) => (r.category || "결정고시") === category);
    }
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
    return result;
  }, [records, grade, centerName, keyword, category]);

  const centers: Center[] = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const r of filtered) {
      if (r.center_name) {
        counts[r.center_name] = (counts[r.center_name] || 0) + 1;
      }
    }
    return CENTERS.map((c) => ({
      name: c.name,
      grade: c.grade,
      lat: c.lat,
      lng: c.lng,
      count: counts[c.name] || 0,
    }));
  }, [filtered]);

  const centerMatched = filtered.filter((r) => r.center_grade).length;
  const latestDate = filtered.length > 0 ? filtered[0].notice_date : "-";
  const oldestDate = filtered.length > 0 ? filtered[filtered.length - 1].notice_date : "-";
  const dailyAvg = filtered.length / 90;

  const tabs: { key: Tab; label: string }[] = [
    { key: "list", label: "전체 목록" },
    { key: "chart", label: "추이/분석" },
    { key: "center", label: "중심지 상세" },
  ];

  if (!mounted) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-6 min-h-[80vh] flex flex-col items-center justify-center">
        <div className="flex items-end gap-1.5 mb-6 h-16">
          {[
            { h: "h-8", delay: "0s" },
            { h: "h-12", delay: "0.15s" },
            { h: "h-16", delay: "0.3s" },
            { h: "h-10", delay: "0.45s" },
            { h: "h-14", delay: "0.6s" },
          ].map((bar, i) => (
            <div
              key={i}
              className={`w-3 ${bar.h} rounded-t bg-blue-500`}
              style={{
                animation: "loadingPulse 1.2s ease-in-out infinite",
                animationDelay: bar.delay,
              }}
            />
          ))}
        </div>
        <p className="text-sm font-medium text-gray-500 animate-pulse">
          서울 도시계획 데이터를 불러오는 중
        </p>
        <div className="flex gap-1 mt-2">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="w-1.5 h-1.5 rounded-full bg-blue-400"
              style={{
                animation: "dotBounce 1.4s ease-in-out infinite",
                animationDelay: `${i * 0.2}s`,
              }}
            />
          ))}
        </div>
        <style jsx>{`
          @keyframes loadingPulse {
            0%, 100% { opacity: 0.3; transform: scaleY(0.6); }
            50% { opacity: 1; transform: scaleY(1); }
          }
          @keyframes dotBounce {
            0%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-6px); }
          }
        `}</style>
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
        {(grade || centerName || keyword || category) && (
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
        total={filtered.length}
        centerMatched={centerMatched}
        latestDate={latestDate}
        oldestDate={oldestDate}
        dailyAvg={dailyAvg}
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
            <GosiList records={filtered} maxItems={15} />
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
          {tab === "list" && <GosiTable records={filtered} />}
          {tab === "chart" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <MonthlyChart records={filtered} />
              <GradeChart records={filtered} />
            </div>
          )}
          {tab === "center" && <CenterRanking records={filtered} />}
        </div>
      </div>

      <AdBanner slot="SLOT_DASHBOARD" className="mt-6" />
    </div>
  );
}
