from fastapi import FastAPI

from .routes.house import router as Router

db_name = "591"
collection_name = "item_detail"

app = FastAPI()

app.include_router(Router, tags=["House"], prefix="/house")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
