import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { loadAllNoticeCodes, loadRecordByCode } from "@/lib/data";
import { GRADE_COLORS } from "@/lib/centers";
import AdBanner from "@/components/AdBanner";

export const dynamic = "force-static";

interface Props {
  params: Promise<{ notice_code: string }>;
}

export async function generateStaticParams() {
  const codes = loadAllNoticeCodes();
  return codes.map((code) => ({ notice_code: code }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { notice_code } = await params;
  const record = loadRecordByCode(notice_code);
  if (!record) return {};

  const location = record.location || record.site_name || "";
  const titleText = record.title.length > 50
    ? record.title.slice(0, 50) + "..."
    : record.title;
  const title = location
    ? `${location} ${titleText}`
    : titleText;

  const description =
    record.content.slice(0, 150).replace(/\n/g, " ") +
    "... 서울시 도시계획 결정고시 원문";

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      type: "article",
    },
  };
}

export default async function GosiDetailPage({ params }: Props) {
  const { notice_code } = await params;
  const record = loadRecordByCode(notice_code);
  if (!record) notFound();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: record.title,
    datePublished: record.notice_date,
    author: {
      "@type": "Organization",
      name: record.organ_name,
    },
    publisher: {
      "@type": "Organization",
      name: "서울 결정고시 모니터",
    },
    description: record.content.slice(0, 150).replace(/\n/g, " "),
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Header */}
      <div className="mb-6">
        <div className="flex flex-wrap items-center gap-2 mb-2">
          {record.center_grade && (
            <span
              className="text-xs px-2 py-1 rounded font-medium text-white"
              style={{
                backgroundColor: GRADE_COLORS[record.center_grade] || "#999",
              }}
            >
              {record.center_grade}·{record.center_name}
            </span>
          )}
          {record.category && record.category !== "결정고시" && (
            <span className="text-xs px-2 py-1 rounded bg-purple-100 text-purple-700 font-medium">
              {record.category}
            </span>
          )}
          {record.location && (
            <span className="text-sm text-gray-500">{record.location}</span>
          )}
        </div>
        <h1 className="text-xl font-bold leading-tight">{record.title}</h1>
      </div>

      {/* Metadata Table */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <table className="w-full text-sm">
          <tbody>
            <tr className="border-b border-gray-200">
              <td className="py-2 pr-4 text-gray-500 font-medium w-24">고시번호</td>
              <td className="py-2">{record.notice_no}</td>
            </tr>
            <tr className="border-b border-gray-200">
              <td className="py-2 pr-4 text-gray-500 font-medium">고시일</td>
              <td className="py-2">{record.notice_date}</td>
            </tr>
            <tr className="border-b border-gray-200">
              <td className="py-2 pr-4 text-gray-500 font-medium">고시기관</td>
              <td className="py-2">{record.organ_name}</td>
            </tr>
            {record.location && (
              <tr className="border-b border-gray-200">
                <td className="py-2 pr-4 text-gray-500 font-medium">위치</td>
                <td className="py-2">{record.location}</td>
              </tr>
            )}
            <tr>
              <td className="py-2 pr-4 text-gray-500 font-medium">유형</td>
              <td className="py-2">{record.notice_type}</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Content */}
      <div className="prose prose-sm max-w-none mb-6">
        <h2 className="text-lg font-bold mb-3">고시 원문</h2>
        <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
          {record.content}
        </div>
      </div>

      {/* Links */}
      <div className="flex flex-wrap gap-3 mb-8">
        {record.doc_url && (
          <a
            href={record.doc_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm px-4 py-2 rounded-lg bg-blue-50 text-blue-700 hover:bg-blue-100 transition-colors"
          >
            원문 PDF
          </a>
        )}
        {record.page_url && (
          <a
            href={record.page_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm px-4 py-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
          >
            출처 페이지
          </a>
        )}
      </div>

      {/* Back link */}
      <div className="border-t border-gray-200 pt-4 mb-6">
        <Link
          href="/"
          className="text-sm text-blue-600 hover:underline"
        >
          &larr; 전체 고시문 목록
        </Link>
      </div>

      <AdBanner slot="SLOT_GOSI_DETAIL" className="mt-4" />
    </div>
  );
}
