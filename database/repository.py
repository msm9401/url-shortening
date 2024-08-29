from datetime import date
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Url, UrlStats


class UrlRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_url_by_original_url(self, original_url: str) -> Url | None:
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


class UrlStatsRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_today_url_stats(self, url_id: int) -> UrlStats | None:
        return self.session.scalar(
            select(UrlStats).where(
                UrlStats.date == date.today(), UrlStats.url_id == url_id
            )
        )

    def get_url_stats_of_specific_day(self, date: date, url_id: int) -> UrlStats | None:
        return self.session.scalar(
            select(UrlStats).where(UrlStats.date == date, UrlStats.url_id == url_id)
        )

    def save_url_stats(self, url_stats: UrlStats) -> UrlStats:
        self.session.add(instance=url_stats)
        self.session.commit()  # db save
        self.session.refresh(instance=url_stats)
        return url_stats

    def update_url_stats(self, url_stats: UrlStats) -> UrlStats:
        self.session.add(instance=url_stats)
        self.session.commit()  # db save
        self.session.refresh(instance=url_stats)
        return url_stats
