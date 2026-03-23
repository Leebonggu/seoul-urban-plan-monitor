import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-white mt-12">
      <div className="max-w-7xl mx-auto px-4 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
        <p className="text-xs text-gray-400">
          데이터 출처: 서울도시공간포털 (urban.seoul.go.kr)
        </p>
        <div className="flex gap-4 text-xs text-gray-400">
          <a href="https://2lee.kr" target="_blank" rel="noopener noreferrer" className="hover:text-gray-600">
            봉수네 돈공부 블로그
          </a>
          <Link href="/privacy" className="hover:text-gray-600">
            개인정보처리방침
          </Link>
          <Link href="/terms" className="hover:text-gray-600">
            이용약관
          </Link>
        </div>
      </div>
    </footer>
  );
}
