Claude






































Readme · MD
# Sales ETL Pipeline
 
A small end-to-end **ETL pipeline** that takes a messy CSV of coffee-shop orders, cleans it with **pandas**, loads it into **PostgreSQL** running in **Docker**, and answers business questions with **SQL**.
 
```
sales_raw.csv ──► clean.py ──► sales_clean.csv ──► load.py ──► PostgreSQL (Docker) ──► analysis.sql
  (Extract)      (Transform)                        (Load)                             (Analysis)
```
 
## Tech stack
 
- **Python 3.11**: pandas, SQLAlchemy, psycopg2
- **PostgreSQL 16** in **Docker Compose**
- **SQL** for analysis
- **Git** for version control
## The data
 
`data/sales_raw.csv` has 260 orders from a small shop that sells coffee, tea, accessories and snacks. It was built on purpose with the problems you find in real data.
 
| Problem | Example | How it was fixed |
|---|---|---|
| Duplicate rows | 10 orders entered twice | `drop_duplicates()` |
| Same city written many ways | `Θεσσαλονίκη`, `ΘΕΣΣΑΛΟΝΙΚΗ`, `thessaloniki`, `Θεσ/νίκη` | Mapping dictionary + `replace()` |
| Extra spaces | `" Αθήνα"` | `str.strip()` |
| Prices stored as text | `€6.50`, `6,50` | Remove symbols, `to_numeric()` |
| Price typo | `650.00` instead of `6.50` | Targeted fix with `.loc` |
| Bad quantities | `-2`, `0`, `3 τεμ`, empty | Clean text, convert, keep only `> 0` |
| Three date formats | `2026-03-04`, `27/01/2026`, `8-7-2026` | Parse each format explicitly, then combine |
| Impossible date | `2026-02-30` | Becomes empty with `errors="coerce"`, row dropped |
| Missing category | 9 empty values | Derived from the product name with `map()` |
| Inconsistent names | `γιώργος νικολάου` | `str.title()` |
 
**Result:** 260 messy rows → **230 clean orders**, 5 cities, 8 products, 4 categories.
 
Dates are never parsed by letting pandas guess the format: guessing turned `2026-03-04` (4 March) into 3 April without raising an error.
 
## Database design
 
The table is created by `sql/create_tables.sql` with explicit types and constraints:
 
- `order_id` is the **primary key**, so the same order can never be stored twice
- `unit_price` is `NUMERIC(10,2)`, exact decimals for money
- every column is `NOT NULL`, so the database rejects incomplete rows
## Idempotent load
 
`load.py` empties the table (`TRUNCATE`) before inserting, so the pipeline can run any number of times and the table always ends up with the same 230 rows. Without this, a second run fails on the primary key.
 
## Analysis
 
`sql/analysis.sql` answers six business questions:
 
1. Total revenue
2. Revenue by city
3. Number of orders by payment method
4. Top 5 customers by revenue
5. Average order value by category
6. Revenue by month
**Key findings**
 
- Total revenue: **€3,638.20**
- **Thessaloniki** brings almost 30% of revenue, **Athens** only 9%
- **Accessories** have the highest average order value (€26.29), snacks the lowest (€6.47)
- **August** was the best month (€489.20) and **May** the weakest (€262.30)
- **Card** is used in more than half of all orders

## How to run

```bash
# 0. Download the project
git clone https://github.com/it175085/sales-etl-pipeline.git
cd sales-etl-pipeline
 
**Requirements:** Python 3.11+, Docker Desktop
 
```bash
# 1. Install Python packages
python -m venv venv
venv\Scripts\activate          # Windows (on macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
 
# 2. Create a .env file from the example
copy .env.example .env         # Windows (on macOS/Linux: cp .env.example .env)
 
# 3. Start PostgreSQL
docker compose up -d
 
# 4. Create the table: run sql/create_tables.sql in any SQL client (e.g. DBeaver),
#    or from the terminal (macOS/Linux):
docker exec -i sales_postgres psql -U sales -d sales_db < sql/create_tables.sql
 
# 5. Run the pipeline
python clean.py
python load.py
```
 
Then run the queries in `sql/analysis.sql`.
 
The database is available at `localhost:5441`.
 
## Project structure
 
```
sales-elt/
├── data/
│   └── sales_raw.csv        # raw input (sales_clean.csv is generated)
├── sql/
│   ├── create_tables.sql    # table definition
│   └── analysis.sql         # business questions
├── explore.py               # first look at the raw data
├── clean.py                 # Transform: cleaning with pandas
├── load.py                  # Load: into PostgreSQL
├── docker-compose.yml       # PostgreSQL container
├── requirements.txt
├── .env.example             # settings template (the real .env is not committed)
└── .gitignore
```
 
## Possible next steps
 
- Extract from an API instead of a CSV
- Incremental loading with upserts instead of a full reload
- Schedule the pipeline to run automatically
 
Claude finished the response
