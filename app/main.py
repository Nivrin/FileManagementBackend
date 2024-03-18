import logging
import uvicorn
from fastapi import FastAPI

from app.database.database import create_database
from app.routes import files,groups,users
from app.utils.logger import setup_logging

app = FastAPI()

setup_logging()

logging.info('Application started')

create_database()


app.include_router(files.router)
app.include_router(users.router)
app.include_router(groups.router)


@app.get("/")
async def health_check():
    return {"status": "UP"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)