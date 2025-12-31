# Olist E-Commerce Analysis Pipeline & Dashboard 🇧🇷

## 📌 Project Overview
This project is an end-to-end data analysis solution for the **Olist E-Commerce dataset** (100k+ orders). It involves a full data pipeline: ingesting raw CSV data using **Python**, storing it in a **PostgreSQL (Supabase)** data warehouse, and visualizing key business metrics via **Google Looker Studio**.

## 🔗 Project Links
* 📊 **[Interact with Live Dashboard](https://lookerstudio.google.com/reporting/ea938543-1b4f-4eb3-9b82-caf03a2c7614)**
* 📄 **[View Full PDF Report](https://github.com/SensXation/olist-ecommerce-analysis/raw/main/dashboard_report.pdf)**
* 🗄️ **[Data Source (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**

## 🛠 Tech Stack
* **Python:** Data Extraction, Transformation, and Loading (ETL).
    * *Libraries:* `pandas`, `psycopg2`, `sqlalchemy`, `streamlit`.
* **SQL (PostgreSQL):** Complex data joining and aggregation.
* **Supabase:** Cloud-hosted Postgres database.
* **Google Looker Studio:** Interactive dashboard for final business reporting.

## 📂 Project Structure
* `upload_to_db.py`: Python script that reads raw CSVs, cleans data types, and uploads to Supabase.
* `warehouse.sql`: SQL scripts defining the schema and joins for the data warehouse.
* `dashboard.py`: Streamlit application for database connection testing.
* `requirements.txt`: List of Python dependencies.

## 📊 Key Insights
* **Total Revenue:** Generated **R$ 15.4M** in sales over the analyzed period (2016-2018).
* **Top Categories:** **"Bed, Bath & Table"** and **"Health & Beauty"** are the consistent market leaders.
* **Sales Trend:** Identified a massive growth spike in **late 2017**, correlating with Black Friday seasonality.

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/SensXation/olist-ecommerce-dashboard.git](https://github.com/SensXation/olist-ecommerce-dashboard.git)
cd olist-ecommerce-dashboard
