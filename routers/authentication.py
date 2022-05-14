from fastapi import APIRouter, status, Depends, HTTPException
# from ..dependencies import get_token_header
from sqlalchemy.orm import Session
from hashing import Hash
import schemas
import models
import database
import JWTToken

router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_200_OK)
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User detail do not match our record.")

    # if Hash.verify(user.password, request.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Incorrect password.")

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTToken.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user}
