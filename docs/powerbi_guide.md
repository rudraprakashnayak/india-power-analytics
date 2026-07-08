# Power BI Build Guide - India Power Consumption Analytics

This guide will help you build an interactive Power BI dashboard using the provided CSV files.

## Prerequisites
- Power BI Desktop (Windows version - free download from Microsoft)
- Files: `power_consumption.csv` and `state_region_mapping.csv` from the `data/` folder
- Optional: `power_consumption.db` SQLite database (if you created it using the SQL scripts)

---

## Step 1: Import Data into Power BI

### Option A: Import from CSV Files (Recommended for Beginners)

#### 1.1 Import power_consumption.csv
1. Open Power BI Desktop
2. Click **Get Data** (Home tab) → **Text/CSV**
3. Navigate to `data/power_consumption.csv` and select it
4. In the import dialog:
   - Ensure **File Origin** is set to detect automatically
   - Verify that columns are correctly detected
   - Click **Load**

#### 1.2 Import state_region_mapping.csv
1. Click **Get Data** → **Text/CSV**
2. Navigate to `data/state_region_mapping.csv` and select it
3. Click **Load**

### Option B: Import from SQLite Database (Advanced)

1. Click **Get Data** → **Database** → **SQLite Database**
2. Navigate to `sql/power_consumption.db` (if you created it)
3. Select the tables: `consumption_records` and `state_master`
4. Click **Load**

---

## Step 2: Set Up the Data Model

### 2.1 View Data Model
1. Go to **Modeling** tab → Click **Manage Relationships**
2. Alternatively, click the **Model View** icon on the left sidebar (second icon from left)

### 2.2 Create Relationship Between Tables
1. In Model View, you'll see two tables:
   - `power_consumption` (or `consumption_records`)
   - `state_region_mapping` (or `state_master`)

2. Click and drag from the **state** column in `power_consumption` table
3. Drop it onto the **state** column in `state_region_mapping` table
4. A line will appear connecting the tables
5. Click the relationship line
6. In the properties pane (right side):
   - Ensure **Cardinality** is set to **Many to One** (*:1)
   - Ensure **Cross filter direction** is set to **Single**
   - The relationship should be: `power_consumption[state] → state_region_mapping[state]`

### 2.3 Verify Data Types
1. Go to **Data View** (first icon on left sidebar)
2. Select the `power_consumption` table
3. In the Fields pane (right), verify column data types:
   - `record_id`: Whole Number
   - `year`: Whole Number
   - `consumption_units_mwh`: Decimal Number
   - `per_capita_consumption`: Decimal Number
   - `tariff_rate_per_unit`: Decimal Number
   - `renewable_share_percent`: Decimal Number
   - All text columns: Text

4. If any column has wrong type:
   - Select the column
   - Go to **Column tools** tab
   - Change **Data type** dropdown to correct type

---

## Step 3: Create DAX Measures

### 3.1 Open DAX Editor
1. Go to **Home** tab → Click **New Measure**
2. A formula bar will appear at the top
3. Enter each measure below and press Enter

### 3.2 Create the 5 Required DAX Measures

#### Measure 1: Total Consumption
```
Total Consumption = 
SUM(power_consumption[consumption_units_mwh])
```

#### Measure 2: YoY Growth %
```
YoY Growth % = 
VAR CurrentYearConsumption = 
    CALCULATE([Total Consumption], power_consumption[year] = MAX(power_consumption[year]))
VAR PreviousYearConsumption = 
    CALCULATE([Total Consumption], power_consumption[year] = MAX(power_consumption[year]) - 1)
RETURN
    DIVIDE(CurrentYearConsumption - PreviousYearConsumption, PreviousYearConsumption, 0)
```

#### Measure 3: Avg Tariff
```
Avg Tariff = 
AVERAGE(power_consumption[tariff_rate_per_unit])
```

#### Measure 4: Renewable Share %
```
Renewable Share % = 
AVERAGE(power_consumption[renewable_share_percent])
```

#### Measure 5: Per Capita Rank
```
Per Capita Rank = 
RANKX(
    ALL(power_consumption[state]), 
    CALCULATE(AVERAGE(power_consumption[per_capita_consumption])), 
    , 
    DESC
)
```

### 3.3 Additional Useful Measures (Optional)

#### Measure 6: Total Consumption by Sector
```
Total Consumption by Sector = 
SUM(power_consumption[consumption_units_mwh])
```

#### Measure 7: Regional Consumption
```
Regional Consumption = 
SUM(power_consumption[consumption_units_mwh])
```

#### Measure 8: Monthly Average
```
Monthly Average = 
AVERAGEX(
    VALUES(power_consumption[month]), 
    [Total Consumption]
)
```

---

## Step 4: Build Report Pages

### Page 1: Overview (KPI Cards + India Map)

#### 4.1 Create Overview Page
1. Click the **+** icon at the bottom of Power BI to add a new page
2. Rename the page: Double-click "Page 1" tab → Type "Overview"

#### 4.2 Add KPI Cards
1. Click the **Card** visual icon (in Visualizations pane)
2. Drag **Total Consumption** measure to the card
3. Format the card:
   - Click the paint roller icon (Format)
   - Under **Card**, change title to "Total Consumption (MWh)"
   - Set font size to 20
   - Choose a background color (light blue)

4. Repeat for other measures:
   - Card 2: **Avg Tariff** → Title: "Average Tariff (₹/unit)"
   - Card 3: **Renewable Share %** → Title: "Avg Renewable Share (%)"
   - Card 4: Create a measure for total records: `Total Records = COUNTROWS(power_consumption)`

5. Arrange cards in a row at the top of the page

#### 4.3 Add India Map (Filled Map)
1. Click the **Filled Map** visual icon
2. Drag **state** from `power_consumption` to **Location**
3. Drag **Total Consumption** to **Values**
4. Drag **state_region_mapping[region]** to **Legend** (optional)
5. Format the map:
   - Click Format → Under **Map controls**, enable zoom buttons
   - Under **Data labels**, enable to show state names
   - Under **Title**, change to "Consumption by State"

#### 4.4 Add Slicers
1. Click the **Slicer** visual icon
2. Drag **year** from `power_consumption` to **Field**
3. Position slicer on the right side
4. Add another slicer for **region**
5. Format slicers to be vertical

---

### Page 2: Trend Analysis (Line Charts by Month/Season)

#### 4.5 Create Trend Analysis Page
1. Click **+** to add new page
2. Rename to "Trend Analysis"

#### 4.6 Add Monthly Trend Line Chart
1. Click **Line Chart** visual icon
2. Drag **month** to **Axis**
3. Drag **Total Consumption** to **Values**
4. Drag **year** to **Legend**
5. Format:
   - Title: "Monthly Consumption Trend"
   - Enable data labels
   - Add smooth line option if desired

#### 4.7 Add Seasonal Comparison (Clustered Column Chart)
1. Click **Clustered Column Chart** visual icon
2. Drag **region** to **Axis**
3. Drag **Total Consumption** to **Values**
4. Drag **year** to **Legend**
5. Format:
   - Title: "Regional Consumption by Year"
   - Enable data labels

#### 4.8 Add Sector Trend (Stacked Area Chart)
1. Click **Stacked Area Chart** visual icon
2. Drag **month** to **Axis**
3. Drag **Total Consumption** to **Values**
4. Drag **sector** to **Legend**
5. Format:
   - Title: "Sector-wise Monthly Trend"
   - Adjust transparency for better visibility

---

### Page 3: Sector Breakdown

#### 4.9 Create Sector Breakdown Page
1. Click **+** to add new page
2. Rename to "Sector Breakdown"

#### 4.10 Add Sector Distribution (Donut Chart)
1. Click **Donut Chart** visual icon
2. Drag **sector** to **Legend**
3. Drag **Total Consumption** to **Values**
4. Format:
   - Title: "Consumption by Sector"
   - Enable data labels with percentages
   - Change colors for each sector

#### 4.11 Add Sector Comparison (Treemap)
1. Click **Treemap** visual icon
2. Drag **state** to **Group**
3. Drag **sector** to **Category**
4. Drag **Total Consumption** to **Values**
5. Format:
   - Title: "State-Sector Consumption Treemap"
   - Enable labels

#### 4.12 Add Sector Table
1. Click **Table** visual icon
2. Drag **sector**, **state**, **Total Consumption**, **Avg Tariff** to **Values**
3. Format:
   - Enable totals
   - Sort by Total Consumption descending
   - Title: "Sector-wise Details"

---

### Page 4: State Comparison

#### 4.13 Create State Comparison Page
1. Click **+** to add new page
2. Rename to "State Comparison"

#### 4.14 Add State Ranking (Bar Chart)
1. Click **Clustered Bar Chart** visual icon
2. Drag **state** to **Axis**
3. Drag **Total Consumption** to **Values**
4. Drag **region** to **Legend**
5. Format:
   - Title: "State Consumption Ranking"
   - Sort by Total Consumption descending
   - Enable data labels

#### 4.15 Add Per Capita Comparison (Scatter Plot)
1. Click **Scatter Chart** visual icon
2. Drag **per_capita_consumption** to **X-axis**
3. Drag **Total Consumption** to **Y-axis**
4. Drag **state** to **Details**
5. Drag **region** to **Legend**
6. Format:
   - Title: "Per Capita vs Total Consumption"
   - Enable data labels for states
   - Adjust marker size

#### 4.16 Add Renewable Energy Comparison (Ribbon Chart)
1. Click **Ribbon Chart** visual icon
2. Drag **state** to **Axis**
3. Drag **Renewable Share %** to **Values**
4. Drag **region** to **Legend**
5. Format:
   - Title: "Renewable Energy Share by State"
   - Enable data labels

#### 4.17 Add Detailed State Table
1. Click **Table** visual icon
2. Add columns: **state**, **region**, **Total Consumption**, **Avg Tariff**, **Renewable Share %**, **Per Capita Rank**
3. Format:
   - Enable search box
   - Enable sorting on all columns
   - Title: "State-wise Summary"

#### 4.18 Add Slicers for Interactivity
1. Add slicer for **year**
2. Add slicer for **sector**
3. Add slicer for **region**
4. Position slicers on the left side
5. Connect all slicers to visuals on the page (automatic by default)

---

## Step 5: Formatting and Polish

### 5.1 Apply Consistent Theme
1. Go to **View** tab → Click **Themes**
2. Choose a professional theme (e.g., "Corporate" or "Urban")
3. Or customize colors in **Format** pane

### 5.2 Add Page Navigation
1. Go to **View** tab → Enable **Page Navigation Pane** (if not visible)
2. Right-click page tabs → Rename to meaningful names
3. Reorder pages by dragging tabs

### 5.3 Add Bookmarks (Optional)
1. Go to **View** tab → Click **Bookmarks** → **Add**
2. Create bookmarks for different views (e.g., "2023 View", "Industrial Focus")
3. Add bookmark buttons to report for navigation

### 5.4 Set Default View
1. Configure slicers to show all data by default
2. Set the Overview page as the first page
3. Save the report

---

## Step 6: Publish and Share (Optional)

### 6.1 Save the Report
1. Click **File** → **Save As**
2. Choose **Power BI Report (.pbix)**
3. Save to your project folder

### 6.2 Publish to Power BI Service (Requires Account)
1. Click **Home** tab → **Publish**
2. Select your workspace
3. Follow prompts to upload
4. Share with colleagues via link

### 6.3 Export to PDF
1. Click **File** → **Export** → **Export to PDF**
2. Choose pages to include
3. Save PDF for sharing without Power BI

---

## Summary of Your Power BI Report

Your completed Power BI report should have:
- **4 Report Pages**: Overview, Trend Analysis, Sector Breakdown, State Comparison
- **5 DAX Measures**: Total Consumption, YoY Growth %, Avg Tariff, Renewable Share %, Per Capita Rank
- **Interactive Visuals**: Maps, charts, tables, slicers
- **Data Model**: Proper relationship between consumption and state reference tables
- **Professional Formatting**: Consistent theme, titles, and labels

You can now filter by year, region, and sector to explore the data dynamically!
