from fastapi import FastAPI
from app.api.v1.items import router as items_router

app = FastAPI(title="My API")

# Register router
app.include_router(items_router)
