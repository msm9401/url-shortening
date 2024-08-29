from fastapi import FastAPI

from api import stat, url

app = FastAPI()
app.include_router(url.router)
app.include_router(stat.router)


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}
