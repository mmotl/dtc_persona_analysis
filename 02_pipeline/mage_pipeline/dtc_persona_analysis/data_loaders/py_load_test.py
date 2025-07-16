from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


import psycopg2
import os

@data_loader
def load_data_from_postgres(*args, **kwargs):
    """
    Template for loading data from a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    # This is a direct connection test that completely bypasses io_config.yaml
# It uses the same library that Mage uses under the hood.

# These are the hardcoded connection details for the Docker network
db_host = 'postgres'          # The Docker service name
db_port = 5432              # The internal Docker port
db_name = 'mydb'
db_user = 'user'
db_password = 'password'    # The password from your docker-compose file

# We will build the connection string manually
conn_string = f"dbname='{db_name}' user='{db_user}' host='{db_host}' port='{db_port}' password='{db_password}'"

print("--- Starting Direct Connection Test ---")
print(f"Attempting to connect with DSN: {conn_string}")

conn = None  # Initialize connection variable
try:
    # Attempt to establish the connection
    conn = psycopg2.connect(conn_string)
    
    # If the connection succeeds, create a cursor to run a command
    cur = conn.cursor()
    
    # Execute a simple, harmless query to prove the connection is live
    print("Connection established. Executing 'SELECT 1'...")
    cur.execute('SELECT 1;')
    
    # Fetch the result
    result = cur.fetchone()
    print(f"Query executed successfully. Result: {result}")
    
    # If we get here, the test is a success
    print("\n✅✅✅ --- SUCCESS! Direct connection to PostgreSQL is working. --- ✅✅✅")
    
    # Clean up
    cur.close()

except Exception as e:
    # If any part of the connection or query fails, print the error
    print(f"\n❌❌❌ --- FAILURE! An error occurred: {e} --- ❌❌❌")

finally:
    # Make sure to close the connection if it was opened
    if conn is not None:
        conn.close()
        print("Connection closed.")

# Mage requires data loaders to return something, even if it's empty
@data_loader
def direct_connection_test(*args, **kwargs):
    # This block's purpose is the print output, so we don't need to return data.
    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
