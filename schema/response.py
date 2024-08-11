from pydantic import BaseModel


class UrlSchema(BaseModel):
    short_key: str

    class Config:
        orm_mode = True


class RedirectUrlSchema(BaseModel):
    original_url: str

    class Config:
        orm_mode = True
