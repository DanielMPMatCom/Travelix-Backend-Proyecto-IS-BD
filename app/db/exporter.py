import pandas as pd
from sqlalchemy.orm import Session

def export_to_excel(session: Session, objects):
    df = pd.DataFrame()

    for obj in objects:
        data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        df = df.append(data, ignore_index=True)

    df.to_excel('output.xlsx', index=False)

