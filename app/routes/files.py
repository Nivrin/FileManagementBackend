from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import conint

from app.database.database import get_db
from app.models.file import File
from app.schemas.file import FileCreate, FileResponse

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/CreateFile/", response_model=FileResponse, description="Create file.")
def create_file(file: FileCreate, db: Session = Depends(get_db)):
    existing_file = db.query(File).filter(File.name is file.name).first()

    if existing_file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File already exists")

    db_file = File(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return file


@router.get("/GetAllFiles/", response_model=List[FileResponse], description="Get all files.")
def get_files(db: Session = Depends(get_db)):
    files = db.query(File).all()
    return files


@router.get("/TopSharedFiles/", response_model=List[FileResponse], description="Get top shared files.")
def get_top_shared_files(K: int = 1 , db: Session = Depends(get_db)):
    files = db.query(File).all()
    sorted_files = sorted(files, key=lambda x: len(x.users), reverse=True)
    top_files = sorted_files[:K]
    top_files_response = [FileResponse(name=file.name, risk=file.risk, users=file.users) for file in top_files]

    return top_files_response



@router.get("/GetFileByID/", response_model=FileResponse, description="get file by id.")
def get_file_by_id(file_id: conint(ge=1, le=100), db: Session = Depends(get_db)):
    file = db.query(File).filter(File.id == file_id).first()

    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File not found")

    return file


@router.get("/GetFileByName/", response_model=FileResponse, description="get file by name.")
def get_file_by_name(file_name: int, db: Session = Depends(get_db)):
    file = db.query(File).filter(File.name == file_name).first()

    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File not found")

    return file
