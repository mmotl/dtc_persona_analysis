from mage_ai.io.postgres import Postgres
from pandas import DataFrame

# Check if the decorator is already in the global scope
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_postgres(*args, **kwargs) -> DataFrame:
    """
    Template for loading data from a PostgreSQL database.
    This method directly runs a SELECT query and returns a DataFrame.
    """
    # Specify your SQL query
    query = 'SELECT * FROM test_ref'

    # Specify the name of the data profile in your io_config.yaml file
    config_profile = 'dev_docker_postgres'

    # --- THE CORRECT AND FINAL PATTERN ---
    
    # 1. Use the .with_profile() class method to create a fully configured loader instance.
    #    This method reads your io_config.yaml file and finds the specified profile.
    loader = Postgres.with_profile(profile=config_profile)

    # 2. Use the created loader instance to execute the query.
    #    The .load() method handles opening and closing the connection.
    return loader.load(query)


@test
def test_output(df: DataFrame, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
    assert not df.empty, 'The DataFrame is empty. Check if the source table has data.'