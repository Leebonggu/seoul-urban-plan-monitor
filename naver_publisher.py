"""
네이버 블로그 자동 포스팅.

사전 준비 (최초 1회):
  1. https://developers.naver.com → 애플리케이션 등록
     - 사용 API: 블로그 (글쓰기)
     - 서비스 URL: 본인 사이트 또는 http://localhost
  2. Client ID / Secret 발급 → GitHub Secrets에 저장
  3. 최초 OAuth 인증 (로컬 브라우저 필요):
       python naver_publisher.py --auth
     → 브라우저에서 로그인 후 콘솔에 출력된 access_token, refresh_token을 GitHub Secrets에 저장

Env vars (GitHub Secrets):
  NAVER_CLIENT_ID       — 애플리케이션 Client ID
  NAVER_CLIENT_SECRET   — 애플리케이션 Client Secret
  NAVER_ACCESS_TOKEN    — OAuth 액세스 토큰
  NAVER_REFRESH_TOKEN   — OAuth 리프레시 토큰 (만료 시 자동 갱신)
  NAVER_BLOG_ID         — 네이버 아이디 (블로그 ID와 동일)
"""

import os
import sys
import httpx

_TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
_WRITE_URL  = "https://openapi.naver.com/v1/blog/writePost.json"


def _env(key: str) -> str:
    return os.environ.get(key, "")


def _refresh_token() -> str:
    """리프레시 토큰으로 액세스 토큰 갱신. 실패 시 빈 문자열 반환."""
    resp = httpx.post(_TOKEN_URL, params={
        "grant_type":    "refresh_token",
        "client_id":     _env("NAVER_CLIENT_ID"),
        "client_secret": _env("NAVER_CLIENT_SECRET"),
        "refresh_token": _env("NAVER_REFRESH_TOKEN"),
    }, timeout=10)
    return resp.json().get("access_token", "") if resp.status_code == 200 else ""


def post_to_naver_blog(title: str, html: str, tags: list[str]) -> bool:
    """네이버 블로그에 포스트 발행. 성공 시 True."""
    blog_id = _env("NAVER_BLOG_ID")
    token   = _env("NAVER_ACCESS_TOKEN") or _refresh_token()

    if not token or not blog_id:
        print("    [네이버] env 미설정 (NAVER_ACCESS_TOKEN, NAVER_BLOG_ID) — 스킵")
        return False

    resp = httpx.post(
        _WRITE_URL,
        headers={"Authorization": f"Bearer {token}"},
        data={
            "blogId":   blog_id,
            "title":    title,
            "contents": html,
            "tags":     ",".join(tags[:10]),
        },
        timeout=20,
    )

    if resp.status_code == 200:
        print("    [네이버] 발행 완료")
        return True

    # 토큰 만료(401) 시 갱신 후 재시도
    if resp.status_code == 401:
        new_token = _refresh_token()
        if not new_token:
            print("    [네이버] 토큰 갱신 실패")
            return False
        resp2 = httpx.post(
            _WRITE_URL,
            headers={"Authorization": f"Bearer {new_token}"},
            data={"blogId": blog_id, "title": title, "contents": html, "tags": ",".join(tags[:10])},
            timeout=20,
        )
        if resp2.status_code == 200:
            print("    [네이버] 발행 완료 (토큰 갱신 후)")
            return True

    print(f"    [네이버] 발행 실패: {resp.status_code} {resp.text[:120]}")
    return False


# ── 최초 OAuth 인증 흐름 ──────────────────────────────────────────────────────
def _run_auth():
    """브라우저 OAuth 인증 후 토큰 출력. 최초 1회만 실행."""
    client_id = _env("NAVER_CLIENT_ID")
    if not client_id:
        print("NAVER_CLIENT_ID 환경변수를 먼저 설정하세요.")
        sys.exit(1)

    redirect_uri = "http://localhost"
    auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize"
        f"?response_type=code&client_id={client_id}"
        f"&redirect_uri={redirect_uri}&state=SEOUL_GOSI"
    )
    print(f"\n아래 URL을 브라우저에서 열고 로그인 후, 리디렉션된 URL을 붙여넣으세요:\n\n{auth_url}\n")
    redirected = input("리디렉션 URL: ").strip()

    from urllib.parse import urlparse, parse_qs
    code = parse_qs(urlparse(redirected).query).get("code", [""])[0]
    if not code:
        print("code 파라미터를 찾을 수 없습니다.")
        sys.exit(1)

    resp = httpx.post(_TOKEN_URL, params={
        "grant_type":    "authorization_code",
        "client_id":     client_id,
        "client_secret": _env("NAVER_CLIENT_SECRET"),
        "redirect_uri":  redirect_uri,
        "code":          code,
        "state":         "SEOUL_GOSI",
    }, timeout=10)
    data = resp.json()
    print("\n=== GitHub Secrets에 아래 값을 저장하세요 ===")
    print(f"NAVER_ACCESS_TOKEN  = {data.get('access_token', '(없음)')}")
    print(f"NAVER_REFRESH_TOKEN = {data.get('refresh_token', '(없음)')}")


if __name__ == "__main__":
    if "--auth" in sys.argv:
        _run_auth()
    else:
        print("사용법: python naver_publisher.py --auth")
