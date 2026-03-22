"""서울 도시계획 결정고시 대시보드"""

import json
import os
from datetime import datetime, timedelta

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import folium
from streamlit_folium import st_folium
from centers import get_all_centers_with_coords

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# ─── 데이터 로딩 ───


@st.cache_data(ttl=300)
def load_all_data() -> pd.DataFrame:
    records = []
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".json") or fname == "latest.json":
            continue
        with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
            records.extend(json.load(f))

    df = pd.DataFrame(records)
    df["notice_date"] = pd.to_datetime(df["notice_date"], errors="coerce")
    df = df.dropna(subset=["notice_date"])
    df = df.sort_values("notice_date", ascending=False)
    return df


# ─── 페이지 설정 ───

st.set_page_config(
    page_title="서울 결정고시 모니터",
    page_icon="🏙️",
    layout="wide",
)

st.title("서울 도시계획 결정고시 모니터")
st.caption("2040 서울플랜 중심지체계 기반 분석 · urban.seoul.go.kr 데이터")

df = load_all_data()

# ─── 사이드바 필터 ───

with st.sidebar:
    st.header("필터")

    # 기간
    min_date = df["notice_date"].min().date()
    max_date = df["notice_date"].max().date()
    date_range = st.date_input(
        "기간",
        value=(max_date - timedelta(days=90), max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # 중심지 등급
    grade_options = ["전체", "도심", "광역중심", "지역중심", "미매칭"]
    selected_grade = st.selectbox("중심지 등급", grade_options)

    # 고시기관
    organs = ["전체"] + sorted(df["organ_name"].dropna().unique().tolist())
    selected_organ = st.selectbox("고시기관", organs)

    # 키워드
    keyword = st.text_input("키워드 검색", placeholder="재개발, 용적률, 지구단위...")

# ─── 필터 적용 ───

filtered = df.copy()

if len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["notice_date"].dt.date >= start)
        & (filtered["notice_date"].dt.date <= end)
    ]

if selected_grade != "전체":
    if selected_grade == "미매칭":
        filtered = filtered[filtered["center_grade"].isna() | (filtered["center_grade"] == "")]
    else:
        filtered = filtered[filtered["center_grade"] == selected_grade]

if selected_organ != "전체":
    filtered = filtered[filtered["organ_name"] == selected_organ]

if keyword:
    mask = (
        filtered["title"].str.contains(keyword, case=False, na=False)
        | filtered["content"].str.contains(keyword, case=False, na=False)
    )
    filtered = filtered[mask]

# ─── 상단 지표 ───

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("총 고시문", f"{len(filtered):,}건")
with col2:
    center_matched = filtered[filtered["center_grade"].notna() & (filtered["center_grade"] != "")]
    st.metric("중심지 매칭", f"{len(center_matched):,}건")
with col3:
    if not filtered.empty:
        st.metric("최신 고시일", filtered["notice_date"].max().strftime("%Y-%m-%d"))
    else:
        st.metric("최신 고시일", "-")
with col4:
    if len(date_range) == 2:
        days = (date_range[1] - date_range[0]).days or 1
        st.metric("일 평균", f"{len(filtered) / days:.1f}건")

st.divider()

# ─── 메인: 지도 + 최신 목록 ───

map_col, list_col = st.columns([1, 1])

with map_col:
    st.subheader("중심지 현황")

    centers = get_all_centers_with_coords()

    # 각 중심지의 고시문 수 계산
    center_count_map = {}
    for _, row in filtered.iterrows():
        cn = row.get("center_name")
        if cn and cn != "":
            center_count_map[cn] = center_count_map.get(cn, 0) + 1

    grade_colors = {
        "도심": "#e74c3c",
        "광역중심": "#3498db",
        "지역중심": "#f39c12",
    }

    m = folium.Map(
        location=[37.5665, 126.9780],
        zoom_start=11,
        tiles="CartoDB positron",
    )

    for c in centers:
        count = center_count_map.get(c["name"], 0)
        color = grade_colors.get(c["grade"], "#999")
        radius = max(8, min(30, count * 1.5))

        folium.CircleMarker(
            location=[c["lat"], c["lng"]],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>{c['name']}</b><br>"
                f"등급: {c['grade']}<br>"
                f"고시문: {count}건",
                max_width=200,
            ),
            tooltip=f"{c['name']} ({count}건)",
        ).add_to(m)

    st_folium(m, use_container_width=True, height=480)

    st.markdown(
        """
        <div style="display:flex; gap:20px; margin-top:4px; font-size:0.85em;">
            <span><span style="color:#e74c3c;">●</span> 도심</span>
            <span><span style="color:#3498db;">●</span> 광역중심</span>
            <span><span style="color:#f39c12;">●</span> 지역중심</span>
            <span style="color:#888;">원 크기 = 고시문 수</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with list_col:
    st.subheader("최신 고시문")

    if filtered.empty:
        st.info("조건에 맞는 고시문이 없습니다.")
    else:
        # 최신 20건을 카드 형태로 표시
        for _, row in filtered.head(20).iterrows():
            date_str = row["notice_date"].strftime("%Y-%m-%d")
            organ = row.get("organ_name", "")
            location = row.get("location", "")
            title = row.get("title", "")
            center_grade = row.get("center_grade", "")
            center_name = row.get("center_name", "")
            page_url = row.get("page_url", "")
            doc_url = row.get("doc_url", "")

            # 태그
            tags = f"`{date_str}`"
            if center_grade and center_grade != "":
                tag_colors = {"도심": "red", "광역중심": "blue", "지역중심": "orange"}
                tags += f" :{'red' if center_grade == '도심' else 'blue' if center_grade == '광역중심' else 'orange'}[{center_grade}·{center_name}]"

            # 링크
            links = ""
            if page_url:
                links += f" [상세]({page_url})"
            if doc_url:
                links += f" · [원문]({doc_url})"

            location_text = f" · 📍 {location}" if location else ""

            st.markdown(
                f"**{title[:60]}{'...' if len(title) > 60 else ''}**\n\n"
                f"{tags} · {organ}{location_text}{links}",
            )
            st.divider()

        if len(filtered) > 20:
            st.caption(f"외 {len(filtered) - 20:,}건 더 있음")

# ─── 하단: 상세 분석 ───

st.divider()

tab1, tab2, tab3 = st.tabs(["📋 전체 목록", "📊 추이/분석", "🗺️ 중심지 상세"])

with tab1:
    if filtered.empty:
        st.info("조건에 맞는 고시문이 없습니다.")
    else:
        display_df = filtered[
            ["notice_date", "organ_name", "location", "center_grade", "center_name", "title", "notice_type", "page_url", "doc_url"]
        ].copy()
        display_df["notice_date"] = display_df["notice_date"].dt.strftime("%Y-%m-%d")
        display_df = display_df.rename(columns={
            "notice_date": "고시일",
            "organ_name": "기관",
            "location": "위치",
            "center_grade": "등급",
            "center_name": "중심지",
            "title": "제목",
            "notice_type": "유형",
            "page_url": "상세",
            "doc_url": "원문",
        })

        st.dataframe(
            display_df,
            use_container_width=True,
            height=500,
            column_config={
                "상세": st.column_config.LinkColumn("상세", display_text="보기"),
                "원문": st.column_config.LinkColumn("원문", display_text="다운"),
            },
        )
        st.caption(f"총 {len(display_df):,}건")

with tab2:
    if not filtered.empty:
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            # 월별 추이
            monthly = filtered.copy()
            monthly["month"] = monthly["notice_date"].dt.to_period("M").astype(str)
            monthly_counts = monthly.groupby("month").size().reset_index(name="건수")

            fig = px.bar(
                monthly_counts,
                x="month",
                y="건수",
                title="월별 고시문 추이",
                labels={"month": "월", "건수": "건수"},
            )
            fig.update_layout(xaxis_tickangle=-45, height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col_chart2:
            # 고시유형별 분포
            if "notice_type" in filtered.columns:
                type_counts = filtered["notice_type"].value_counts().head(10).reset_index()
                type_counts.columns = ["유형", "건수"]
                fig2 = px.pie(
                    type_counts,
                    values="건수",
                    names="유형",
                    title="고시유형 분포",
                )
                fig2.update_layout(height=350)
                st.plotly_chart(fig2, use_container_width=True)

with tab3:
    if not filtered.empty:
        col_a, col_b = st.columns(2)

        with col_a:
            grade_counts = filtered.copy()
            grade_counts["center_grade"] = grade_counts["center_grade"].fillna("미매칭").replace("", "미매칭")
            grade_summary = grade_counts["center_grade"].value_counts().reset_index()
            grade_summary.columns = ["등급", "건수"]

            fig3 = px.bar(
                grade_summary,
                x="등급",
                y="건수",
                title="중심지 등급별 고시문 수",
                color="등급",
                color_discrete_map={
                    "도심": "#e74c3c",
                    "광역중심": "#3498db",
                    "지역중심": "#f39c12",
                    "미매칭": "#bdc3c7",
                },
            )
            fig3.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

        with col_b:
            center_detail = filtered[
                filtered["center_name"].notna() & (filtered["center_name"] != "")
            ]
            if not center_detail.empty:
                center_top = center_detail["center_name"].value_counts().head(15).reset_index()
                center_top.columns = ["중심지", "건수"]

                fig4 = px.bar(
                    center_top,
                    y="중심지",
                    x="건수",
                    title="중심지별 고시문 수 TOP 15",
                    orientation="h",
                )
                fig4.update_layout(height=350, yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig4, use_container_width=True)

        # 히트맵
        center_monthly = filtered[
            filtered["center_name"].notna() & (filtered["center_name"] != "")
        ].copy()
        if not center_monthly.empty:
            center_monthly["month"] = center_monthly["notice_date"].dt.to_period("M").astype(str)
            pivot = center_monthly.groupby(["center_name", "month"]).size().reset_index(name="건수")
            pivot_table = pivot.pivot(index="center_name", columns="month", values="건수").fillna(0)

            fig5 = px.imshow(
                pivot_table,
                title="중심지 × 월별 고시문 히트맵",
                labels=dict(x="월", y="중심지", color="건수"),
                aspect="auto",
                color_continuous_scale="YlOrRd",
            )
            fig5.update_layout(height=450)
            st.plotly_chart(fig5, use_container_width=True)
