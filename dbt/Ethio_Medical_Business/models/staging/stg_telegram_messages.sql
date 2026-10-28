{{ config(materialized='view') }}

WITH raw_source AS (
    SELECT
        id AS message_id,
        channel_title,
        channel_username,
        message AS message_text,
        date AS message_timestamp,
        media_path
    FROM {{ source('week_7', 'cleaned_scraped_data') }}
),

staged AS (
    SELECT
        message_id,
        TRIM(COALESCE(channel_title, 'Unknown Channel')) AS channel_title,
        TRIM(COALESCE(channel_username, 'unknown')) AS channel_username,
        message_text,
        message_timestamp,
        media_path,
        CASE 
            WHEN media_path IS NOT NULL AND TRIM(media_path) != '' THEN TRUE 
            ELSE FALSE 
        END AS has_media,
        LENGTH(COALESCE(message_text, '')) AS message_length,
        CASE 
            WHEN message_text ~* '(birr|etb|\$|\bprice\b|\bዋጋ\b)' THEN TRUE 
            ELSE FALSE 
        END AS mentions_price
    FROM raw_source
    WHERE message_id IS NOT NULL
)

SELECT * FROM staged
