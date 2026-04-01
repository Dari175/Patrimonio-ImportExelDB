import pandas as pd
from app.db import db

def cargar_equipo_balistico(path):

    coleccion = db["bienes_generales_equipo_balistico"]
    coleccion.drop()

    df = pd.read_excel(path, sheet_name=1, usecols="C:I", header=4)
    df = df.dropna(how="all")

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    registros = df.to_dict("records")

    if registros:
        coleccion.insert_many(registros)

    return {"insertados": len(registros)}