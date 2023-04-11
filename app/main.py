from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers.addresses import addresses_router
from app.utils import models
from app.utils.database_config import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Address Book')

# including the addresses router
app.include_router(addresses_router)

add_pagination(app)


# root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}


# health endpoint
@app.get("/health")
async def health():
    return {"message": "OK"}
