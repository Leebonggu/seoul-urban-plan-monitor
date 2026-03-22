import os
import json
import requests
from wp_config import WP_API_BASE, WP_USER, WP_APP_PASSWORD


def _auth():
    return (WP_USER, WP_APP_PASSWORD)


def upload_image(image_path: str) -> dict:
    """이미지를 WP Media Library에 업로드."""
    filename = os.path.basename(image_path)
    with open(image_path, "rb") as f:
        resp = requests.post(
            f"{WP_API_BASE}/media",
            auth=_auth(),
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "image/png",
            },
            data=f.read(),
            timeout=60,
        )
    resp.raise_for_status()
    return resp.json()


def create_post(title: str, html: str, status: str = "publish", categories: list[int] | None = None, featured_image_id: int | None = None) -> dict:
    """WordPress 포스트 생성."""
    payload = {
        "title": title,
        "content": html,
        "status": status,
    }
    if categories:
        payload["categories"] = categories
    if featured_image_id:
        payload["featured_media"] = featured_image_id
    resp = requests.post(
        f"{WP_API_BASE}/posts",
        auth=_auth(),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def load_published(filepath: str = "data/wp_published.json") -> dict:
    """발행 완료된 notice_code → WP URL 매핑 로드."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_published(data: dict, filepath: str = "data/wp_published.json"):
    """발행 기록 저장."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
