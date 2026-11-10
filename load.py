import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text

# 1. Στοιχεία βάσης από το .env
load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db = os.getenv("POSTGRES_DB")

# 2. Σύνδεση με τη βάση
url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(url)

# 3. Διάβασε τα καθαρά δεδομένα
df = pd.read_csv("data/sales_clean.csv")
print(f"Διαβάστηκαν {len(df)} γραμμές από το CSV")

with engine.begin() as conn:
    conn.execute(text("truncate table sales"))

# 4. Γράψε στη βάση
df.to_sql("sales", engine, if_exists="append", index=False)
print("Φορτώθηκαν στον πίνακα sales ✅")