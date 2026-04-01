import pandas as pd

def obtener_hojas(path):
    xls = pd.ExcelFile(path)
    return xls.sheet_names