-- India Power Consumption Analytics - Analytical Queries
-- These queries provide insights into power consumption patterns across India

-- Query 1: Top 5 States by Total Consumption
SELECT 
    state,
    region,
    SUM(consumption_units_mwh) as total_consumption_mwh,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff
FROM consumption_records
GROUP BY state, region
ORDER BY total_consumption_mwh DESC
LIMIT 5;

-- Query 2: Year-over-Year Consumption Growth by State
SELECT 
    state,
    year,
    SUM(consumption_units_mwh) as annual_consumption_mwh,
    ROUND(SUM(consumption_units_mwh) * 100.0 / LAG(SUM(consumption_units_mwh)) OVER (PARTITION BY state ORDER BY year) - 100, 2) as yoy_growth_percent
FROM consumption_records
GROUP BY state, year
ORDER BY state, year;

-- Query 3: Sector-wise Consumption Split
SELECT 
    sector,
    SUM(consumption_units_mwh) as total_consumption_mwh,
    ROUND(SUM(consumption_units_mwh) * 100.0 / (SELECT SUM(consumption_units_mwh) FROM consumption_records), 2) as percentage_share,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita
FROM consumption_records
GROUP BY sector
ORDER BY total_consumption_mwh DESC;

-- Query 4: Seasonal Trend - Monthly Average Across Years
SELECT 
    month,
    ROUND(AVG(consumption_units_mwh), 2) as avg_consumption_mwh,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff
FROM consumption_records
GROUP BY month
ORDER BY 
    CASE month
        WHEN 'January' THEN 1
        WHEN 'February' THEN 2
        WHEN 'March' THEN 3
        WHEN 'April' THEN 4
        WHEN 'May' THEN 5
        WHEN 'June' THEN 6
        WHEN 'July' THEN 7
        WHEN 'August' THEN 8
        WHEN 'September' THEN 9
        WHEN 'October' THEN 10
        WHEN 'November' THEN 11
        WHEN 'December' THEN 12
    END;

-- Query 5: States with Highest Renewable Energy Share
SELECT 
    state,
    region,
    ROUND(AVG(renewable_share_percent), 2) as avg_renewable_percent,
    SUM(consumption_units_mwh) as total_consumption_mwh
FROM consumption_records
GROUP BY state, region
ORDER BY avg_renewable_percent DESC
LIMIT 10;

-- Query 6: Per-Capita Consumption Ranking by State
SELECT 
    state,
    region,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita_consumption,
    SUM(consumption_units_mwh) as total_consumption_mwh
FROM consumption_records
GROUP BY state, region
ORDER BY avg_per_capita_consumption DESC;

-- Query 7: Tariff vs Consumption Correlation by State
SELECT 
    state,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff,
    SUM(consumption_units_mwh) as total_consumption_mwh,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita
FROM consumption_records
GROUP BY state
ORDER BY avg_tariff DESC;

-- Query 8: Region-wise Summary
SELECT 
    region,
    COUNT(DISTINCT state) as num_states,
    SUM(consumption_units_mwh) as total_consumption_mwh,
    ROUND(SUM(consumption_units_mwh) * 100.0 / (SELECT SUM(consumption_units_mwh) FROM consumption_records), 2) as regional_share_percent,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita,
    ROUND(AVG(renewable_share_percent), 2) as avg_renewable_percent
FROM consumption_records
GROUP BY region
ORDER BY total_consumption_mwh DESC;

-- Query 9: Top 5 States by Industrial Consumption
SELECT 
    state,
    region,
    SUM(consumption_units_mwh) as industrial_consumption_mwh,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff
FROM consumption_records
WHERE sector = 'Industrial'
GROUP BY state, region
ORDER BY industrial_consumption_mwh DESC
LIMIT 5;

-- Query 10: Monthly Consumption Trend by Sector
SELECT 
    month,
    sector,
    ROUND(AVG(consumption_units_mwh), 2) as avg_consumption_mwh
FROM consumption_records
GROUP BY month, sector
ORDER BY 
    CASE month
        WHEN 'January' THEN 1
        WHEN 'February' THEN 2
        WHEN 'March' THEN 3
        WHEN 'April' THEN 4
        WHEN 'May' THEN 5
        WHEN 'June' THEN 6
        WHEN 'July' THEN 7
        WHEN 'August' THEN 8
        WHEN 'September' THEN 9
        WHEN 'October' THEN 10
        WHEN 'November' THEN 11
        WHEN 'December' THEN 12
    END,
    sector;
