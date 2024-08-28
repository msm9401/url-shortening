from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from database.orm import Url, UrlStats
from database.repository import UrlRepository, UrlStatsRepository
from schema.request import CreateShortUrlRequest
from schema.response import UrlSchema
from service.url import UrlService


router = APIRouter()


@router.get("/{short_key}", status_code=301)
def get_original_url_handler(
    short_key: str,
    url_service: UrlService = Depends(),
    url_repo: UrlRepository = Depends(),
    url_stats_repo: UrlStatsRepository = Depends(),
):
    url: Url | None = url_repo.get_url_by_short_key(short_key=short_key)

    # 만료일과 active상태 검증
    if url.expiration_date is not None and url.is_active is True:
        is_expired: bool = url_service.is_expired(expiration_date=url.expiration_date)

        if is_expired is True:  # 만료
            url.inactive()  # soft delete
            url: Url = url_repo.update_url(url=url)
            raise HTTPException(status_code=404, detail="URL Not Found")

    if not url or url.is_active is False:
        raise HTTPException(status_code=404, detail="URL Not Found")

    url_stats: UrlStats | None = url_stats_repo.get_today_url_stats(
        date=date.today(), url_id=url.id
    )

    if url_stats is None:
        url_stats: UrlStats = UrlStats.create(
            date=date.today(), access_count=1, url_id=url.id
        )
        url_stats: UrlStats = url_stats_repo.save_url_stats(url_stats=url_stats)
    else:
        url_stats.increase_access_count()
        url_stats: UrlStats = url_stats_repo.update_url_stats(url_stats=url_stats)

    # TODO: 빠른 응답을 위한 redis 캐시

    # 응답 location 헤더에 반환
    return RedirectResponse(url.original_url, status_code=301)


@router.post("/shorten", status_code=201)
def create_short_key_handler(
    request: CreateShortUrlRequest,
    expiration_date: date | None = None,
    url_service: UrlService = Depends(),
    url_repo: UrlRepository = Depends(),
):
    url: Url | None = url_repo.get_url_by_original_url(
        original_url=request.original_url
    )
    if url:
        raise HTTPException(status_code=409, detail="This URL already exists.")

    tsid: int = url_service.tsid_generator()
    short_key: str = url_service.encode_by_base62(url_tsid=tsid)
    url: Url = Url.create(
        id=tsid,
        original_url=request.original_url,
        short_key=short_key,
        expiration_date=expiration_date,
    )
    url: Url = url_repo.save_url(url=url)

    return UrlSchema.from_orm(url)
