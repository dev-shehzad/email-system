from fastapi import APIRouter, UploadFile, File
import pandas as pd
from database import get_db

router = APIRouter()

@router.post("/contacts/upload")
async def upload_contacts(file: UploadFile = File(...)):
    print(f"📤 CSV Upload Started: {file.filename}")
    
    df = pd.read_csv(file.file)
    total_rows = len(df)
    print(f"📊 CSV File Read: {total_rows} rows found")
    
    conn = get_db()
    cur = conn.cursor()

    inserted = 0
    skipped = 0

    print(f"🔄 Processing contacts...")
    for index, row in df.iterrows():
        try:
            cur.execute(
                "INSERT INTO contacts (email, name) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                (row["email"], row.get("name", None))
            )
            if cur.rowcount > 0:
                inserted += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"❌ Error inserting row {index}: {str(e)}")
            skipped += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Upload Complete!")
    print(f"   ✓ Inserted: {inserted} contacts")
    print(f"   ⚠ Skipped: {skipped} contacts (duplicates or errors)")
    print(f"   📈 Total processed: {total_rows} rows\n")

    return {"status": "uploaded", "inserted": inserted, "skipped": skipped, "total": total_rows}
