import os
import requests
from urllib.parse import urlparse


def download_doc(url: str, output_dir: str) -> str | None:
    """고시문 원문을 다운로드. PDF만 지원, HWP는 건너뜀."""
    if not url:
        return None

    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lower()

    if ext not in (".pdf",):
        return None

    resp = requests.get(url, timeout=30)
    if resp.status_code != 200:
        return None

    original = os.path.basename(parsed.path)
    # 파일명이 너무 긴 경우 해시로 축약
    if len(original.encode("utf-8")) > 200:
        import hashlib
        name_hash = hashlib.md5(original.encode()).hexdigest()[:12]
        filename = f"{name_hash}.pdf"
    else:
        filename = original
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(resp.content)

    return filepath


def convert_pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> list[str]:
    """PDF를 페이지별 PNG로 변환."""
    from pdf2image import convert_from_path

    images = convert_from_path(pdf_path, dpi=dpi)
    paths = []
    base = os.path.splitext(os.path.basename(pdf_path))[0]

    for i, img in enumerate(images):
        img_path = os.path.join(output_dir, f"{base}_page_{i + 1}.png")
        img.save(img_path, "PNG")
        paths.append(img_path)

    return paths
