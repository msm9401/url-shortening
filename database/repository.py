from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Url


class UrlRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_key_by_original_url(self, original_url: str) -> Url | None:
        return self.session.scalar(select(Url).where(Url.original_url == original_url))

    def get_url_by_short_key(self, short_key: str) -> Url | None:
        return self.session.scalar(select(Url).where(Url.short_key == short_key))

    def save_url(self, url: Url) -> Url:
        self.session.add(instance=url)
        self.session.commit()  # db save
        self.session.refresh(instance=url)
        return url

    def update_url(self, url: Url) -> Url:
        self.session.add(instance=url)
        self.session.commit()  # db save
        self.session.refresh(instance=url)
        return url
