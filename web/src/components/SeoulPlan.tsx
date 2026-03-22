"use client";

import Image from "next/image";

const GOALS = [
  {
    num: 1,
    title: "걸어서 누리는 다양한 일상",
    sub: "보행일상권 조성",
    desc: "주거지를 중심으로 업무·교육·쇼핑·여가·문화 등 다양한 활동을 도보 30분 내에 누릴 수 있는 자족적 생활권을 조성합니다.",
    img: "/seoul-plan/sub_13_001.png",
  },
  {
    num: 2,
    title: "수변 공간의 잠재력 발굴",
    sub: "수변 중심 공간 재편",
    desc: "한강과 주요 지천의 수변공간을 활용하여 여가·관광기능을 증진하고, 한강 양안 중심지 간 도시기능을 연계합니다.",
    img: "/seoul-plan/sub_13_002.png",
  },
  {
    num: 3,
    title: "새로운 도시공간의 창출",
    sub: "기반시설 입체화",
    desc: "철도 지하화, 도로 입체화, 차량기지 복합개발 등으로 새로운 가용지를 확보하고 도시공간을 창출합니다.",
    img: "/seoul-plan/sub_13_003.png",
  },
  {
    num: 4,
    title: "미래성장거점의 육성과 연계",
    sub: "중심지 기능 혁신",
    desc: "3도심·7광역중심·12지역중심의 중심지 체계를 유지하며, 일자리·주거·여가 기능이 복합된 24시간 활력 있는 지역으로 고도화합니다.",
    img: "/seoul-plan/sub_13_004.png",
  },
  {
    num: 5,
    title: "기술발전에 선제적 대응",
    sub: "미래교통 기반시설 구축",
    desc: "GTX 등 광역급행철도, 자율주행차, 도심항공교통(UAM) 등 미래교통수단의 인프라를 구축합니다.",
    img: "/seoul-plan/sub_13_005.png",
  },
  {
    num: 6,
    title: "미래위기에 준비",
    sub: "탄소중립 안전도시",
    desc: "2050년 탄소중립도시를 목표로 자립적 자원순환체계와 전방위적 방재체계를 구축합니다.",
    img: "/seoul-plan/sub_13_006.png",
  },
  {
    num: 7,
    title: "도시의 다양한 모습 구현",
    sub: "도시계획 대전환",
    desc: "'Beyond Zoning Seoul'을 추진하여 용도지역제를 유연하게 적용하고 다기능 복합용도를 유도합니다.",
    img: "/seoul-plan/sub_13_007.png",
  },
];

const CENTERS_DATA = [
  {
    grade: "도심",
    color: "#ef4444",
    centers: [
      {
        name: "서울도심 (한양도성)",
        role: "국제문화교류중심지",
        desc: "4+1축을 중심으로 역사문화 기반의 미래 도심 조성. 광화문 일대 국가중심공간 체계적 관리.",
      },
      {
        name: "여의도·영등포",
        role: "국제금융중심지",
        desc: "국제디지털금융업무 생태계 육성. 영등포 산업지역 재생·정비로 신산업·일자리 공간 조성.",
      },
      {
        name: "강남",
        role: "국제업무중심지",
        desc: "영동대로·경부간선도로 입체복합화로 가용지 확보. 국제교류복합지구 조성.",
      },
    ],
  },
  {
    grade: "광역중심",
    color: "#3b82f6",
    centers: [
      {
        name: "용산",
        desc: "서울도심·여의도 연계 한강 중심 국제업무중심지. 용산공원 연계 국제 수준 어메니티 공간.",
      },
      {
        name: "청량리·왕십리",
        desc: "동북권 혁신산업·문화 중심지. 청량리 철도 상부 입체복합개발, 홍릉R&D 연계.",
      },
      {
        name: "창동·상계",
        desc: "수도권 동북부 일자리·문화산업 중심지. 바이오·메디컬, 문화콘텐츠 특화.",
      },
      {
        name: "상암·수색",
        desc: "디지털 미디어 산업 기반 글로벌 창조문화 중심지. 서북권 산업·경제거점.",
      },
      {
        name: "마곡",
        desc: "동북아 미래를 선도하는 지식산업 기반 고용 중심지. 자족적 R&D 클러스터.",
      },
      {
        name: "가산·대림",
        desc: "G밸리 혁신·고도화로 신성장 산업 선도. 산업·창업 지원 및 복합기능 강화.",
      },
      {
        name: "잠실",
        desc: "강남 도심 연계 국제 업무·관광 중심지. 국제적 관광·쇼핑·MICE 산업벨트.",
      },
    ],
  },
  {
    grade: "지역중심",
    color: "#f59e0b",
    centers: [
      { name: "동대문", desc: "도심형 특화산업(패션·문화) 활성화 지원 거점." },
      {
        name: "성수",
        desc: "동북권 자족기능 선도, 창조적 지식기반산업·생활서비스 중심지.",
      },
      {
        name: "망우",
        desc: "동북부 수도권 비즈니스·생활서비스 중심지. 산업·업무기능 육성.",
      },
      {
        name: "미아",
        desc: "동북2권 문화·쇼핑·업무 중심지. 상업·업무·교육 기능 확충.",
      },
      {
        name: "연신내·불광",
        desc: "서북부 수도권 상업·문화 및 혁신산업 중심지. GTX 연계 복합화.",
      },
      {
        name: "신촌",
        desc: "대학 자원 기반 창조문화산업 거점. 디자인·출판, AI·IT융합 육성.",
      },
      {
        name: "마포·공덕",
        desc: "서울도심·여의도 지원 서북권 업무중심지. 근린상업·문화 보완.",
      },
      {
        name: "목동",
        desc: "서남1권 상업·업무·문화 중심지. 생활서비스기능 보완.",
      },
      {
        name: "봉천",
        desc: "행정·상업·문화 복합 서남2권 업무 중심지. 벤처·창업 지원.",
      },
      {
        name: "사당·이수",
        desc: "광역교통 환승 쇼핑·여가 중심지. 수도권 남부 연계.",
      },
      {
        name: "수서·문정",
        desc: "신성장 로봇·IT산업 특화 첨단산업·업무 서비스 중심지.",
      },
      {
        name: "천호·길동",
        desc: "서울 동부 상업·업무복합 중심지. 쇼핑·여가·문화 활성화.",
      },
    ],
  },
];

const AXES = [
  {
    name: "청년첨단 혁신축",
    sub: "바이오·의료·ICT",
    area: "동북권",
    desc: "홍릉 바이오의료허브 → 청량리 → 창동·상계. 바이오 메디컬 혁신산업 공간.",
    color: "#10b981",
  },
  {
    name: "감성문화 혁신축",
    sub: "방송·문화·미디어·R&D",
    area: "서북권",
    desc: "상암 DMC 중심 미래 창조문화 콘텐츠 시장 혁신기지. 마곡 R&D 연계.",
    color: "#8b5cf6",
  },
  {
    name: "국제경쟁 혁신축",
    sub: "금융·핀테크·업무·역사",
    area: "서남권",
    desc: "광화문 → 서울역 → 용산 → 여의도·영등포. 국가중심공간·금융중심지.",
    color: "#f59e0b",
  },
  {
    name: "미래융합 혁신축",
    sub: "AI·R&D·로봇·MICE",
    area: "동남권",
    desc: "강남 → 양재 R&D → 수서·문정. AI, 빅데이터, 로봇산업 등 미래 산업.",
    color: "#3b82f6",
  },
];

export default function SeoulPlan() {
  return (
    <div className="space-y-10">
      {/* 개요 */}
      <section>
        <div className="text-center mb-6">
          <h2 className="text-xl font-bold">2040 서울도시기본계획 (서울플랜)</h2>
          <p className="text-sm text-gray-500 mt-1">
            향후 20년간 서울시가 나아갈 방향을 제시하는 도시계획 분야 최상위
            법정계획
          </p>
          <p className="text-lg font-semibold text-blue-600 mt-3">
            &ldquo;살기 좋은 나의 서울, 세계 속에 모두의 서울&rdquo;
          </p>
        </div>
      </section>

      {/* 7대 목표 */}
      <section>
        <h3 className="text-lg font-bold mb-4">7대 목표</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {GOALS.map((g) => (
            <div
              key={g.num}
              className="border border-gray-200 rounded-xl p-4 flex flex-col items-center text-center"
            >
              <Image
                src={g.img}
                alt={g.title}
                width={180}
                height={120}
                className="mb-3"
              />
              <div className="text-xs text-blue-600 font-bold mb-1">
                목표 {g.num}
              </div>
              <h4 className="text-sm font-bold mb-0.5">{g.title}</h4>
              <p className="text-xs text-gray-400 mb-2">{g.sub}</p>
              <p className="text-xs text-gray-600 leading-relaxed">{g.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 도시공간구조 */}
      <section>
        <h3 className="text-lg font-bold mb-4">도시공간구조</h3>
        <div className="border border-gray-200 rounded-xl overflow-hidden">
          <div className="bg-gray-900 p-6 flex justify-center">
            <Image
              src="/seoul-plan/sub_13_008.png"
              alt="도시공간구조 체계"
              width={500}
              height={300}
              className="max-w-full h-auto"
            />
          </div>
          <div className="p-4">
            <p className="text-sm text-gray-600 leading-relaxed">
              중심지 체계(3도심·7광역중심·12지역중심)와 광역교통축,
              산업·경제축, 공원·녹지·수변축을 연계하여 도시공간구조를
              구성합니다.
            </p>
          </div>
        </div>

        {/* 도시공간구조 지도 */}
        <div className="mt-4 border border-gray-200 rounded-xl overflow-hidden">
          <div className="bg-white p-4 flex justify-center">
            <Image
              src="/seoul-plan/sub_13_map.png"
              alt="서울시 도시공간구조 지도"
              width={800}
              height={600}
              className="max-w-full h-auto"
            />
          </div>
          <div className="px-4 pb-4">
            <p className="text-xs text-gray-400 text-center">
              서울시 도시공간구조 종합 — 중심지 체계, 광역교통축, 산업·경제축,
              공원·녹지·수변축
            </p>
          </div>
        </div>

        {/* 4개 축 이미지 */}
        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            {
              img: "/seoul-plan/sub_13_009.png",
              title: "중심지 체계",
              desc: "3도심·7광역중심·12지역중심",
            },
            {
              img: "/seoul-plan/sub_13_010.png",
              title: "광역교통축",
              desc: "GTX 등 광역급행철도망 연계",
            },
            {
              img: "/seoul-plan/sub_13_011.png",
              title: "산업·경제축",
              desc: "4대 혁신축과 산업거점",
            },
            {
              img: "/seoul-plan/sub_13_012.png",
              title: "공원·녹지·수변축",
              desc: "한강·지천 수변 및 녹지 네트워크",
            },
          ].map((item) => (
            <div
              key={item.title}
              className="border border-gray-200 rounded-xl overflow-hidden"
            >
              <div className="bg-white p-3 flex justify-center">
                <Image
                  src={item.img}
                  alt={item.title}
                  width={400}
                  height={350}
                  className="max-w-full h-auto"
                />
              </div>
              <div className="px-4 pb-3">
                <h4 className="text-sm font-bold">{item.title}</h4>
                <p className="text-xs text-gray-400">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 중심지 체계 상세 */}
      <section>
        <h3 className="text-lg font-bold mb-4">
          중심지 체계 — 특성 및 육성방향
        </h3>
        <div className="space-y-6">
          {CENTERS_DATA.map((group) => (
            <div key={group.grade}>
              <div className="flex items-center gap-2 mb-3">
                <span
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: group.color }}
                />
                <h4 className="font-bold">
                  {group.grade} ({group.centers.length})
                </h4>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {group.centers.map((c) => (
                  <div
                    key={c.name}
                    className="border rounded-lg p-3"
                    style={{ borderColor: group.color + "40" }}
                  >
                    <div className="flex items-start gap-2 mb-1">
                      <span
                        className="text-xs px-1.5 py-0.5 rounded text-white font-medium shrink-0 mt-0.5"
                        style={{ backgroundColor: group.color }}
                      >
                        {group.grade}
                      </span>
                      <h5 className="text-sm font-bold">{c.name}</h5>
                    </div>
                    {"role" in c && c.role && (
                      <p className="text-xs text-blue-600 font-medium mb-1 ml-[calc(0.375rem+1px+0.5rem)]">
                        {c.role}
                      </p>
                    )}
                    <p className="text-xs text-gray-600 leading-relaxed">
                      {c.desc}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 4대 혁신축 */}
      <section>
        <h3 className="text-lg font-bold mb-4">4대 혁신축</h3>
        <p className="text-sm text-gray-500 mb-4">
          중심지 체계와 산업거점·자원을 연계하여 권역별 미래 성장기반을
          구축합니다.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {AXES.map((a) => (
            <div
              key={a.name}
              className="border rounded-xl p-4"
              style={{ borderColor: a.color + "40" }}
            >
              <div className="flex items-center gap-2 mb-2">
                <span
                  className="w-2.5 h-2.5 rounded-full"
                  style={{ backgroundColor: a.color }}
                />
                <h4 className="text-sm font-bold">{a.name}</h4>
                <span className="text-xs text-gray-400">({a.area})</span>
              </div>
              <p className="text-xs text-gray-500 mb-1">{a.sub}</p>
              <p className="text-xs text-gray-600 leading-relaxed">{a.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 출처 */}
      <section className="border-t border-gray-200 pt-4">
        <p className="text-xs text-gray-400 leading-relaxed">
          <span className="font-medium text-gray-500">출처:</span>{" "}
          서울특별시, 「2040 서울도시기본계획」, 2023년 2월 발간.{" "}
          <a
            href="https://urban.seoul.go.kr/view/html/PMNU3030000001"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            서울도시공간포털
          </a>{" "}
          |{" "}
          <a
            href="https://urban.seoul.go.kr/UpisArchive/DATA/PWEB/STATIC/2040_seoul_plan.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            원문 PDF 다운로드
          </a>
        </p>
      </section>
    </div>
  );
}
