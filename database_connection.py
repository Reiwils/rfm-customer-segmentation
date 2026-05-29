import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Memuat (load) variabel dari file .env
load_dotenv()

def get_connection():
    """
    Fungsi untuk membuat koneksi ke database MySQL menggunakan variabel lingkungan (.env).
    """
    # Mengambil nilai kredensial secara aman
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    # Merangkai connection string secara dinamis
    connection_string = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    
    engine = create_engine(connection_string)
    return engine

def fetch_rfm_data():
    engine = get_connection()
    
    query = """
    WITH reference_date AS (
        SELECT MAX(InvoiceDate) AS max_date FROM retail_transactions
    )
    SELECT 
        CustomerID,
        DATEDIFF((SELECT max_date FROM reference_date), MAX(InvoiceDate)) AS Recency,
        COUNT(DISTINCT InvoiceNo) AS Frequency,
        SUM(Quantity * UnitPrice) AS Monetary
    FROM retail_transactions
    WHERE CustomerID IS NOT NULL 
      AND Quantity > 0      
      AND UnitPrice > 0     
    GROUP BY CustomerID;
    """
    
    df_rfm = pd.read_sql_query(query, engine)
    return df_rfm

if __name__ == "__main__":
    print("Mencoba koneksi ke database secara aman...")
    data = fetch_rfm_data()
    print("Berhasil! Berikut sampel datanya:")
    print(data.head())