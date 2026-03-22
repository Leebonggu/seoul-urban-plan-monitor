"""2040 서울도시기본계획 중심지체계 매핑"""

# 중심지체계: 등급 → 중심지 목록
# 각 중심지에 대해 매칭에 사용할 키워드와 좌표를 포함
CENTER_HIERARCHY = {
    "도심": [
        {"name": "한양도성(서울도심)", "keywords": ["종로", "중구", "한양도성", "광화문", "을지로", "명동", "시청"], "lat": 37.5704, "lng": 126.9922},
        {"name": "여의도·영등포", "keywords": ["여의도", "영등포"], "lat": 37.5219, "lng": 126.9245},
        {"name": "강남", "keywords": ["강남구", "강남역", "테헤란"], "lat": 37.4979, "lng": 127.0276},
    ],
    "광역중심": [
        {"name": "용산", "keywords": ["용산"], "lat": 37.5299, "lng": 126.9648},
        {"name": "청량리·왕십리", "keywords": ["청량리", "왕십리"], "lat": 37.5804, "lng": 127.0470},
        {"name": "창동·상계", "keywords": ["창동", "상계"], "lat": 37.6538, "lng": 127.0474},
        {"name": "상암·수색", "keywords": ["상암", "수색"], "lat": 37.5791, "lng": 126.8908},
        {"name": "마곡", "keywords": ["마곡"], "lat": 37.5596, "lng": 126.8260},
        {"name": "가산·대림", "keywords": ["가산", "대림"], "lat": 37.4816, "lng": 126.8826},
        {"name": "잠실", "keywords": ["잠실"], "lat": 37.5133, "lng": 127.1001},
    ],
    "지역중심": [
        {"name": "동대문", "keywords": ["동대문"], "lat": 37.5714, "lng": 127.0096},
        {"name": "망우", "keywords": ["망우"], "lat": 37.5983, "lng": 127.0920},
        {"name": "미아", "keywords": ["미아"], "lat": 37.6134, "lng": 127.0300},
        {"name": "성수", "keywords": ["성수"], "lat": 37.5445, "lng": 127.0560},
        {"name": "신촌", "keywords": ["신촌"], "lat": 37.5596, "lng": 126.9370},
        {"name": "마포", "keywords": ["마포"], "lat": 37.5539, "lng": 126.9513},
        {"name": "공덕", "keywords": ["공덕"], "lat": 37.5441, "lng": 126.9516},
        {"name": "연신내·불광", "keywords": ["연신내", "불광"], "lat": 37.6190, "lng": 126.9215},
        {"name": "목동", "keywords": ["목동"], "lat": 37.5264, "lng": 126.8750},
        {"name": "봉천", "keywords": ["봉천"], "lat": 37.4813, "lng": 126.9418},
        {"name": "사당·이수", "keywords": ["사당", "이수"], "lat": 37.4765, "lng": 126.9816},
        {"name": "수서·문정", "keywords": ["수서", "문정"], "lat": 37.4848, "lng": 127.1190},
        {"name": "천호·길동", "keywords": ["천호", "길동"], "lat": 37.5381, "lng": 127.1237},
    ],
}


def get_all_centers_with_coords() -> list[dict]:
    """모든 중심지의 이름, 등급, 좌표를 반환"""
    result = []
    for grade, centers in CENTER_HIERARCHY.items():
        for c in centers:
            result.append({
                "name": c["name"],
                "grade": grade,
                "lat": c["lat"],
                "lng": c["lng"],
            })
    return result


def match_center(text: str) -> tuple[str | None, str | None]:
    """고시문 텍스트에서 중심지체계 매칭.

    Returns:
        (등급, 중심지명) 또는 매칭 없으면 (None, None)
    """
    if not text:
        return None, None

    # 도심 → 광역중심 → 지역중심 순으로 매칭 (상위 등급 우선)
    for grade, centers in CENTER_HIERARCHY.items():
        for center in centers:
            for keyword in center["keywords"]:
                if keyword in text:
                    return grade, center["name"]

    return None, None
