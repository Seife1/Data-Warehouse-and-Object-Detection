{{ config(materialized='table') }}

WITH raw_detections AS (
    SELECT * FROM {{ ref('raw_image_detections') }}
),

computed_detections AS (
    SELECT
        detection_id,
        image_name,
        TRIM(object_class) AS object_class,
        ROUND(confidence::numeric, 4) AS confidence,
        CASE
            WHEN confidence >= 0.75 THEN 'High'
            WHEN confidence >= 0.50 THEN 'Medium'
            ELSE 'Low'
        END AS confidence_tier,
        ROUND((xmax - xmin)::numeric, 2) AS box_width,
        ROUND((ymax - ymin)::numeric, 2) AS box_height,
        ROUND(((xmax - xmin) * (ymax - ymin))::numeric, 2) AS box_area,
        xmin,
        ymin,
        xmax,
        ymax
    FROM raw_detections
)

SELECT * FROM computed_detections
