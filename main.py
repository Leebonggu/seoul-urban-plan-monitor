"""CLI 엔트리포인트"""

import logging
import click

from db import init_db, get_gosi_list, get_total_count, get_stats
from crawler import fetch_and_save
from scheduler import start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@click.group()
def cli():
    """서울 도시계획 결정고시 크롤러"""
    init_db()


@cli.command()
@click.option("--max-pages", default=None, type=int, help="최대 페이지 수 제한")
def fetch(max_pages):
    """최신 고시문 데이터를 수집합니다."""
    click.echo("데이터 수집 시작...")
    result = fetch_and_save(max_pages=max_pages)
    click.echo(
        f"완료: 총 {result['total_fetched']}건 수집, "
        f"신규 {result['new_count']}건, "
        f"업데이트 {result['updated_count']}건"
    )


@cli.command("list")
@click.option("--center", default=None, help="중심지 등급 필터 (도심/광역중심/지역중심)")
@click.option("--keyword", default=None, help="제목/내용 키워드 검색")
@click.option("--limit", default=20, help="출력 건수")
@click.option("--offset", default=0, help="시작 위치")
def list_gosi(center, keyword, limit, offset):
    """저장된 고시문 목록을 조회합니다."""
    rows = get_gosi_list(limit=limit, offset=offset, center_grade=center, keyword=keyword)
    total = get_total_count(center_grade=center)

    if not rows:
        click.echo("데이터가 없습니다. 먼저 'fetch' 명령으로 데이터를 수집하세요.")
        return

    click.echo(f"\n총 {total}건 중 {len(rows)}건 표시\n")
    click.echo(f"{'고시일자':<12} {'고시기관':<10} {'위치':<20} {'중심지':<16} {'제목'}")
    click.echo("-" * 100)

    for r in rows:
        date = r["notice_date"] or ""
        organ = (r["organ_name"] or "")[:8]
        location = (r.get("location") or "")[:18]
        center_info = ""
        if r["center_grade"]:
            center_info = f"[{r['center_grade']}] {r['center_name']}"
        title = (r["title"] or "")[:40]
        click.echo(f"{date:<12} {organ:<10} {location:<20} {center_info:<16} {title}")


@cli.command()
def stats():
    """수집 통계를 보여줍니다."""
    s = get_stats()
    click.echo(f"\n=== 수집 통계 ===")
    click.echo(f"총 고시문: {s['total']}건")
    click.echo(f"최신 고시일: {s['latest_date'] or '없음'}")

    if s["by_grade"]:
        click.echo(f"\n중심지 등급별:")
        for grade, cnt in s["by_grade"].items():
            click.echo(f"  {grade}: {cnt}건")
    else:
        click.echo("\n중심지 매칭된 고시문이 없습니다.")


@cli.command()
def schedule():
    """스케줄러를 시작합니다 (매일 자동 수집)."""
    click.echo("스케줄러를 시작합니다. Ctrl+C로 종료.")
    start_scheduler()


if __name__ == "__main__":
    cli()
