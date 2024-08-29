from datetime import date
from pydantic import BaseModel


class UrlSchema(BaseModel):
    original_url: str
    short_key: str
    expiration_date: date | None
    is_active: bool

    class Config:
        orm_mode = True


class UrlStatsSchema(BaseModel):
    date: date
    access_count: int
    url_id = int

    class Config:
        orm_mode = True
