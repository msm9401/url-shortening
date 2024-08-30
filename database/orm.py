from datetime import date
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()


class Url(Base):
    __tablename__ = "url"

    id = Column(BigInteger, primary_key=True, autoincrement=False, index=True)
    original_url = Column(String, nullable=False, index=True)
    short_key = Column(String(256), unique=True, nullable=False, index=True)
    expiration_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    stats = relationship("UrlStats", lazy="joined")

    @classmethod
    def create(
        cls,
        id: int,
        original_url: str,
        short_key: str,
        expiration_date: date | None = None,
    ) -> "Url":
        return cls(
            id=id,
            original_url=original_url,
            short_key=short_key,
            expiration_date=expiration_date,
        )

    def inactive(self) -> "Url":
        self.is_active = False
        return self


class UrlStats(Base):
    __tablename__ = "url_stats"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    access_count = Column(Integer, default=0, nullable=False)
    url_id = Column(BigInteger, ForeignKey("url.id"), nullable=False)

    @classmethod
    def create(cls, date: str, access_count: int, url_id: int) -> "UrlStats":
        return cls(date=date, access_count=access_count, url_id=url_id)

    def increase_access_count(self) -> "UrlStats":
        self.access_count += 1
        return self
