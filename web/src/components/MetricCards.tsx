"use client";

interface Props {
  total: number;
  centerMatched: number;
  latestDate: string;
  oldestDate: string;
  dailyAvg: number;
}

export default function MetricCards({
  total,
  centerMatched,
  latestDate,
  oldestDate,
  dailyAvg,
}: Props) {
  const cards = [
    { label: "총 고시문", value: `${total.toLocaleString()}건` },
    { label: "중심지 매칭", value: `${centerMatched.toLocaleString()}건` },
    { label: "최신 고시일", value: latestDate },
    { label: "데이터 시작", value: oldestDate },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="bg-white rounded-xl border border-gray-200 p-4"
        >
          <p className="text-sm text-gray-500">{card.label}</p>
          <p className="text-2xl font-bold mt-1">{card.value}</p>
        </div>
      ))}
    </div>
  );
}
