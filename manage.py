import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import bots
from app.config import settings
from app.connections import postgres

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bots.router)


@app.on_event("startup")
def on_app_start():
    print("---- server start -----")
    postgres.connect()
    postgres.prepare()


@app.on_event("shutdown")
def on_app_shutdown():
    postgres.close()
    print("---- server shutdown -----")


if __name__ == "__main__":
    uvicorn.run(
        "manage:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        use_colors=True,
        reload=True,
    )
