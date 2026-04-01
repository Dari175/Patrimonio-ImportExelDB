from fastapi import APIRouter, UploadFile, File
import shutil, os
from app.utils.excel_utils import obtener_hojas

from app.services.bienes_generales.cargar_catalogo import cargar_catalogo
from app.services.bienes_generales.cargar_equipo_balistico import cargar_equipo_balistico
from app.services.bienes_generales.cargar_inmuebles import cargar_inmuebles
from app.services.bienes_generales.cargar_muebles import cargar_muebles
from app.services.bienes_generales.cargar_computo import cargar_computo
from app.services.bienes_generales.cargar_parque_vehicular import cargar_vehicular
from app.services.cargar_bienes_control import cargar_control

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def guardar_archivo(file: UploadFile):
    path = f"{UPLOAD_FOLDER}/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path


# =============================
# ENDPOINTS INDIVIDUALES
# =============================

@router.post("/catalogo")
async def catalogo(file: UploadFile = File(...)):
    return cargar_catalogo(guardar_archivo(file))


@router.post("/balistico")
async def balistico(file: UploadFile = File(...)):
    return cargar_equipo_balistico(guardar_archivo(file))


@router.post("/inmuebles")
async def inmuebles(file: UploadFile = File(...)):
    return cargar_inmuebles(guardar_archivo(file))


@router.post("/muebles")
async def muebles(file: UploadFile = File(...)):
    return cargar_muebles(guardar_archivo(file))


@router.post("/computo")
async def computo(file: UploadFile = File(...)):
    return cargar_computo(guardar_archivo(file))


@router.post("/vehicular")
async def vehicular(file: UploadFile = File(...)):
    return cargar_vehicular(guardar_archivo(file))


@router.post("/control")
async def control(file: UploadFile = File(...)):
    return cargar_control(guardar_archivo(file))


# =============================
# ENDPOINT INTELIGENTE
# =============================

@router.post("/auto")
async def importar_automatico(file: UploadFile = File(...)):
    path = guardar_archivo(file)

    print("\n==============================")
    print("🚀 INICIANDO IMPORTACIÓN")
    print("📄 Archivo:", file.filename)

    hojas = obtener_hojas(path)
    print("📑 Hojas detectadas:", hojas)

    resultados = {}

    # =========================
    # 🔥 CASO 1: CONTROL
    # =========================
    if "BIENES MENORES" in hojas:
        print("🟢 Tipo detectado: CONTROL")

        try:
            print("➡️ Iniciando CONTROL...")
            resultados["tipo"] = "control"
            resultados["control"] = cargar_control(path)
            print("✅ CONTROL terminado")

        except Exception as e:
            print("❌ ERROR EN CONTROL:", e)
            raise e

        print("🏁 FIN IMPORTACIÓN CONTROL\n")
        return resultados

    # =========================
    # 🔥 CASO 2: GENERALES
    # =========================
    print("🔵 Tipo detectado: GENERALES")
    resultados["tipo"] = "generales"

    try:
        print("➡️ Iniciando CATALOGO...")
        resultados["catalogo"] = cargar_catalogo(path)
        print("✅ CATALOGO terminado")
    except Exception as e:
        print("❌ ERROR EN CATALOGO:", e)
        raise e

    try:
        print("➡️ Iniciando BALISTICO...")
        resultados["balistico"] = cargar_equipo_balistico(path)
        print("✅ BALISTICO terminado")
    except Exception as e:
        print("❌ ERROR EN BALISTICO:", e)
        raise e

    try:
        print("➡️ Iniciando INMUEBLES...")
        resultados["inmuebles"] = cargar_inmuebles(path)
        print("✅ INMUEBLES terminado")
    except Exception as e:
        print("❌ ERROR EN INMUEBLES:", e)
        raise e

    try:
        print("➡️ Iniciando MUEBLES...")
        resultados["muebles"] = cargar_muebles(path)
        print("✅ MUEBLES terminado")
    except Exception as e:
        print("❌ ERROR EN MUEBLES:", e)
        raise e

    try:
        print("➡️ Iniciando COMPUTO...")
        resultados["computo"] = cargar_computo(path)
        print("✅ COMPUTO terminado")
    except Exception as e:
        print("❌ ERROR EN COMPUTO:", e)
        raise e

    try:
        print("➡️ Iniciando VEHICULAR...")
        resultados["vehicular"] = cargar_vehicular(path)
        print("✅ VEHICULAR terminado")
    except Exception as e:
        print("❌ ERROR EN VEHICULAR:", e)
        raise e

    print("🏁 IMPORTACIÓN COMPLETA\n")

    return resultados