
import pandas as pd
from database import query

def tax_export():
    data = query("""
    SELECT
    t.date,
    p.name property,
    u.name unit,
    t.type,
    t.category,
    t.amount,
    t.notes
    FROM transactions t
    LEFT JOIN properties p ON p.id=t.property_id
    LEFT JOIN units u ON u.id=t.unit_id
    ORDER BY date
    """)

    df = pd.DataFrame([dict(x) for x in data])
    file = "tax_export.csv"
    df.to_csv(file,index=False)
    return file
