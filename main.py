from fastapi import FastAPI, status, Response, Depends, HTTPException
from database import Base, engine
from routers import blogs, users, authentication


app = FastAPI()

Base.metadata.create_all(engine)
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(blogs.router)
