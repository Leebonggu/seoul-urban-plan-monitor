import { GosiRecord } from "./types";

export function generateBlogContent(record: GosiRecord): {
  title: string;
  body: string;
} {
  // SEO 최적화 제목: [지역구] 키워드 결정고시 (날짜) — 상세
  const location = record.location?.split(" ")[0] || record.organ_name || "서울";
  const titleText =
    record.title.length > 40
      ? record.title.substring(0, 40) + "..."
      : record.title;
  const title = `${location} ${record.notice_type || "도시계획"} 결정고시 (${record.notice_date}) — ${titleText}`;

  const centerInfo =
    record.center_grade && record.center_name
      ? `\n🏙️ 2040 서울플랜 중심지: ${record.center_grade} - ${record.center_name}\n`
      : "";

  const body = `📋 서울시 도시계획 결정고시 안내

━━━━━━━━━━━━━━━━━━━━

📌 고시번호: ${record.organ_name} 제${record.notice_no}호
📅 고시일자: ${record.notice_date}
🏢 고시기관: ${record.organ_name}
📍 위치: ${record.location || "정보 없음"}
📝 고시유형: ${record.notice_type || "결정"}
${centerInfo}
━━━━━━━━━━━━━━━━━━━━

📄 고시 내용

${record.content || "상세 내용은 원문을 확인해주세요."}

━━━━━━━━━━━━━━━━━━━━

🔗 관련 링크
- 상세 페이지: ${record.page_url}
${record.doc_url ? `- 원문 다운로드: ${record.doc_url}` : ""}

━━━━━━━━━━━━━━━━━━━━
출처: 서울도시공간포털 (urban.seoul.go.kr)

---
더 많은 서울시 결정고시를 한눈에 보려면:
서울 결정고시 모니터: https://seoul-urban-plan-monitor.2lee.kr
`;

  return { title, body };
}
