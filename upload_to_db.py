import pandas as pd
from sqlalchemy import create_engine
import os
import toml 

# 1.SECURE CONFIGURATION
try:
    # Load secrets 
    secrets = toml.load(".streamlit/secrets.toml")
    DB_URL = secrets["database"]["url"]
except FileNotFoundError:
    print("❌ Error: .streamlit/secrets.toml not found!")
    exit()
except KeyError:
    print("❌ Error: 'url' not found under [database] in secrets.toml")
    exit()

# Create the connection engine
engine = create_engine(DB_URL)

#2. AUTOMATIC UPLOADER 
data_folder = "data"

# List of files we want to upload and the table name.
files_to_tables = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_translations" 
}

print("🚀 Starting Data Ingestion to Supabase...")

for file_name, table_name in files_to_tables.items():
    file_path = os.path.join(data_folder, file_name)
    
    if os.path.exists(file_path):
        print(f"   ⏳ Processing {table_name}...")
        
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Upload to SQL
        try:
            # chunksize=1000 helps prevent timeouts with large files
            df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=1000)
            print(f"   ✅ Uploaded {len(df)} rows to table '{table_name}'")
        except Exception as e:
            print(f"   ❌ Error uploading {table_name}: {e}")
    else:
        print(f"   ⚠️ File not found: {file_name}")

print("🎉 All done! Your Data Warehouse is ready.")