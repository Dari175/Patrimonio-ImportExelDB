import pandas as pd
from app.db import db

def cargar_catalogo(path):

    coleccion = db["bienes_generales_catalogo"]
    coleccion.drop()

    df = pd.read_excel(
        path,
        sheet_name=0,
        usecols="C:F",
        header=4
    )

    df = df.dropna(how="all")

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()

    df = df.where(pd.notnull(df), None)

    documentos = []

    for _, row in df.iterrows():

        doc = {
            "SUBCUENTAS ARMONIZADAS PARA DAR CUMPLIMIENTO CON LA LEY DE CONTABILIDAD": {
                "clave": row[df.columns[0]],
                "descripcion": row[df.columns[1]]
            },
            "CLASIFICADOR POR OBJETO DE GASTO": {
                "codigo": row[df.columns[2]],
                "descripcion": row[df.columns[3]]
            }
        }

        documentos.append(doc)

    if documentos:
        coleccion.insert_many(documentos)

    return {"insertados": len(documentos)}