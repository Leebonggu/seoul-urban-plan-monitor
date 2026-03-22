"""고시문 썸네일 생성. PDF 첫 페이지 + 등급별 컬러 오버레이 + 텍스트."""
import os
from PIL import Image, ImageDraw, ImageFont

# 중심지 등급별 오버레이 색상 (R, G, B)
GRADE_COLORS = {
    "도심": (59, 130, 246),       # 파랑
    "광역중심": (34, 197, 94),    # 초록
    "지역중심": (249, 115, 22),   # 주황
}
DEFAULT_COLOR = (156, 163, 175)   # 회색

THUMB_WIDTH = 800
THUMB_HEIGHT = 800  # 정사각형 — 테마 크롭에 강함


def create_thumbnail(
    record: dict,
    output_path: str,
    pdf_first_page: str | None = None,
) -> str:
    """썸네일 이미지 생성."""
    center_grade = record.get("center_grade") or ""
    color = GRADE_COLORS.get(center_grade, DEFAULT_COLOR)

    if pdf_first_page and os.path.exists(pdf_first_page):
        thumb = _create_with_pdf(pdf_first_page, color, record)
    else:
        thumb = _create_solid(color, record)

    thumb.save(output_path, "PNG", optimize=True)
    return output_path


def _create_with_pdf(pdf_image_path: str, color: tuple, record: dict) -> Image.Image:
    """PDF 첫 페이지를 배경으로 썸네일 생성."""
    bg = Image.open(pdf_image_path).convert("RGB")
    # 정사각형 중앙 크롭
    bg = _center_crop(bg, THUMB_WIDTH, THUMB_HEIGHT)

    # 진한 반투명 오버레이 (텍스트 가독성)
    overlay = Image.new("RGBA", (THUMB_WIDTH, THUMB_HEIGHT), (*color, 210))
    bg = bg.convert("RGBA")
    bg = Image.alpha_composite(bg, overlay)

    _draw_text(bg, record, color)
    return bg.convert("RGB")


def _create_solid(color: tuple, record: dict) -> Image.Image:
    """단색 배경 썸네일 생성."""
    bg = Image.new("RGBA", (THUMB_WIDTH, THUMB_HEIGHT), (*color, 255))
    _draw_text(bg, record, color)
    return bg.convert("RGB")


def _center_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """이미지를 중앙 기준으로 크롭+리사이즈."""
    w, h = img.size
    ratio = max(target_w / w, target_h / h)
    img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    w, h = img.size
    left = (w - target_w) // 2
    top = (h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def _draw_text(img: Image.Image, record: dict, color: tuple):
    """썸네일에 텍스트 — 중앙 정렬."""
    draw = ImageDraw.Draw(img)

    font_large = _get_font(44)
    font_medium = _get_font(24)
    font_small = _get_font(18)

    location = record.get("location") or ""
    title_location = location.split(" ")[0] if location else record.get("organ_name", "서울")
    notice_type = record.get("notice_type") or "도시계획"
    center_grade = record.get("center_grade") or "기타"
    center_name = record.get("center_name") or ""
    title = record.get("title", "")
    date = record.get("notice_date", "")

    # 제목 줄바꿈 처리
    title_lines = _wrap_text(title, font_medium, THUMB_WIDTH - 120)

    # 전체 텍스트 블록 높이 계산 (중앙 배치용)
    badge_text = f" {center_grade} · {center_name} " if center_name else f" {center_grade} "
    badge_h = 32
    gap = 20
    location_h = 50
    type_h = 30
    title_h = len(title_lines) * 34
    date_h = 24
    total_h = badge_h + gap + location_h + gap + type_h + gap + title_h + gap * 2 + date_h
    start_y = (THUMB_HEIGHT - total_h) // 2

    y = start_y

    # 등급 배지 (중앙)
    badge_bbox = draw.textbbox((0, 0), badge_text, font=font_small)
    badge_w = badge_bbox[2] - badge_bbox[0]
    badge_x = (THUMB_WIDTH - badge_w - 16) // 2
    draw.rounded_rectangle(
        [badge_x, y, badge_x + badge_w + 16, y + badge_h],
        radius=6,
        fill=(255, 255, 255, 200),
    )
    draw.text((badge_x + 8, y + 5), badge_text, fill=(*color, 255), font=font_small)
    y += badge_h + gap

    # 지역명 (중앙, 큰 글자)
    loc_bbox = draw.textbbox((0, 0), title_location, font=font_large)
    loc_w = loc_bbox[2] - loc_bbox[0]
    draw.text(((THUMB_WIDTH - loc_w) // 2, y), title_location, fill=(255, 255, 255, 255), font=font_large)
    y += location_h + gap

    # 고시유형 (중앙)
    type_text = f"{notice_type} 결정고시"
    type_bbox = draw.textbbox((0, 0), type_text, font=font_medium)
    type_w = type_bbox[2] - type_bbox[0]
    draw.text(((THUMB_WIDTH - type_w) // 2, y), type_text, fill=(255, 255, 255, 220), font=font_medium)
    y += type_h + gap

    # 고시 제목 (중앙, 여러 줄)
    for line in title_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_medium)
        line_w = line_bbox[2] - line_bbox[0]
        draw.text(((THUMB_WIDTH - line_w) // 2, y), line, fill=(255, 255, 255, 200), font=font_medium)
        y += 34

    y += gap

    # 날짜 (중앙)
    date_bbox = draw.textbbox((0, 0), date, font=font_small)
    date_w = date_bbox[2] - date_bbox[0]
    draw.text(((THUMB_WIDTH - date_w) // 2, y), date, fill=(255, 255, 255, 180), font=font_small)

    # 출처 (하단 중앙)
    src = "서울도시공간포털"
    src_bbox = draw.textbbox((0, 0), src, font=font_small)
    src_w = src_bbox[2] - src_bbox[0]
    draw.text(((THUMB_WIDTH - src_w) // 2, THUMB_HEIGHT - 40), src, fill=(255, 255, 255, 120), font=font_small)


def _wrap_text(text: str, font, max_width: int, max_lines: int = 3) -> list[str]:
    """텍스트를 max_width에 맞게 줄바꿈. 최대 max_lines줄."""
    lines = []
    current = ""
    for char in text:
        test = current + char
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] > max_width:
            lines.append(current)
            current = char
            if len(lines) >= max_lines - 1:
                break
        else:
            current = test

    if current:
        if len(lines) >= max_lines:
            lines[-1] = lines[-1][:-3] + "..."
        else:
            lines.append(current)
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                lines[-1] = lines[-1][:-3] + "..."

    return lines


def _get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """시스템 한글 폰트 로드."""
    font_paths = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()
