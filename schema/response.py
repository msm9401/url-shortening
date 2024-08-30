from datetime import date
from typing import List

from pydantic import BaseModel


class UrlSchema(BaseModel):
    original_url: str
    short_key: str
    expiration_date: date | None
    is_active: bool

    class Config:
        orm_mode = True


class UrlStatsSchema(BaseModel):
    id: int
    date: date | None
    access_count: int

    class Config:
        orm_mode = True


class UrlStatsListSchema(BaseModel):
    stats: List[UrlStatsSchema]
    total_view: int
