from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from hashing import Hash


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def create(request: schemas.User, db: Session):
    user = models.User(name=request.name, email=request.email,
                       password=Hash.bcrypt(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def show(id: int, db: Session()):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with if {id} is not available.")
    return user


def update(id: int, request: schemas.User, db: Session()):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with if {id} is not available.")
    user.update({'title': request.title, 'body': request.body})

    db.commit()
    return f"User with id {id} updated."


def destroy(id: int, db: Session()):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with if {id} is not available.")

    user.delete(synchronize_session=False)
    db.commit()
    return f"User with id {id} deleted."
