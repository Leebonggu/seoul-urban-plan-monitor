"""기존 WP 포스트 전체 삭제 + wp_published.json 초기화."""
import json
import requests
from wp_config import validate_config, WP_API_BASE, WP_USER, WP_APP_PASSWORD


def delete_all_posts():
    validate_config()
    auth = (WP_USER, WP_APP_PASSWORD)
    page = 1
    deleted = 0

    while True:
        resp = requests.get(
            f"{WP_API_BASE}/posts",
            auth=auth,
            params={"per_page": 100, "page": page, "status": "publish,draft,pending"},
            timeout=30,
        )
        if resp.status_code != 200:
            break

        posts = resp.json()
        if not posts:
            break

        for post in posts:
            pid = post["id"]
            title = post["title"]["rendered"][:40]
            del_resp = requests.delete(
                f"{WP_API_BASE}/posts/{pid}",
                auth=auth,
                params={"force": True},
                timeout=30,
            )
            if del_resp.status_code == 200:
                deleted += 1
                print(f"  삭제: [{pid}] {title}")
            else:
                print(f"  실패: [{pid}] {title} — {del_resp.status_code}")

    print(f"\n총 {deleted}건 삭제 완료.")

    # wp_published.json 초기화
    with open("data/wp_published.json", "w", encoding="utf-8") as f:
        json.dump({}, f)
    print("wp_published.json 초기화 완료.")


if __name__ == "__main__":
    delete_all_posts()
