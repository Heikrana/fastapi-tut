from fastapi import FastAPI

import TodoApp.models as models
from TodoApp.database import engine
from TodoApp.routers import auth, todos

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)

models.Base.metadata.create_all(bind=engine)
