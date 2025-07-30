from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    MetaData,
    Table,
    text,
    inspect,
)
from pandas.io.sql import get_schema
import pandas as pd
from dotenv import load_dotenv
import os
import sys

load_dotenv()

password = os.getenv("POSTGRES_PASSWORD")

table_name = sys.argv[1]  # for example purposes, change as needed
file_name = sys.argv[2]  # for example purposes, change as needed

# Define database connection
db_uri = f"postgresql+psycopg2://user:{password}@localhost:4321/mydb"
engine = create_engine(db_uri)

df = pd.read_csv(f"../data/{file_name}")

# Convert the 'date' column to datetime format with UTC timezone
df["date"] = pd.to_datetime(df["date"], utc=True)

# 1. Get the schema of the dataframe as it would be created in SQL

inspector = inspect(engine)
schema_sql = get_schema(df, name="table_name", con=engine)
schema_sql = schema_sql.replace(
    "CREATE TABLE",
    "CREATE TABLE IF NOT EXISTS",
    1,  # The '1' ensures we only replace the first instance
)
print(schema_sql)

# # Robustly add the "customer_id" as a SERIAL PRIMARY KEY.
# # We find the first '(' and insert the column definition right after it.
# first_paren_index = schema_sql.find('(')
# if first_paren_index != -1:
#     # The new column to be inserted
#     pk_column_definition = '\n    customer_id SERIAL PRIMARY KEY,'
#     # Reconstruct the string with the new column
#     schema_sql = (
#         schema_sql[:first_paren_index + 1] +
#         pk_column_definition +
#         schema_sql[first_paren_index + 1:]
#     )
# print(schema_sql)


# 2. Check if the table already exists in the database
if not inspector.has_table(table_name):
    print(f"Table {table_name} does not exist. Creating it now...")
    with engine.connect() as conn:
        conn.execute(text(schema_sql))
        conn.commit()  # Commit the table creation
    print(f"Table {table_name} created successfully.")
else:
    print(f"Table {table_name} already exists.")

# 3. Append data
print(f"Appending data to {table_name} table...")
with engine.connect() as conn:
    df.to_sql(table_name, con=conn, if_exists="append", index=False)
    # The to_sql method in pandas often uses its own transaction handling,
    # but an explicit commit here is safe and good practice in SQLAlchemy 2.0.
    conn.commit()

print("Data successfully written to the database.")
