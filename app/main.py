from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.importador_routes import router

app = FastAPI()

# 🔥 CORS abierto (para pruebas / Figma / frontend externo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ en producción mejor restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raíz
@app.get("/")
def root():
    return {"status": "API funcionando"}

#  Endpoint health (para Render / monitoreo)
@app.get("/health")
def health():
    return {"status": "ok"}

# importar bd
app.include_router(router, prefix="/importar")