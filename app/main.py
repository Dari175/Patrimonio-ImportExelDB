from fastapi import FastAPI
from app.routes.importador_routes import router

app = FastAPI()

app.include_router(router, prefix="/importar")