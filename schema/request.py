from pydantic import BaseModel


class CreateShortUrlRequest(BaseModel):
    original_url: str
