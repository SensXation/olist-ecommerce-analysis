import toml
from sqlalchemy import create_engine, text

# 1. LOAD SECRETS
try:
    secrets = toml.load(".streamlit/secrets.toml")
    DB_URL = secrets["database"]["url"]
except Exception as e:
    print(f"❌ Error loading secrets: {e}")
    exit()

# 2. CONNECT TO DB
engine = create_engine(DB_URL)

# 3. READ THE SQL FILE
print("📂 Reading SQL script...")
with open("warehouse.sql", "r") as file:
    sql_script = file.read()

# 4. EXECUTE THE SCRIPT
print("⏳ Running ELT Transformation (Creating 'analytics_orders')...")
try:
    with engine.connect() as conn:
        # We use text() to safely execute the raw SQL
        conn.execute(text(sql_script))
        conn.commit() # Important! Saves the changes.
    print("✅ Success! The 'analytics_orders' table has been created in Supabase.")
except Exception as e:
    print(f"❌ SQL Error: {e}")