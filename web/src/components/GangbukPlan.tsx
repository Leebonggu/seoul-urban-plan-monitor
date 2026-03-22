"use client";

/* ── 강남북 불균형 ── */
const GAP_DATA = [
  { label: "사업체 수", south: "24만", north: "8만", ratio: "2.7배" },
  { label: "자족기능", south: "21.2%", north: "7.6%", ratio: "~3배" },
  { label: "지하철역", south: "61개", north: "10개", ratio: "3.2배" },
  { label: "역당 인구", south: "2.1만", north: "5.4만", ratio: "2.6배" },
  { label: "도시고속도로", south: "147km", north: "99km", ratio: "1.5배" },
];

/* ── 교통 사업 ── */
const TRANSPORT = [
  {
    name: "강북횡단 지하고속도로",
    spec: "내부순환~북부간선 20.5km, 왕복 6차로",
    effect: "통행속도 34.5→67km/h",
    budget: "3.4조",
  },
  {
    name: "동부간선도로 지하화",
    spec: "월계IC~대치IC 15.4km, 왕복 4차로",
    effect: "동남~동북권 20분 단축, 지상부 공원화",
    budget: "공사 중",
  },
  {
    name: "강북횡단선(철도)",
    spec: "신규 도시철도 노선",
    effect: "동북~서북권 횡적 연결",
    budget: "2.6조",
  },
  {
    name: "동북선",
    spec: "왕십리역~상계역",
    effect: "2027년 개통 목표",
    budget: "-",
  },
  {
    name: "우이신설연장선",
    spec: "솔밭공원~방학역 3.93km, 3개역",
    effect: "2032년 개통 예정",
    budget: "-",
  },
  {
    name: "노후 지하철 환경개선",
    spec: "강북 20개역 대상",
    effect: "역사 환경 현대화",
    budget: "1.0조",
  },
];

/* ── 성장거점 10개소 ── */
const HUBS = [
  {
    num: 1,
    name: "창동·상계 S-DBC",
    area: "동북",
    detail:
      "서울디지털바이오시티. 하반기 산업단지 지정, 약 800개 일자리 기업 유치 목표. 창동차량기지·면허시험장 이전 부지 활용.",
    highlight: true,
  },
  {
    num: 2,
    name: "서울아레나",
    area: "동북",
    detail:
      "2만 8천석 K-POP 전용 공연장. 2027년 상반기 개관, 연간 270만+ 관람 수요.",
    highlight: false,
  },
  {
    num: 3,
    name: "DMC 랜드마크",
    area: "서북",
    detail: "데이터 기반 미래산업 및 미디어·엔터테인먼트 산업 지원 거점.",
    highlight: false,
  },
  {
    num: 4,
    name: "서부면허시험장 이전지",
    area: "서북",
    detail: "첨단산업 거점 공간으로 전환.",
    highlight: false,
  },
  {
    num: 5,
    name: "삼표레미콘 부지",
    area: "사전협상",
    detail:
      "79층 초고층 복합시설, 올 연말 착공 목표. 유니콘 창업허브 + 성수·서울숲·한강 연계.",
    highlight: false,
  },
  {
    num: 6,
    name: "동서울터미널",
    area: "사전협상",
    detail:
      "준공 40년 경과. 환승센터·업무·상업·문화 복합시설로 현대화, 강변북로 직결램프.",
    highlight: false,
  },
  {
    num: 7,
    name: "광운대역 물류부지",
    area: "사전협상",
    detail:
      "업무·상업·주거 대형 복합거점. HDC현대산업개발 본사 이전, 도서관·체육센터 등 생활SOC.",
    highlight: false,
  },
  {
    num: 8,
    name: "세운지구",
    area: "도심",
    detail: "약 13.6만㎡ 녹지 확보, 직·주·락 도시 모델 구현.",
    highlight: false,
  },
  {
    num: 9,
    name: "서울역 북부역세권",
    area: "도심",
    detail:
      "2029년 완성, 최대 39층 5개동. 2,000명+ 수용 MICE 시설 도입.",
    highlight: false,
  },
  {
    num: 10,
    name: "용산서울코어",
    area: "도심",
    detail: "용산정비창 국제업무지구. 비즈니스·첨단기술·삶·자연 융합 혁신거점.",
    highlight: false,
  },
];

/* ── 새 제도 ── */
const INSTITUTIONS = [
  {
    name: "성장거점형 복합개발사업",
    where: "도심·광역중심·환승역세권(500m 이내)",
    condition: "비주거 50% 이상",
    benefit: "일반상업지역 용적률 최대 1,300%까지 완화",
  },
  {
    name: "성장잠재권 활성화사업",
    where: "통일로·도봉로·동일로 등 폭 35m+ 간선도로변",
    condition: "평균 공시지가 60% 이하 자치구",
    benefit: "공공기여 비중 30%까지 인하",
  },
  {
    name: "강북전성시대기금(가칭)",
    where: "사전협상 대상지 전체",
    condition: "공공기여 현금 비중 30→70%로 확대",
    benefit: "공공부지 매각수입과 합산하여 강북 투자재원으로 활용",
  },
];

/* ── 인사이트: 2040 서울플랜 × 강북전성시대 2.0 ── */
const INSIGHTS = [
  {
    title: "상계·창동: 재건축과 신도시급 개발이 동시에",
    desc: "2040 서울플랜은 '상계·중계 노후 택지지구의 선제적 관리계획 수립'을 명시하고, 강북전성시대 2.0은 바로 그 옆에 S-DBC(서울디지털바이오시티)를 1번 성장거점으로 배치했다. 4호선 지상구간 지하화 검토, 동부간선도로 지하화, 동북선 개통(2027)이 겹치면서 상계 일대는 단순 아파트 재건축이 아니라 도시 구조 전체가 바뀌는 국면이다.",
  },
  {
    title: "용적률 1,300% — 강북에만 적용되는 파격적 규제 완화",
    desc: "성장거점형 복합개발사업은 광역중심·환승역세권에서 비주거 50% 이상이면 용적률을 1,300%까지 허용한다. 창동·상계는 광역중심이므로 이 제도의 직접 적용 대상이다. 2040 서울플랜의 'Beyond Zoning Seoul'(용도지역 유연화)이 강북전성시대 2.0에서 구체적 숫자로 현실화된 셈이다.",
  },
  {
    title: "16조의 구조: 돈이 어디서 나오는가",
    desc: "서울시 10조 + 국비 2.4조 + 민자 3.6조. 핵심은 사전협상제도의 공공기여 현금 비중을 30%에서 70%로 올리고, 여기서 나온 현금 + 공공부지 매각수입으로 '강북전성시대기금'을 만든다는 것. 삼표·동서울터미널·광운대 3곳의 사전협상에서만 대체비자체 5.2조가 예상된다.",
  },
  {
    title: "교통이 먼저 — 강북 전체를 관통하는 도로+철도 동시 투자",
    desc: "강북횡단 지하고속도로(20.5km)와 동부간선도로 지하화(15.4km)가 완성되면 강북 도로 체계가 근본적으로 바뀐다. 여기에 강북횡단선, 동북선, 우이신설연장선 등 철도까지 동시 투입. 2040 서울플랜이 '중심지 체계와 광역교통축의 연계'를 큰 그림으로 제시했다면, 강북전성시대 2.0은 노선·구간·예산까지 확정한 실행 계획이다.",
  },
  {
    title: "동북권 산업축의 완성: 홍릉→청량리→광운대→창동·상계",
    desc: "2040 서울플랜의 '청년첨단 혁신축'(바이오·의료·ICT)이 강북전성시대 2.0에서 S-DBC + 광운대역 물류부지 + 서울아레나로 구체화됐다. 기존 동북권의 가장 큰 약점이었던 '일자리 자족성 부재'(베드타운)를 산업단지 지정, 800개 기업 유치, K-POP 문화산업으로 돌파하려는 전략이다.",
  },
];

export default function GangbukPlan() {
  return (
    <div className="space-y-10">
      {/* 헤더 */}
      <section>
        <h2 className="text-2xl font-bold">다시, 강북전성시대 2.0</h2>
        <p className="text-sm text-gray-400 mt-1">
          서울시 균형발전기획관 · 2026.03 발표 · 총 16조 투자
        </p>
      </section>

      {/* 한 줄 요약 */}
      <section className="bg-gray-900 text-white rounded-xl p-6">
        <p className="text-sm leading-relaxed">
          2024년 강북전성시대 1.0에{" "}
          <span className="text-emerald-400 font-medium">
            교통 인프라 8개 + 산업·일자리 4개
          </span>{" "}
          사업을 추가한 확장판. 강북횡단 지하고속도로(20.5km), 동부간선도로
          지하화(15.4km), S-DBC 산업단지 지정, 용적률 1,300% 파격 완화 등{" "}
          <span className="text-emerald-400 font-medium">
            총 16조 재원
          </span>
          을 투입하여 강남북 불균형을 해소하겠다는 계획.
        </p>
      </section>

      {/* 강남북 격차 */}
      <section>
        <h3 className="text-lg font-bold mb-4">강남북 격차 현황</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-2 pr-4 text-xs text-gray-400 font-medium">
                  항목
                </th>
                <th className="text-right py-2 px-4 text-xs text-gray-400 font-medium">
                  강남
                </th>
                <th className="text-right py-2 px-4 text-xs text-gray-400 font-medium">
                  강북
                </th>
                <th className="text-right py-2 pl-4 text-xs text-gray-400 font-medium">
                  차이
                </th>
              </tr>
            </thead>
            <tbody>
              {GAP_DATA.map((row) => (
                <tr key={row.label} className="border-b border-gray-100">
                  <td className="py-2.5 pr-4 text-sm">{row.label}</td>
                  <td className="py-2.5 px-4 text-right font-mono">
                    {row.south}
                  </td>
                  <td className="py-2.5 px-4 text-right font-mono">
                    {row.north}
                  </td>
                  <td className="py-2.5 pl-4 text-right text-red-500 font-medium">
                    {row.ratio}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          2024년 기준, 서울시 총 사업체 117만 6,066개
        </p>
      </section>

      {/* 재원 */}
      <section>
        <h3 className="text-lg font-bold mb-4">재원 구조 — 총 16조</h3>
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="bg-blue-50 rounded-xl p-4 text-center">
            <p className="text-2xl font-bold text-blue-700">10조</p>
            <p className="text-xs text-gray-500 mt-1">서울시</p>
          </div>
          <div className="bg-gray-50 rounded-xl p-4 text-center">
            <p className="text-2xl font-bold text-gray-700">2.4조</p>
            <p className="text-xs text-gray-500 mt-1">국비</p>
          </div>
          <div className="bg-emerald-50 rounded-xl p-4 text-center">
            <p className="text-2xl font-bold text-emerald-700">3.6조</p>
            <p className="text-xs text-gray-500 mt-1">민자</p>
          </div>
        </div>
        <p className="text-xs text-gray-500 leading-relaxed">
          사전협상 3곳(삼표·동서울터미널·광운대)에서 대체비자체{" "}
          <strong>5.2조</strong> 예상. 공공기여 현금 비중을 30→70%로 확대하여
          '강북전성시대기금(가칭)'을 신설, 도로·철도 사업에 재투자하는 구조.
        </p>
      </section>

      {/* 교통 사업 */}
      <section>
        <h3 className="text-lg font-bold mb-4">핵심 교통 사업</h3>
        <div className="space-y-2">
          {TRANSPORT.map((t) => (
            <div
              key={t.name}
              className="border border-gray-200 rounded-lg p-4 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-6"
            >
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-bold">{t.name}</h4>
                <p className="text-xs text-gray-500 mt-0.5">{t.spec}</p>
              </div>
              <p className="text-xs text-gray-600 sm:text-right shrink-0">
                {t.effect}
              </p>
              {t.budget !== "-" && (
                <span className="text-xs font-mono text-blue-600 font-medium shrink-0">
                  {t.budget}
                </span>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* 성장거점 10개소 */}
      <section>
        <h3 className="text-lg font-bold mb-4">산업·일자리 성장거점 10개소</h3>
        <div className="space-y-2">
          {HUBS.map((hub) => (
            <div
              key={hub.num}
              className={`border rounded-lg p-4 ${
                hub.highlight
                  ? "border-emerald-400 bg-emerald-50/40"
                  : "border-gray-200"
              }`}
            >
              <div className="flex items-start gap-3">
                <span className="text-xs font-mono text-gray-400 mt-0.5 shrink-0">
                  {String(hub.num).padStart(2, "0")}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h4 className="text-sm font-bold">{hub.name}</h4>
                    <span className="text-xs text-gray-400">
                      {hub.area}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mt-1 leading-relaxed">
                    {hub.detail}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 새 제도 */}
      <section>
        <h3 className="text-lg font-bold mb-4">새로운 제도적 도구</h3>
        <div className="space-y-3">
          {INSTITUTIONS.map((inst) => (
            <div
              key={inst.name}
              className="border border-gray-200 rounded-lg p-4"
            >
              <h4 className="text-sm font-bold mb-2">{inst.name}</h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
                <div>
                  <span className="text-gray-400">대상</span>
                  <p className="text-gray-700 mt-0.5">{inst.where}</p>
                </div>
                <div>
                  <span className="text-gray-400">조건</span>
                  <p className="text-gray-700 mt-0.5">{inst.condition}</p>
                </div>
                <div>
                  <span className="text-gray-400">혜택</span>
                  <p className="text-emerald-700 font-medium mt-0.5">
                    {inst.benefit}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 인사이트 */}
      <section>
        <div className="border-t-2 border-gray-900 pt-6">
          <h3 className="text-lg font-bold mb-1">
            인사이트 — 2040 서울플랜 × 강북전성시대 2.0
          </h3>
          <p className="text-xs text-gray-400 mb-6">
            두 정책 원문을 교차하여 도출한 분석입니다. 서울시 공식 해석과 다를 수
            있습니다.
          </p>
          <div className="space-y-4">
            {INSIGHTS.map((insight, i) => (
              <div key={i} className="border border-gray-200 rounded-xl p-5">
                <h4 className="text-sm font-bold mb-2">
                  <span className="text-gray-400 mr-2">{i + 1}.</span>
                  {insight.title}
                </h4>
                <p className="text-xs text-gray-600 leading-relaxed">
                  {insight.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 출처 */}
      <section className="border-t border-gray-200 pt-4">
        <p className="text-xs text-gray-400 leading-relaxed">
          <span className="font-medium text-gray-500">출처:</span>{" "}
          ① 서울특별시 균형발전기획관, 「다시, 강북전성시대 2.0」, 2026.03 —{" "}
          <a
            href="https://uri.seoul.go.kr/web/contents/24.do?mid=1346"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            서울균형발전포털
          </a>
          {" · "}
          <a
            href="https://mediahub.seoul.go.kr/archives/2017184"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            보도자료
          </a>{" "}
          ② 서울특별시, 「2040 서울도시기본계획」, 2023.02 —{" "}
          <a
            href="https://urban.seoul.go.kr/view/html/PMNU3030000001"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            서울도시공간포털
          </a>
        </p>
      </section>
    </div>
  );
}
