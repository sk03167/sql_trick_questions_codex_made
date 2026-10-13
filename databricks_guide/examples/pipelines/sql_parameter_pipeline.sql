-- Separate illustrative SQL asset, using current SQL pipeline parameters.
-- Prerequisite: bronze.order_events already exists and fields match this lab.
CREATE OR REFRESH MATERIALIZED VIEW recent_order_events AS
SELECT * FROM IDENTIFIER(:source_catalog || '.bronze.order_events')
WHERE CAST(event_time AS TIMESTAMP) >= CAST(:start_date AS TIMESTAMP);
