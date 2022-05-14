from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    blog = models.Blog(title=request.title,
                       body=request.body, user_id=request.user_id)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def show(id: int, db: Session()):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with if {id} is not available.")
    return blog


def update(id: int, request: schemas.Blog, db: Session()):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with if {id} is not available.")
    blog.update({'title': request.title, 'body': request.body})

    db.commit()
    return f"Blog with id {id} updated."


def destroy(id: int, db: Session()):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with if {id} is not available.")

    blog.delete(synchronize_session=False)
    db.commit()
    return f"Blog with id {id} deleted."
