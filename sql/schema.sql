-- India Power Consumption Analytics - Database Schema
-- This script creates normalized tables for SQLite

-- Drop tables if they exist (for clean re-creation)
DROP TABLE IF EXISTS consumption_records;
DROP TABLE IF EXISTS state_master;

-- Create state_master table (reference table for states)
CREATE TABLE state_master (
    state_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL UNIQUE,
    state_code TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL,
    capital TEXT NOT NULL
);

-- Create consumption_records table (main data table)
CREATE TABLE consumption_records (
    record_id INTEGER PRIMARY KEY,
    state TEXT NOT NULL,
    region TEXT NOT NULL,
    sector TEXT NOT NULL,
    month TEXT NOT NULL,
    year INTEGER NOT NULL,
    consumption_units_mwh REAL NOT NULL,
    per_capita_consumption REAL NOT NULL,
    tariff_rate_per_unit REAL NOT NULL,
    renewable_share_percent REAL NOT NULL,
    FOREIGN KEY (state) REFERENCES state_master(state)
);

-- Create indexes for better query performance
CREATE INDEX idx_consumption_state ON consumption_records(state);
CREATE INDEX idx_consumption_year ON consumption_records(year);
CREATE INDEX idx_consumption_sector ON consumption_records(sector);
CREATE INDEX idx_consumption_region ON consumption_records(region);
CREATE INDEX idx_consumption_month ON consumption_records(month);
