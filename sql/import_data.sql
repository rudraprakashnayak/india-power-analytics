-- India Power Consumption Analytics - Data Import Script
-- This script loads CSV data into SQLite database
-- Run this after creating the schema with schema.sql

-- Import state_master data from CSV
.mode csv
.import ../data/state_region_mapping.csv state_master

-- Import consumption_records data from CSV
.import ../data/power_consumption.csv consumption_records

-- Verify the data was loaded
SELECT 'State Master Records:' as info;
SELECT COUNT(*) as count FROM state_master;

SELECT 'Consumption Records:' as info;
SELECT COUNT(*) as count FROM consumption_records;

-- Sample data verification
SELECT 'Sample State Master Data:' as info;
SELECT * FROM state_master LIMIT 5;

SELECT 'Sample Consumption Records:' as info;
SELECT * FROM consumption_records LIMIT 5;
