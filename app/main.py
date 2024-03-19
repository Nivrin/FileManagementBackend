import logging
import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.database.database import create_database
from app.routes import files, groups, users
from app.utils.logger import setup_logging
from app.config.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB



print(POSTGRES_USER)
print(POSTGRES_PASSWORD)
print(POSTGRES_HOST)
print(POSTGRES_PORT)
print(POSTGRES_DB)
app = FastAPI()

setup_logging()

logging.info('Application started')

LOG_FILE_PATH = "./logs/app.log"

create_database()


app.include_router(files.router)
app.include_router(users.router)
app.include_router(groups.router)


@app.get("/")
async def health_check():
    return {"status": "UP"}


@app.get("/logs")
async def get_logs():
    if not os.path.exists(LOG_FILE_PATH):
        raise HTTPException(status_code=404, detail="Log file not found")

    return FileResponse(LOG_FILE_PATH)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
    