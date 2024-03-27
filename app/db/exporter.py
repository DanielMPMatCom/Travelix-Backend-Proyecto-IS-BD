from fastapi.responses import FileResponse
from sqlalchemy import inspect
from pandas import DataFrame
import os

def export_to_excel(excel_name: str, entities):
    
    result = []

    for entity in entities:
        inspector = inspect(entity)
        data = {
            column.key: getattr(entity, column.key)
            for column in inspector.mapper.column_attrs
        }
        result.append(data)

    df = DataFrame(result)
    df.to_excel(excel_name, index=False)

    return FileResponse(
        excel_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=excel_name,
    )

    
def export_to_excel2(excel_name: str, entities):
    # Crear un DataFrame a partir de la lista de diccionarios
    df = DataFrame(entities)
    
    # Escribir el DataFrame en un archivo Excel
    df.to_excel(excel_name, index=False)

    # Retornar el archivo Excel como una respuesta HTTP
    return FileResponse(
        excel_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=excel_name,
    )