#!/usr/bin/env python3
"""
Initialize/migrate database schema from schema.sql
Reads DB credentials from .env and applies schema.sql
"""
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DB credentials from .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "email_system")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "changeme")
DB_PORT = os.getenv("DB_PORT", "5432")

print(f"📌 Database Configuration:")
print(f"   Host: {DB_HOST}")
print(f"   Port: {DB_PORT}")
print(f"   Database: {DB_NAME}")
print(f"   User: {DB_USER}")
print()

try:
    # Connect to database
    print("🔌 Connecting to database...")
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    print("✅ Connected!")
    
    # Read schema.sql
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    print(f"\n📄 Reading schema from: {schema_path}")
    
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Execute schema
    print("\n⏳ Applying schema...")
    cur = conn.cursor()
    cur.execute(schema_sql)
    conn.commit()
    cur.close()
    
    print("✅ Schema applied successfully!")
    print("\n📊 Verifying events table...")
    
    # Verify
    cur = conn.cursor()
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'events' ORDER BY ordinal_position;")
    columns = cur.fetchall()
    
    print("\nEvents table columns:")
    for col_name, col_type in columns:
        print(f"   • {col_name}: {col_type}")
    
    cur.close()
    conn.close()
    
    print("\n✅ Database initialization complete!")
    print("🚀 You can now restart the backend and reload the frontend.")
    
except psycopg2.OperationalError as e:
    print(f"❌ Failed to connect to database:")
    print(f"   {e}")
    print(f"\n💡 Check your .env file:")
    print(f"   DB_HOST={DB_HOST}")
    print(f"   DB_PORT={DB_PORT}")
    print(f"   DB_NAME={DB_NAME}")
    print(f"   DB_USER={DB_USER}")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
