import logging
import os
import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.database.database import create_database
from app.routes import files, groups, users
from app.utils.logger import setup_logging

app = FastAPI()

setup_logging()

logging.info('Application started')

current_dir = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(current_dir, '..', 'logs', 'app.log')

create_database()


app.include_router(files.router)
app.include_router(users.router)
app.include_router(groups.router)


@app.get("/")
async def health_check():
    return {"status": "UP"}


@app.get("/logs")
async def get_logs():
    if not os.path.exists(log_file):
        raise HTTPException(status_code=404, detail="Log file not found")

    return FileResponse(log_file)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
