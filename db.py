"""SQLite DB 초기화 및 CRUD"""

import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gosi (
            notice_code TEXT PRIMARY KEY,
            notice_no TEXT,
            notice_date TEXT,
            title TEXT,
            content TEXT,
            organ_code TEXT,
            organ_name TEXT,
            notice_type TEXT,
            classify_g TEXT,
            classify_m TEXT,
            site_code TEXT,
            site_name TEXT,
            location TEXT,
            doc_url TEXT,
            page_url TEXT,
            center_grade TEXT,
            center_name TEXT,
            fetched_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_gosi_notice_date
        ON gosi(notice_date DESC)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_gosi_center_grade
        ON gosi(center_grade)
    """)
    conn.commit()
    conn.close()


def upsert_gosi(record: dict) -> bool:
    """고시문 저장 (UPSERT). 새로 삽입되면 True, 이미 존재하면 False."""
    conn = get_connection()
    cursor = conn.execute("SELECT 1 FROM gosi WHERE notice_code = ?", (record["notice_code"],))
    exists = cursor.fetchone() is not None

    conn.execute("""
        INSERT INTO gosi (
            notice_code, notice_no, notice_date, title, content,
            organ_code, organ_name, notice_type,
            classify_g, classify_m,
            site_code, site_name, location,
            doc_url, page_url,
            center_grade, center_name, fetched_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(notice_code) DO UPDATE SET
            title = excluded.title,
            content = excluded.content,
            notice_type = excluded.notice_type,
            classify_g = excluded.classify_g,
            classify_m = excluded.classify_m,
            location = excluded.location,
            doc_url = excluded.doc_url,
            page_url = excluded.page_url,
            center_grade = excluded.center_grade,
            center_name = excluded.center_name,
            fetched_at = excluded.fetched_at
    """, (
        record["notice_code"],
        record["notice_no"],
        record["notice_date"],
        record["title"],
        record["content"],
        record["organ_code"],
        record["organ_name"],
        record["notice_type"],
        record["classify_g"],
        record["classify_m"],
        record["site_code"],
        record["site_name"],
        record["location"],
        record["doc_url"],
        record["page_url"],
        record["center_grade"],
        record["center_name"],
        record["fetched_at"],
    ))
    conn.commit()
    conn.close()
    return not exists


def get_gosi_list(
    limit: int = 20,
    offset: int = 0,
    center_grade: str | None = None,
    keyword: str | None = None,
) -> list[dict]:
    conn = get_connection()
    query = "SELECT * FROM gosi WHERE 1=1"
    params = []

    if center_grade:
        query += " AND center_grade = ?"
        params.append(center_grade)
    if keyword:
        query += " AND (title LIKE ? OR content LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])

    query += " ORDER BY notice_date DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_total_count(center_grade: str | None = None) -> int:
    conn = get_connection()
    query = "SELECT COUNT(*) FROM gosi WHERE 1=1"
    params = []
    if center_grade:
        query += " AND center_grade = ?"
        params.append(center_grade)
    count = conn.execute(query, params).fetchone()[0]
    conn.close()
    return count


def get_stats() -> dict:
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM gosi").fetchone()[0]
    by_grade = conn.execute("""
        SELECT center_grade, COUNT(*) as cnt
        FROM gosi
        WHERE center_grade IS NOT NULL
        GROUP BY center_grade
        ORDER BY cnt DESC
    """).fetchall()
    latest = conn.execute(
        "SELECT notice_date FROM gosi ORDER BY notice_date DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return {
        "total": total,
        "by_grade": {r["center_grade"]: r["cnt"] for r in by_grade},
        "latest_date": latest["notice_date"] if latest else None,
    }
