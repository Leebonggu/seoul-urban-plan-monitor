"""2040 서울도시기본계획 중심지체계 매핑"""

# 중심지체계: 등급 → 중심지 목록
# 각 중심지에 대해 매칭에 사용할 키워드를 포함
CENTER_HIERARCHY = {
    "도심": [
        {"name": "한양도성(서울도심)", "keywords": ["종로", "중구", "한양도성", "광화문", "을지로", "명동", "시청"]},
        {"name": "여의도·영등포", "keywords": ["여의도", "영등포"]},
        {"name": "강남", "keywords": ["강남구", "강남역", "테헤란"]},
    ],
    "광역중심": [
        {"name": "용산", "keywords": ["용산"]},
        {"name": "청량리·왕십리", "keywords": ["청량리", "왕십리"]},
        {"name": "창동·상계", "keywords": ["창동", "상계"]},
        {"name": "상암·수색", "keywords": ["상암", "수색"]},
        {"name": "마곡", "keywords": ["마곡"]},
        {"name": "가산·대림", "keywords": ["가산", "대림"]},
        {"name": "잠실", "keywords": ["잠실"]},
    ],
    "지역중심": [
        {"name": "동대문", "keywords": ["동대문"]},
        {"name": "망우", "keywords": ["망우"]},
        {"name": "미아", "keywords": ["미아"]},
        {"name": "성수", "keywords": ["성수"]},
        {"name": "신촌", "keywords": ["신촌"]},
        {"name": "마포", "keywords": ["마포"]},
        {"name": "공덕", "keywords": ["공덕"]},
        {"name": "연신내·불광", "keywords": ["연신내", "불광"]},
        {"name": "목동", "keywords": ["목동"]},
        {"name": "봉천", "keywords": ["봉천"]},
        {"name": "사당·이수", "keywords": ["사당", "이수"]},
        {"name": "수서·문정", "keywords": ["수서", "문정"]},
        {"name": "천호·길동", "keywords": ["천호", "길동"]},
    ],
}


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
