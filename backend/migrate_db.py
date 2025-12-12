#!/usr/bin/env python3
"""
Migration: Add missing contact_email column to events table
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "email_system")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "changeme")
DB_PORT = os.getenv("DB_PORT", "5432")

print(f"🔧 Database Migration: Add contact_email to events table")
print(f"📌 Connecting to {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}...")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    print("✅ Connected!\n")
    
    cur = conn.cursor()
    
    # Step 1: Add contact_email column if missing
    print("⏳ Step 1: Adding contact_email column to events table...")
    try:
        cur.execute("""
            ALTER TABLE events
            ADD COLUMN contact_email VARCHAR(255);
        """)
        print("   ✅ Column added")
    except psycopg2.errors.DuplicateColumn:
        print("   ℹ️  Column already exists")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # Step 2: Add index on contact_email
    print("\n⏳ Step 2: Creating index on contact_email...")
    try:
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_contact_email
            ON events(contact_email);
        """)
        print("   ✅ Index created")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # Step 3: Add foreign key constraint (optional, will fail if contacts don't exist)
    print("\n⏳ Step 3: Adding foreign key constraint...")
    try:
        cur.execute("""
            ALTER TABLE events
            ADD CONSTRAINT events_contact_email_fkey
            FOREIGN KEY (contact_email)
            REFERENCES contacts(email)
            ON DELETE CASCADE;
        """)
        print("   ✅ Foreign key added")
    except Exception as e:
        print(f"   ⚠️  Foreign key not added: {e}")
    
    conn.commit()
    cur.close()
    
    # Verify
    print("\n✅ Verifying changes...")
    cur = conn.cursor()
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'events'
        ORDER BY ordinal_position;
    """)
    columns = cur.fetchall()
    
    print("\nEvents table columns:")
    for col_name, col_type in columns:
        status = "✓" if col_name == "contact_email" else " "
        print(f"   [{status}] {col_name}: {col_type}")
    
    cur.close()
    conn.close()
    
    print("\n🎉 Migration complete!")
    print("📝 Next steps:")
    print("   1. Restart the backend (Ctrl+C and rerun python main.py)")
    print("   2. Reload the frontend (http://localhost:5173)")
    print("   3. Dashboard stats should now load without 500 errors\n")
    
except psycopg2.OperationalError as e:
    print(f"❌ Database connection failed: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Migration failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
