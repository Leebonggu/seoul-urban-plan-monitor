import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "개인정보처리방침",
  description:
    "서울 결정고시 모니터의 개인정보처리방침. 수집하는 개인정보, 쿠키 및 광고, 데이터 출처 안내.",
};

export const dynamic = "force-static";

export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-bold mb-6">개인정보처리방침</h1>
      <div className="prose prose-sm text-gray-600 space-y-4">
        <p>
          서울 결정고시 모니터(이하 &quot;서비스&quot;)는 이용자의 개인정보를
          중요시하며, 관련 법령을 준수합니다.
        </p>

        <h2 className="text-lg font-bold mt-6">1. 수집하는 개인정보</h2>
        <p>
          본 서비스는 별도의 회원가입 없이 이용할 수 있으며, 개인정보를 직접
          수집하지 않습니다.
        </p>

        <h2 className="text-lg font-bold mt-6">2. 쿠키 및 광고</h2>
        <p>
          본 서비스는 Google AdSense를 통해 광고를 게재하며, 이 과정에서
          쿠키가 사용될 수 있습니다. Google의 쿠키 사용에 대한 자세한 내용은{" "}
          <a
            href="https://policies.google.com/technologies/ads"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            Google 광고 정책
          </a>
          을 참조하세요.
        </p>

        <h2 className="text-lg font-bold mt-6">3. 데이터 출처</h2>
        <p>
          본 서비스에서 제공하는 고시문 데이터는 서울도시공간포털
          (urban.seoul.go.kr)에서 공개한 공공데이터를 활용합니다.
        </p>

        <h2 className="text-lg font-bold mt-6">4. 문의</h2>
        <p>
          개인정보 관련 문의사항은 서비스 운영자에게 연락해 주세요.
        </p>
      </div>
    </div>
  );
}
