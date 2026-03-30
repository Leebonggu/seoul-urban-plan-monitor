"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { GRADE_COLORS } from "@/lib/centers";

interface MonthlyProps {
  aggregatedData: { month: string; count: number }[];
}

export function MonthlyChart({ aggregatedData }: MonthlyProps) {
  return (
    <div>
      <h3 className="text-sm font-medium text-gray-500 mb-2">월별 추이</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={aggregatedData}>
          <XAxis dataKey="month" tick={{ fontSize: 11 }} angle={-45} textAnchor="end" height={60} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip />
          <Bar dataKey="count" name="건수" fill="#3b82f6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

interface GradeProps {
  aggregatedData: { name: string; value: number }[];
}

export function GradeChart({ aggregatedData }: GradeProps) {
  return (
    <div>
      <h3 className="text-sm font-medium text-gray-500 mb-2">
        중심지 등급 분포
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={aggregatedData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={({ name, value }) => `${name} ${value}`}
          >
            {aggregatedData.map((entry) => (
              <Cell
                key={entry.name}
                fill={GRADE_COLORS[entry.name] || "#d1d5db"}
              />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

interface CenterRankingProps {
  aggregatedData: { name: string; count: number; grade: string }[];
}

export function CenterRanking({ aggregatedData }: CenterRankingProps) {
  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-500">
          중심지별 TOP 15
        </h3>
        <div className="flex gap-3 text-xs text-gray-400">
          <span><span style={{ color: GRADE_COLORS["도심"] }}>●</span> 도심</span>
          <span><span style={{ color: GRADE_COLORS["광역중심"] }}>●</span> 광역중심</span>
          <span><span style={{ color: GRADE_COLORS["지역중심"] }}>●</span> 지역중심</span>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={aggregatedData} layout="vertical">
          <XAxis type="number" tick={{ fontSize: 11 }} />
          <YAxis dataKey="name" type="category" tick={{ fontSize: 11 }} width={120} />
          <Tooltip />
          <Bar dataKey="count" name="건수" radius={[0, 4, 4, 0]}>
            {aggregatedData.map((entry) => (
              <Cell
                key={entry.name}
                fill={GRADE_COLORS[entry.grade] || "#d1d5db"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
