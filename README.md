# India Power Consumption Analytics

![Power BI Dashboard](screenshots/dashboard_overview.png)

A comprehensive end-to-end analytics project analyzing power consumption patterns across Indian states using Excel, SQL, and Power BI.

## 🎯 Problem Statement

Understanding electricity consumption patterns across Indian states is crucial for energy planning, policy-making, and infrastructure development. This project analyzes consumption data across 16 major states to identify trends, seasonal patterns, and regional disparities in power usage across different sectors (Residential, Commercial, Industrial, Agricultural).

## 📊 Project Objective

- Analyze power consumption patterns across Indian states from 2023-2025
- Identify seasonal trends and regional disparities
- Compare consumption across different sectors
- Assess renewable energy adoption by state
- Build interactive dashboards for stakeholder visualization

## 🛠 Tools Used

- **Excel** - Data cleaning, VLOOKUP/XLOOKUP, pivot tables, conditional formatting
- **SQLite** - Database schema design, data import, analytical SQL queries
- **Power BI** - Interactive dashboards, DAX measures, data visualization

## 📁 Project Structure

```
india-power-analytics/
├── data/
│   ├── power_consumption.csv          # Main dataset (500 rows)
│   └── state_region_mapping.csv       # State reference table
├── sql/
│   ├── schema.sql                     # Database schema definition
│   ├── import_data.sql                # CSV to SQLite import script
│   └── queries.sql                    # 10 analytical SQL queries
├── docs/
│   ├── excel_guide.md                 # Excel dashboard build guide
│   └── powerbi_guide.md               # Power BI dashboard build guide
├── screenshots/                       # Dashboard screenshots
└── README.md                          # This file
```

## 📈 Dataset Description

### power_consumption.csv (500 rows)
- **Coverage**: 16 major Indian states across 5 regions (North, South, East, West, Northeast)
- **Time Period**: January 2023 - October 2025 (selected months for seasonal analysis)
- **Sectors**: Residential, Commercial, Industrial, Agricultural
- **Key Metrics**: Consumption (MWh), per-capita consumption, tariff rates, renewable energy share
- **Features**: Realistic consumption patterns with seasonal variations and state-specific characteristics

### state_region_mapping.csv (16 rows)
- State codes, regional classifications, and capital cities for reference and normalization

## 🔍 Key Insights

*[After completing your analysis, fill in your key findings here. Examples:]*

- **Top Consumers**: Maharashtra and Gujarat lead in industrial consumption due to heavy manufacturing presence
- **Seasonal Patterns**: Summer months (April-July) show 25-30% higher consumption across all states
- **Renewable Leaders**: Kerala, Tamil Nadu, and Karnataka show highest renewable energy adoption (>30%)
- **Regional Disparity**: Western region consumes 35% more per capita than Northeastern region
- **Sector Split**: Industrial sector accounts for 45% of total consumption, followed by Residential (30%)

## 🚀 How to Reproduce

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd india-power-analytics
```

### Step 2: SQL Database Setup
```bash
# Navigate to sql folder
cd sql

# Create database and schema
sqlite3 power_consumption.db < schema.sql

# Import CSV data
sqlite3 power_consumption.db < import_data.sql

# Run analytical queries
sqlite3 power_consumption.db < queries.sql
```

### Step 3: Excel Dashboard
1. Open `data/power_consumption.csv` in Excel
2. Follow the step-by-step guide in `docs/excel_guide.md`
3. Build pivot tables, charts, and conditional formatting
4. Create the dashboard with KPI cards

### Step 4: Power BI Dashboard
1. Open Power BI Desktop
2. Import `data/power_consumption.csv` and `data/state_region_mapping.csv`
3. Follow the comprehensive guide in `docs/powerbi_guide.md`
4. Set up data model relationships
5. Create DAX measures and build the 4-page report

## 📊 Dashboard Screenshots

### Power BI Report Pages

![Overview Page](screenshots/overview_page.png)
*Overview: KPI cards and India map visualization*

![Trend Analysis](screenshots/trend_analysis.png)
*Trend Analysis: Monthly consumption patterns and seasonal trends*

![Sector Breakdown](screenshots/sector_breakdown.png)
*Sector Breakdown: Consumption distribution by sector*

![State Comparison](screenshots/state_comparison.png)
*State Comparison: Per-capita and renewable energy analysis*

### Excel Dashboard

![Excel Dashboard](screenshots/excel_dashboard.png)
*Excel dashboard with pivot tables and charts*

## 🎓 Learning Outcomes

**Excel Skills:**
- Data import, cleaning, and validation
- VLOOKUP/XLOOKUP for data merging
- Pivot tables and multi-dimensional analysis
- Conditional formatting and data visualization
- Dashboard creation with KPI cards

**SQL Skills:**
- Database schema design and normalization
- Data import/export operations
- Complex analytical queries with aggregations
- Window functions (LAG, RANK) for trend analysis
- Foreign key relationships and data integrity

**Power BI Skills:**
- Data modeling and relationship management
- DAX measure creation and optimization
- Interactive visualization design
- Report publishing and sharing
- Cross-filtering and drill-down capabilities

## 🔗 Power BI Report

**[View Interactive Report](#)** *(Add your Power BI Publish-to-Web link here)*

> ⚠️ **Note**: The interactive report is published using Power BI's "Publish to Web" feature, which makes the data publicly accessible. This is for demonstration purposes only with synthetic data.

## 📝 SQL Queries Included

1. Top 5 States by Total Consumption
2. Year-over-Year Growth by State
3. Sector-wise Consumption Split
4. Seasonal Trend Analysis
5. States with Highest Renewable Share
6. Per-Capita Consumption Ranking
7. Tariff vs Consumption Correlation
8. Region-wise Summary
9. Top Industrial Consumers
10. Monthly Sector Trends

## 🛡 Data Privacy

This project uses **synthetic data** created for educational purposes. The consumption figures, tariff rates, and renewable energy percentages are realistic but do not represent actual state-level power consumption data.

## 📄 License

This project is created for educational purposes. Feel free to use it for learning and portfolio building.

## 👤 Author

**Your Name** - Data Analytics Portfolio Project

## 🙏 Acknowledgments

- State and regional data based on official Indian geographical divisions
- Consumption patterns inspired by real-world electricity consumption trends
- Tariff rates based on approximate industry standards in India

---

**Built with ❤️ using Excel, SQL, and Power BI**
