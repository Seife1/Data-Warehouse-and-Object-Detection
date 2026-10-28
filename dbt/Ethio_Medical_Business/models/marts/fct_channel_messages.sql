{{ config(materialized='table') }}

WITH staged_messages AS (
    SELECT * FROM {{ ref('stg_telegram_messages') }}
),

channels AS (
    SELECT channel_key, channel_title, channel_username FROM {{ ref('dim_channels') }}
),

fact_messages AS (
    SELECT
        m.message_id,
        c.channel_key,
        m.channel_title,
        m.channel_username,
        m.message_timestamp,
        m.message_text,
        m.has_media,
        m.media_path,
        m.message_length,
        m.mentions_price
    FROM staged_messages m
    LEFT JOIN channels c
        ON m.channel_title = c.channel_title
        AND m.channel_username = c.channel_username
)

SELECT * FROM fact_messages
