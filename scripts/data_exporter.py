def export_data_to_postgres(df, table_name, engine):
    """
    Exports a DataFrame to a PostgreSQL database as a table using a SQLAlchemy engine.

    :param df: DataFrame to export.
    :param table_name: Name of the PostgreSQL table to create/replace.
    :param engine: SQLAlchemy engine object.
    """
    try:
        df.to_sql(table_name, engine, index=False, if_exists='replace')
        print(f"Data exported successfully to table '{table_name}'!")
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")
