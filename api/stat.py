from datetime import date
from fastapi import APIRouter, Depends, HTTPException

from database.orm import Url, UrlStats
from database.repository import UrlRepository, UrlStatsRepository
from schema.response import UrlStatsSchema


router = APIRouter(prefix="/stats")


@router.get("/{short_key}", status_code=200)
def get_stat_handlers(
    short_key: str,
    date: date,
    url_repo: UrlRepository = Depends(),
    url_stats_repo: UrlStatsRepository = Depends(),
) -> UrlStatsSchema:
    url: Url | None = url_repo.get_url_by_short_key(short_key=short_key)
    if not url:
        raise HTTPException(status_code=404, detail="URL Not Found")

    url_stats: UrlStats | None = url_stats_repo.get_url_stats_of_specific_day(
        date=date, url_id=url.id
    )
    if not url_stats:
        raise HTTPException(status_code=404, detail="There are no views for that date")

    return UrlStatsSchema.from_orm(url_stats)
