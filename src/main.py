from fastapi import FastAPI

from api import api_roter

app = FastAPI()

app.include_router(api_roter)


def main():
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
