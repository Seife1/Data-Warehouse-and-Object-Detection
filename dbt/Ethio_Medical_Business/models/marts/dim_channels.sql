{{ config(materialized='table') }}

WITH staged_messages AS (
    SELECT * FROM {{ ref('stg_telegram_messages') }}
),

channel_aggregations AS (
    SELECT
        MD5(channel_username || '-' || channel_title) AS channel_key,
        channel_title,
        channel_username,
        COUNT(message_id) AS total_messages,
        SUM(CASE WHEN has_media THEN 1 ELSE 0 END) AS messages_with_media,
        SUM(CASE WHEN mentions_price THEN 1 ELSE 0 END) AS messages_mentioning_price,
        MIN(message_timestamp) AS first_message_date,
        MAX(message_timestamp) AS last_message_date,
        ROUND(AVG(message_length), 2) AS avg_message_length
    FROM staged_messages
    GROUP BY channel_title, channel_username
)

SELECT * FROM channel_aggregations
