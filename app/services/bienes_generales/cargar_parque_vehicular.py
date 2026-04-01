import pandas as pd
from app.db import db

def cargar_vehicular(path):

    coleccion = db["bienes_generales_parque_vehicular"]
    coleccion.drop()

    df = pd.read_excel(path, sheet_name=5, header=2)

    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    registros = df.to_dict("records")

    if registros:
        coleccion.insert_many(registros)

    return {"insertados": len(registros)}