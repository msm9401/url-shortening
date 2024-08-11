from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from database.orm import Url
from database.repository import UrlRepository
from schema.request import CreateShortUrlRequest
from schema.response import RedirectUrlSchema, UrlSchema
from service.url import UrlService


router = APIRouter()


@router.get("/{short_key}", status_code=301)
def get_original_url_handler(
    short_key: str,
    url_repo: UrlRepository = Depends(),
):
    original_url: Url | None = url_repo.get_original_url_by_short_key(
        short_key=short_key
    )
    if not original_url:
        raise HTTPException(status_code=404, detail="URL Not Found")

    return RedirectUrlSchema.from_orm(original_url)
    # return RedirectResponse(url=original_url)


@router.post("/shorten", status_code=201)
def create_short_key_handler(
    request: CreateShortUrlRequest,
    expiration_date: date | None = None,
    url_service: UrlService = Depends(),
    url_repo: UrlRepository = Depends(),
):
    original_url: Url | None = url_repo.get_key_by_original_url(
        original_url=request.original_url
    )
    if original_url:
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
