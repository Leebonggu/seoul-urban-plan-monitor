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
import { GosiRecord } from "@/lib/types";
import { GRADE_COLORS } from "@/lib/centers";

interface Props {
  records: GosiRecord[];
}

export function MonthlyChart({ records }: Props) {
  const byMonth: Record<string, number> = {};
  for (const r of records) {
    const month = r.notice_date.slice(0, 7);
    byMonth[month] = (byMonth[month] || 0) + 1;
  }
  const data = Object.entries(byMonth)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([month, count]) => ({ month, count }));

  return (
    <div>
      <h3 className="text-sm font-medium text-gray-500 mb-2">월별 추이</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <XAxis dataKey="month" tick={{ fontSize: 11 }} angle={-45} textAnchor="end" height={60} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip />
          <Bar dataKey="count" name="건수" fill="#3b82f6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function GradeChart({ records }: Props) {
  const counts: Record<string, number> = {};
  for (const r of records) {
    const grade = r.center_grade || "미매칭";
    counts[grade] = (counts[grade] || 0) + 1;
  }
  const data = Object.entries(counts).map(([name, value]) => ({ name, value }));

  return (
    <div>
      <h3 className="text-sm font-medium text-gray-500 mb-2">
        중심지 등급 분포
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={({ name, value }) => `${name} ${value}`}
          >
            {data.map((entry) => (
              <Cell
                key={entry.name}
                fill={
                  GRADE_COLORS[entry.name] || "#d1d5db"
                }
              />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export function CenterRanking({ records }: Props) {
  const counts: Record<string, number> = {};
  for (const r of records) {
    if (r.center_name) {
      counts[r.center_name] = (counts[r.center_name] || 0) + 1;
    }
  }
  const data = Object.entries(counts)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 15)
    .map(([name, count]) => ({ name, count }));

  return (
    <div>
      <h3 className="text-sm font-medium text-gray-500 mb-2">
        중심지별 TOP 15
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data} layout="vertical">
          <XAxis type="number" tick={{ fontSize: 11 }} />
          <YAxis dataKey="name" type="category" tick={{ fontSize: 11 }} width={120} />
          <Tooltip />
          <Bar dataKey="count" name="건수" fill="#f59e0b" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
