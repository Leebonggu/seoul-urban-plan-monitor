"""APScheduler 기반 자동 실행"""

import logging
from apscheduler.schedulers.blocking import BlockingScheduler

import config
from db import init_db
from crawler import fetch_and_save

logger = logging.getLogger(__name__)


def scheduled_job():
    logger.info("=== 스케줄 작업 시작 ===")
    result = fetch_and_save(max_pages=None)
    logger.info(
        f"완료: 총 {result['total_fetched']}건 수집, "
        f"신규 {result['new_count']}건, "
        f"업데이트 {result['updated_count']}건"
    )


def start_scheduler():
    init_db()

    scheduler = BlockingScheduler()
    scheduler.add_job(
        scheduled_job,
        "cron",
        hour=config.SCHEDULE_HOUR,
        minute=config.SCHEDULE_MINUTE,
        id="gosi_daily_fetch",
    )

    logger.info(
        f"스케줄러 시작 — 매일 {config.SCHEDULE_HOUR:02d}:{config.SCHEDULE_MINUTE:02d}에 실행"
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("스케줄러 종료")
