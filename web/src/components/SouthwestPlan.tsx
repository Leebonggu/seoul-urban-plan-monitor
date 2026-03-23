"use client";

import AdBanner from "./AdBanner";

/* ── 재원 구조 ── */
const BUDGET = [
  { label: "시비", amount: "4.7조", color: "bg-blue-50", textColor: "text-blue-700" },
  { label: "민간", amount: "1.8조", color: "bg-emerald-50", textColor: "text-emerald-700" },
  { label: "국비", amount: "0.8조", color: "bg-gray-50", textColor: "text-gray-700" },
];

/* ── 대상 자치구 ── */
const DISTRICTS = ["양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구"];

/* ── 교통 사업 ── */
const TRANSPORT_RAIL = [
  {
    name: "강북횡단선",
    spec: "신규 도시철도 노선",
    effect: "서남~서북~동북권 횡적 연결",
  },
  {
    name: "목동선",
    spec: "신규 도시철도 노선",
    effect: "목동~여의도 연결, 서남권 교통 해소",
  },
  {
    name: "서부선",
    spec: "신규 도시철도 노선",
    effect: "은평~서대문~마포 연결",
  },
  {
    name: "난곡선",
    spec: "신규 도시철도 노선",
    effect: "난곡 지역 교통 사각지대 해소",
  },
];

const TRANSPORT_ROAD = [
  {
    name: "남부순환 지하도로",
    spec: "개화동~신림동 15km 신설",
    effect: "강남↔강서 70분→40분 단축",
  },
  {
    name: "국회 지하차도",
    spec: "신월IC~국회의사당 교차로 7.6km (연장 4.1km)",
    effect: "서남권 동서축 관통",
  },
  {
    name: "서부간선도로 확장",
    spec: "4차로 → 5차로 확장",
    effect: "서남권 남북축 용량 확대",
  },
  {
    name: "신림봉천터널",
    spec: "강남순환로 연결 터널 신설",
    effect: "남부순환로 직결",
  },
];

/* ── 산업 거점 ── */
const INDUSTRY_HUBS = [
  {
    num: 1,
    name: "마곡산단",
    area: "강서",
    detail:
      "복합용지 전환, 문화·편의시설 유치, 피지컬 AI 산업 거점으로 고도화. R&D 클러스터 확대.",
    highlight: true,
  },
  {
    num: 2,
    name: "G밸리 (구로디지털단지)",
    area: "구로·금천",
    detail:
      "교학사·마리오아울렛 특별계획구역 복합개발. 도심형 가로숲 조성. 혁신 플랫폼으로 재편.",
    highlight: true,
  },
  {
    num: 3,
    name: "온수산단",
    area: "구로",
    detail: "지구단위계획 재정비, 기반·지원시설 확충. 첨단제조업 중심 공간으로 재구조화.",
    highlight: false,
  },
  {
    num: 4,
    name: "서부트럭터미널 → 도시첨단물류단지",
    area: "신정동",
    detail: "10.4만㎡ 규모 도시첨단물류단지 조성. 1.9조원 투입.",
    highlight: false,
  },
  {
    num: 5,
    name: "금천 공군부대 → 컴팩트시티",
    area: "금천",
    detail: "용적률·용도 규제 완화. 직주근접형 컴팩트시티로 전환.",
    highlight: false,
  },
  {
    num: 6,
    name: "관악S밸리",
    area: "관악",
    detail: "낙성대 일대 벤처창업 거점 조성.",
    highlight: false,
  },
  {
    num: 7,
    name: "기술인재사관학교 서남캠퍼스",
    area: "온수역",
    detail: "온수역 럭비구장 부지에 기술인재 양성 캠퍼스 조성.",
    highlight: false,
  },
  {
    num: 8,
    name: "서울 테크 스페이스",
    area: "고척동",
    detail: "첨단 IT 제조·검증·데이터분석 기능 거점.",
    highlight: false,
  },
];

/* ── 주택 공급 ── */
const HOUSING = [
  { label: "총 착공 목표 (2030년)", value: "7.3만호" },
  { label: "신속통합기획", value: "36개소" },
  { label: "모아타운", value: "37개소" },
  { label: "모아주택", value: "1.2만 세대" },
  { label: "가양·등촌 택지개발", value: "4.0만 세대" },
  { label: "양육친화주택", value: "580세대" },
];

/* ── 녹지·생태 ── */
const GREEN = [
  {
    name: "서울초록길",
    detail: "48.4km 조성 (2027년까지)",
  },
  {
    name: "봉천천 생태하천 복원",
    detail: "복개 하천을 생태하천으로 복원 (2026년 완료)",
  },
  {
    name: "도림천 자연친화형 복원",
    detail: "도림천2지류 자연친화형 하천 복원",
  },
  {
    name: "안양천 수변공간",
    detail: "카페·레저시설·수변테라스·캠핑장 도입",
  },
  {
    name: "G밸리 도심형 가로숲",
    detail: "산업단지 내 녹지 확충",
  },
  {
    name: "궁산~증미산 선형보행·녹지네트워크",
    detail: "서울식물원~한강 연결 (2026년 완공)",
  },
];

/* ── 제도 변화 ── */
const REGULATIONS = [
  {
    name: "준공업지역 용적률 상향",
    before: "250%",
    after: "최대 400%",
    detail: "기준·허용용적률도 210%→230%, 230%→250%로 각 20%p 상향",
  },
  {
    name: "정비유형 단순화",
    before: "4가지 유형 (전략·산업·주거·산업단지재생형)",
    after: "2가지 (산업복합형·주거복합형)",
    detail: "공장비율 10% 기준으로 구분",
  },
  {
    name: "복합개발 면적 제한 폐지",
    before: "1만㎡ 미만만 가능",
    after: "면적 무관",
    detail: "사업 주체가 개발 방식 자유 선택",
  },
  {
    name: "산업혁신구역 지정",
    before: "용도·밀도 규제 적용",
    after: "규제 자유 구역",
    detail: "용적률 인센티브 대폭 개선",
  },
];

/* ── 인사이트 ── */
const INSIGHTS = [
  {
    title: "강북전성시대 2.0과 서남권 대개조 2.0: '비강남권 대개조' 양대 축",
    desc: "오세훈 시장은 서남권 대개조 2.0을 '강북전성시대에 이은 비강남권 대개조 2탄'으로 명명했다. 강북은 16조·용적률 1,300%, 서남권은 7.3조·용적률 400%로, 투자 규모와 방식은 다르지만 '비강남권 균형발전'이라는 같은 목표를 향한다. 두 계획 모두 교통→산업→주거→녹지 순서로 전략을 세운 점이 동일하다.",
  },
  {
    title: "남부순환 지하도로 15km — 서남권 교통 판도를 바꿀 핵심 사업",
    desc: "강남↔강서 이동시간을 70분에서 40분으로 단축하는 남부순환 지하도로(개화동~신림동 15km)는 서남권 대개조의 가장 큰 물리적 변화다. 강북전성시대의 '강북횡단 지하고속도로 20.5km'와 대칭되는 사업으로, 서남권이 강남 접근성에서 열위에 놓여 있던 구조를 근본적으로 바꾼다.",
  },
  {
    title: "용적률 400%: 준공업지역의 주거·산업 복합화 가속",
    desc: "준공업지역 용적률 250%→400% 상향은 단순 수치 변화가 아니다. 면적 제한 폐지(기존 1만㎡ 미만만 복합개발 가능)와 정비유형 단순화(4가지→2가지)가 결합되면서, 사실상 준공업지역의 대규모 직주근접 복합개발이 가능해졌다. 서부트럭터미널 1.9조 물류단지, 금천 공군부대 컴팩트시티 등이 이 제도 위에서 추진된다.",
  },
  {
    title: "마곡·G밸리 양대 산업축 — 서울 서남부의 자족성 확보 전략",
    desc: "2040 서울플랜에서 마곡은 광역중심, 가산·대림은 광역중심으로 지정되어 있다. 서남권 대개조 2.0은 이 두 거점을 '피지컬 AI'와 '혁신 플랫폼'이라는 미래산업 키워드로 특화하면서, 서남권이 단순 베드타운에서 벗어나 산업 자족성을 갖추는 방향으로 움직인다.",
  },
  {
    title: "2030년 7.3만호 — 서울 주택공급의 서남권 비중 확대",
    desc: "신속통합기획 36개소, 모아타운 37개소(서울 81개소 중 30개소가 서남권 집중), 가양·등촌 4만 세대 등 2030년까지 7.3만호 착공 계획은 서남권을 서울 주택공급의 핵심 지역으로 만든다. 특히 모아타운의 서남권 집중(37%)은 노후 저층주거지가 많은 이 지역의 특성을 반영한다.",
  },
];

export default function SouthwestPlan() {
  return (
    <div className="space-y-10">
      {/* 헤더 */}
      <section>
        <h2 className="text-2xl font-bold">서남권 대개조 2.0</h2>
        <p className="text-sm text-gray-400 mt-1">
          서울시 · 2026.03.05 발표 · 총 7.3조 투자
        </p>
      </section>

      {/* 한 줄 요약 */}
      <section className="bg-gray-900 text-white rounded-xl p-6">
        <p className="text-sm leading-relaxed">
          강북전성시대에 이은{" "}
          <span className="text-amber-400 font-medium">
            &lsquo;비강남권 대개조&rsquo; 2탄
          </span>
          . 서남권 7개 자치구(양천·강서·구로·금천·영등포·동작·관악)에{" "}
          <span className="text-amber-400 font-medium">7.3조원</span>을
          투입하여, 준공업지역 용적률{" "}
          <span className="text-amber-400 font-medium">250%→400%</span> 상향,
          남부순환 지하도로 15km 신설, 4개 도시철도 노선 추진 등 교통·산업·주거·녹지를
          혁신한다.
        </p>
      </section>

      {/* 대상 지역 */}
      <section>
        <h3 className="text-lg font-bold mb-4">대상 자치구</h3>
        <div className="flex flex-wrap gap-2">
          {DISTRICTS.map((d) => (
            <span
              key={d}
              className="text-sm px-3 py-1.5 rounded-lg bg-amber-50 text-amber-800 font-medium"
            >
              {d}
            </span>
          ))}
        </div>
      </section>

      {/* 재원 */}
      <section>
        <h3 className="text-lg font-bold mb-4">재원 구조 — 총 7.3조</h3>
        <div className="grid grid-cols-3 gap-4 mb-4">
          {BUDGET.map((b) => (
            <div key={b.label} className={`${b.color} rounded-xl p-4 text-center`}>
              <p className={`text-2xl font-bold ${b.textColor}`}>{b.amount}</p>
              <p className="text-xs text-gray-500 mt-1">{b.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 교통: 철도 */}
      <section>
        <h3 className="text-lg font-bold mb-4">교통 — 도시철도 4개 노선</h3>
        <div className="space-y-2">
          {TRANSPORT_RAIL.map((t) => (
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
            </div>
          ))}
        </div>
      </section>

      {/* 교통: 도로 */}
      <section>
        <h3 className="text-lg font-bold mb-4">교통 — 도로 사업</h3>
        <div className="space-y-2">
          {TRANSPORT_ROAD.map((t) => (
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
            </div>
          ))}
        </div>
        <p className="text-xs text-amber-600 font-medium mt-3">
          핵심 효과: 강남↔강서 이동시간 70분 → 40분으로 단축
        </p>
      </section>

      <AdBanner slot="SLOT_SOUTHWEST" className="my-6" />

      {/* 산업 거점 */}
      <section>
        <h3 className="text-lg font-bold mb-4">산업·일자리 거점</h3>
        <div className="space-y-2">
          {INDUSTRY_HUBS.map((hub) => (
            <div
              key={hub.num}
              className={`border rounded-lg p-4 ${
                hub.highlight
                  ? "border-amber-400 bg-amber-50/40"
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
                    <span className="text-xs text-gray-400">{hub.area}</span>
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

      {/* 제도 변화 */}
      <section>
        <h3 className="text-lg font-bold mb-4">핵심 제도 변화</h3>
        <div className="space-y-3">
          {REGULATIONS.map((reg) => (
            <div
              key={reg.name}
              className="border border-gray-200 rounded-lg p-4"
            >
              <h4 className="text-sm font-bold mb-2">{reg.name}</h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
                <div>
                  <span className="text-gray-400">기존</span>
                  <p className="text-gray-500 mt-0.5 line-through">{reg.before}</p>
                </div>
                <div>
                  <span className="text-gray-400">변경</span>
                  <p className="text-amber-700 font-medium mt-0.5">{reg.after}</p>
                </div>
                <div>
                  <span className="text-gray-400">상세</span>
                  <p className="text-gray-700 mt-0.5">{reg.detail}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 주택 공급 */}
      <section>
        <h3 className="text-lg font-bold mb-4">주택 공급 (2030년 목표)</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {HOUSING.map((h) => (
            <div key={h.label} className="border border-gray-200 rounded-lg p-3">
              <p className="text-lg font-bold text-gray-900">{h.value}</p>
              <p className="text-xs text-gray-400 mt-0.5">{h.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 녹지 */}
      <section>
        <h3 className="text-lg font-bold mb-4">녹지·생태 사업</h3>
        <div className="space-y-2">
          {GREEN.map((g) => (
            <div
              key={g.name}
              className="border border-gray-200 rounded-lg p-4 flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-6"
            >
              <h4 className="text-sm font-bold flex-1">{g.name}</h4>
              <p className="text-xs text-gray-600 sm:text-right shrink-0">
                {g.detail}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* 인사이트 */}
      <section>
        <div className="border-t-2 border-gray-900 pt-6">
          <h3 className="text-lg font-bold mb-1">
            인사이트 — 2040 서울플랜 × 서남권 대개조 2.0
          </h3>
          <p className="text-xs text-gray-400 mb-6">
            정책 원문과 보도자료를 교차하여 도출한 분석입니다. 서울시 공식 해석과
            다를 수 있습니다.
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
          ①{" "}
          <a
            href="https://mediahub.seoul.go.kr/archives/2010408"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            서울시 미디어허브 — 서남권 대개조 보도자료
          </a>
          {" · "}
          ②{" "}
          <a
            href="https://biz.heraldcorp.com/article/10687438"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            헤럴드경제 — 서남권 대개조 2.0 상세
          </a>
          {" · "}
          ③{" "}
          <a
            href="https://www.engdaily.com/news/articleView.html?idxno=21858"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            엔지니어링데일리
          </a>
          {" · "}
          ④{" "}
          <a
            href="https://www.hankyung.com/article/2024022726065"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            한국경제 — 용적률 상향 상세
          </a>
          {" · "}
          ⑤ 서울특별시, 「2040 서울도시기본계획」, 2023.02
        </p>
        <p className="text-xs text-gray-400 mt-2">
          원문 보고서 PDF는 아직 공개되지 않았습니다. 공개 시 업데이트 예정.
        </p>
      </section>
    </div>
  );
}
