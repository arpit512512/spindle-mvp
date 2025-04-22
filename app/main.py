from fastapi import FastAPI
from app.routers import concept_map
from app.core.templates import templates

app = FastAPI()
app.include_router(concept_map.router)
