from fastapi import FastAPI

from api import url

app = FastAPI()
app.include_router(url.router)


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}
