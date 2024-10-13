{{ config(materialized='table') }}

WITH base_data AS (
    SELECT
        "Channel Title",
        COUNT("ID") AS message_count,
        MIN("Date") AS first_message_date,
        MAX("Date") AS last_message_date
    FROM {{ source('week_7', 'cleaned_scraped_data') }}
    GROUP BY "Channel Title"
)
-- This SQL script transforms and aggregates data from the 'cleaned_scraped_data' source table.
-- It groups the data by 'Channel Title' and calculates the following metrics for each channel:
-- - message_count: The total number of messages (count of 'ID').
-- - first_message_date: The date of the first message (minimum 'Date').
-- - last_message_date: The date of the last message (maximum 'Date').
-- The resulting aggregated data is then selected from the 'base_data' CTE.
-- The final output is materialized as a table.

SELECT * FROM base_data

