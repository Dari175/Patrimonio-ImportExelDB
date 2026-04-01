import pandas as pd
from app.db import db

def cargar_control(path):

    coleccion = db["bienes_control"]
    coleccion.drop()

    df = pd.read_excel(path, sheet_name="BIENES MENORES")

    df.columns = df.columns.str.strip()
    df = df.where(pd.notna(df), "")

    registros = []

    for _, row in df.iterrows():
        doc = {}
        for col in df.columns:
            doc[col] = str(row[col]).strip()
        registros.append(doc)

    if registros:
        coleccion.insert_many(registros)

    return {"insertados": len(registros)}