from fastapi import APIRouter, status, Depends, HTTPException
# from ..dependencies import get_token_header
from sqlalchemy.orm import Session
import schemas
import models
import database
from repository import blog
import oauth2


router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db


@router.get("/")
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


@router.get("/{id}")
def show(id: int, db: Session = Depends(get_db)):
    return blog.show(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)
