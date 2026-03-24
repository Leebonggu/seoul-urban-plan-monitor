"""기존 WP 포스트에 Google Maps 지도를 추가하는 일회성 스크립트.

Usage:
  python wp_update_maps.py           # 드라이런 (변경 없이 확인만)
  python wp_update_maps.py --apply   # 실제 업데이트 적용

Env vars: WP_URL, WP_USER, WP_APP_PASSWORD
"""
import os
import sys
import json
import glob
import re

import requests

from wp_config import WP_API_BASE, WP_USER, WP_APP_PASSWORD, validate_config


def _auth():
    return (WP_USER, WP_APP_PASSWORD)


def load_all_records() -> dict[str, dict]:
    """notice_code → record 매핑."""
    data_dir = os.environ.get("DATA_DIR", "data")
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\.json$")
    records = {}
    for filepath in glob.glob(os.path.join(data_dir, "*.json")):
        if not date_pattern.match(os.path.basename(filepath)):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            for r in json.load(f):
                records[r["notice_code"]] = r
    return records


def get_post_id_from_url(wp_url: str) -> int | None:
    """WP URL로 포스트 ID 조회."""
    slug = wp_url.rstrip("/").split("/")[-1]
    resp = requests.get(
        f"{WP_API_BASE}/posts",
        params={"slug": slug},
        auth=_auth(),
        timeout=30,
    )
    resp.raise_for_status()
    posts = resp.json()
    return posts[0]["id"] if posts else None


def build_map_html(location: str) -> str:
    map_query = location.replace(" ", "+")
    return (
        f'<h2>🗺️ 위치</h2>\n'
        f'<iframe '
        f'src="https://maps.google.com/maps?q={map_query}&amp;output=embed&amp;hl=ko" '
        f'width="100%" height="400" style="border:0;border-radius:4px;margin-bottom:24px;" '
        f'allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade">'
        f'</iframe>'
    )


def update_post_content(post_id: int, new_content: str) -> bool:
    resp = requests.post(
        f"{WP_API_BASE}/posts/{post_id}",
        auth=_auth(),
        json={"content": new_content},
        timeout=30,
    )
    resp.raise_for_status()
    return True


def main():
    validate_config()
    apply = "--apply" in sys.argv

    if not apply:
        print("[드라이런 모드] --apply 플래그로 실제 업데이트")
        print()

    # 발행 기록 로드
    published_path = os.path.join(os.environ.get("DATA_DIR", "data"), "wp_published.json")
    with open(published_path, "r", encoding="utf-8") as f:
        published = json.load(f)

    records = load_all_records()

    updated = 0
    skipped = 0
    failed = 0

    for notice_code, wp_url in published.items():
        record = records.get(notice_code)
        if not record:
            print(f"  [{notice_code}] 레코드 없음, 건너뜀")
            skipped += 1
            continue

        location = record.get("location") or ""
        if not location:
            print(f"  [{notice_code}] 위치 정보 없음, 건너뜀")
            skipped += 1
            continue

        if not apply:
            print(f"  [{notice_code}] 지도 추가 예정: {location[:40]}")
            updated += 1
            continue

        # 포스트 ID 가져오기
        try:
            post_id = get_post_id_from_url(wp_url)
            if not post_id:
                print(f"  [{notice_code}] 포스트 못 찾음: {wp_url}")
                failed += 1
                continue

            # 기존 콘텐츠 가져오기
            resp = requests.get(
                f"{WP_API_BASE}/posts/{post_id}",
                params={"context": "edit"},
                auth=_auth(),
                timeout=30,
            )
            resp.raise_for_status()
            post_data = resp.json()
            rendered_content = post_data["content"]["rendered"]
            raw_content = post_data["content"]["raw"]

            # 이미 지도가 있으면 건너뜀
            if "maps.google.com/maps" in rendered_content:
                print(f"  [{notice_code}] 이미 지도 있음, 건너뜀")
                skipped += 1
                continue

            # 관련 링크 섹션 앞에 지도 삽입
            map_html = build_map_html(location)

            if "🔗 관련 링크" in raw_content:
                new_content = raw_content.replace(
                    '<h2>🔗 관련 링크</h2>',
                    f'{map_html}\n<h2>🔗 관련 링크</h2>'
                )
            elif "<hr" in raw_content:
                new_content = raw_content.replace(
                    '<hr',
                    f'{map_html}\n<hr',
                    1,
                )
            else:
                new_content = raw_content + f'\n{map_html}'

            update_post_content(post_id, new_content)
            print(f"  [{notice_code}] 지도 추가 완료: {location[:40]}")
            updated += 1

        except Exception as e:
            print(f"  [{notice_code}] 실패: {e}")
            failed += 1

    print()
    print(f"결과: 업데이트 {updated}건, 건너뜀 {skipped}건, 실패 {failed}건")


if __name__ == "__main__":
    main()
