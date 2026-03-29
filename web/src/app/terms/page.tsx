import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "이용약관",
  description:
    "서울 결정고시 모니터 이용약관. 서비스 개요, 데이터 정확성, 분석 콘텐츠, 저작권 안내.",
};

export const dynamic = "force-static";

export default function TermsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-bold mb-6">이용약관</h1>
      <div className="prose prose-sm text-gray-600 space-y-4">
        <h2 className="text-lg font-bold mt-6">1. 서비스 개요</h2>
        <p>
          서울 결정고시 모니터는 서울시 도시계획 결정고시를 수집·분석하여
          제공하는 정보 서비스입니다.
        </p>

        <h2 className="text-lg font-bold mt-6">2. 데이터 정확성</h2>
        <p>
          본 서비스는 서울도시공간포털의 공공데이터를 기반으로 하며, 데이터의
          정확성을 보장하지 않습니다. 정확한 정보는 원문을 확인해 주세요.
        </p>

        <h2 className="text-lg font-bold mt-6">3. 분석 콘텐츠</h2>
        <p>
          본 서비스에서 제공하는 분석 및 인사이트는 참고용이며, 투자 판단의
          근거로 사용하기에 부적합합니다. 투자 결정은 이용자 본인의 판단과
          책임 하에 이루어져야 합니다.
        </p>

        <h2 className="text-lg font-bold mt-6">4. 저작권</h2>
        <p>
          고시문 원문은 공공저작물로서 출처 표시 시 자유 이용이 가능합니다.
          본 서비스의 분석 콘텐츠 및 디자인에 대한 저작권은 서비스 운영자에게
          있습니다.
        </p>

        <h2 className="text-lg font-bold mt-6">5. 면책</h2>
        <p>
          본 서비스 이용으로 발생하는 직·간접적 손해에 대해 서비스 운영자는
          책임을 지지 않습니다.
        </p>
      </div>
    </div>
  );
}
