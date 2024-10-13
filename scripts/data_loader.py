import pandas as pd

def load_data_from_db(query, engine):
    """
    Loads data from PostgreSQL database using a SQLAlchemy engine and SQL query.

    :param query: SQL query to execute.
    :param engine: SQLAlchemy engine object.
    :return: DataFrame containing the results of the query.
    """
    try:
        df = pd.read_sql_query(query, engine)
        print("Data loaded successfully!")
        return df
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None