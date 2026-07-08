# Excel Build Guide - India Power Consumption Analytics

This guide will help you build a power consumption dashboard in Excel using the provided CSV files.

## Prerequisites
- Microsoft Excel (Windows version)
- Files: `power_consumption.csv` and `state_region_mapping.csv` from the `data/` folder

---

## Step 1: Import and Clean the Raw CSV

### 1.1 Import power_consumption.csv
1. Open Excel
2. Go to **Data** tab → **Get Data** → **From Text/CSV**
3. Navigate to `data/power_consumption.csv` and select it
4. In the import dialog:
   - Ensure **File Origin** is set to **65001: Unicode (UTF-8)**
   - Click **Load** to import into a new worksheet

### 1.2 Clean the Data
1. **Remove Duplicates:**
   - Select the entire dataset (Ctrl+A)
   - Go to **Data** tab → **Remove Duplicates**
   - Check all columns
   - Click **OK** (Excel will tell you if duplicates were found)

2. **Fix Blank Cells:**
   - Select the dataset
   - Press **Ctrl+F** → Click **Options** → Check **Match entire cell contents**
   - Leave "Find what" blank and click **Find All**
   - If blanks are found, replace with 0 or appropriate value

3. **Format Numbers:**
   - Select columns H, I, J, K (consumption, per_capita, tariff, renewable)
   - Right-click → **Format Cells**
   - Select **Number** category
   - Set decimal places to **2**
   - Click **OK**

4. **Format Headers:**
   - Select row 1 (headers)
   - Go to **Home** tab → Click **Bold** (Ctrl+B)
   - Apply **Light Gray** fill color from the Fill Color dropdown

5. **Rename the Sheet:**
   - Double-click the sheet tab at the bottom
   - Name it **"Raw_Data"**

---

## Step 2: Import state_region_mapping.csv

1. Go to **Data** tab → **Get Data** → **From Text/CSV**
2. Navigate to `data/state_region_mapping.csv` and select it
3. Click **Load** to import into a new worksheet
4. Rename this sheet to **"State_Reference"**

---

## Step 3: Merge Data Using VLOOKUP/XLOOKUP

### 3.1 Add Reference Columns to Raw_Data
1. Go to the **Raw_Data** sheet
2. Add new headers in columns L, M, N:
   - L1: `state_code`
   - M1: `region_ref`
   - N1: `capital`

### 3.2 Use XLOOKUP (Excel 2021 or later)
In cell L2, enter:
```
=XLOOKUP(B2, State_Reference!$A$2:$A$17, State_Reference!$B$2:$B$17, "Not Found")
```

In cell M2, enter:
```
=XLOOKUP(B2, State_Reference!$A$2:$A$17, State_Reference!$C$2:$C$17, "Not Found")
```

In cell N2, enter:
```
=XLOOKUP(B2, State_Reference!$A$2:$A$17, State_Reference!$D$2:$D$17, "Not Found")
```

### 3.3 Use VLOOKUP (Excel 2019 or earlier)
If you don't have XLOOKUP, use VLOOKUP instead:

In cell L2, enter:
```
=VLOOKUP(B2, State_Reference!$A$2:$D$17, 2, FALSE)
```

In cell M2, enter:
```
=VLOOKUP(B2, State_Reference!$A$2:$D$17, 3, FALSE)
```

In cell N2, enter:
```
=VLOOKUP(B2, State_Reference!$A$2:$D$17, 4, FALSE)
```

### 3.4 Copy Formulas Down
1. Select cells L2:N2
2. Double-click the small square at the bottom-right corner (fill handle) to copy down to all rows
3. The formulas should now populate for all 500 rows

---

## Step 4: Build a Pivot Table

### 4.1 Create Pivot Table
1. Select the entire dataset on **Raw_Data** sheet (Ctrl+A)
2. Go to **Insert** tab → **PivotTable**
3. In the dialog:
   - Choose **New Worksheet**
   - Click **OK**
4. Rename the new sheet to **"Pivot_Analysis"**

### 4.2 Configure Pivot Table for State and Sector Analysis
1. In the **PivotTable Fields** pane (right side):
   - Drag **state** to **Rows** area
   - Drag **sector** to **Columns** area
   - Drag **consumption_units_mwh** to **Values** area

2. Format the values:
   - Right-click any value in the pivot table → **Value Field Settings**
   - Change "Sum of consumption_units_mwh" to a cleaner name like "Total Consumption (MWh)"
   - Click **Number Format** → Select **Number** → Set decimal places to **0**
   - Click **OK** twice

### 4.3 Create a Second Pivot Table for Regional Analysis
1. On the same **Pivot_Analysis** sheet, click outside the existing pivot table
2. Go to **Insert** tab → **PivotTable**
3. Choose **New Worksheet** or place on existing sheet
4. Configure:
   - Drag **region** to **Rows**
   - Drag **year** to **Columns**
   - Drag **consumption_units_mwh** to **Values**

---

## Step 5: Add Charts

### 5.1 Create Column Chart - Consumption by State
1. Select the first pivot table (State × Sector)
2. Go to **Insert** tab → **Column Chart** → **Clustered Column**
3. Move the chart to a clean area of the sheet
4. Format the chart:
   - Click chart title → Type "Power Consumption by State and Sector"
   - Right-click legend → Choose position (Bottom or Right)
   - Right-click axis → Format as needed

### 5.2 Create Line Chart - Monthly Trend
1. Go back to **Raw_Data** sheet
2. Create a small summary table:
   - Select a blank area
   - Create a table with months in rows and average consumption
   - Use formula: `=AVERAGEIF(F:F, "January", H:H)` for January, etc.
3. Select the summary table
4. Go to **Insert** tab → **Line Chart** → **Line with Markers**
5. Format:
   - Title: "Monthly Consumption Trend"
   - Add data labels if desired

### 5.3 Create Pie Chart - Sector Distribution
1. Create a pivot table showing total consumption by sector only
2. Select the pivot table
3. Go to **Insert** tab → **Pie Chart** → **Pie**
4. Format:
   - Title: "Consumption by Sector"
   - Add percentage labels: Right-click pie → **Add Data Labels** → **Format Data Labels** → Check **Percentage**

---

## Step 6: Create Dashboard Tab

### 6.1 Create Dashboard Sheet
1. Right-click any sheet tab → **Insert** → **Worksheet**
2. Rename to **"Dashboard"**

### 6.2 Add Key Metrics (KPI Cards)
1. In cells A1:B5, create KPI summary:
   - A1: "Total Consumption" | B1: `=SUM(Raw_Data!H:H)`
   - A2: "Avg Per Capita" | B2: `=AVERAGE(Raw_Data!I:I)`
   - A3: "Avg Tariff" | B3: `=AVERAGE(Raw_Data!J:J)`
   - A4: "Avg Renewable %" | B4: `=AVERAGE(Raw_Data!K:K)`
   - A5: "Total Records" | B5: `=COUNTA(Raw_Data!A:A)`

2. Format KPI cells:
   - Select B1:B5
   - Apply **Bold** font
   - Set font size to **14**
   - Apply **Light Blue** fill color

### 6.3 Add Conditional Formatting
1. On the **Raw_Data** sheet, select the consumption column (H)
2. Go to **Home** tab → **Conditional Formatting** → **Color Scales**
3. Choose **Green-Yellow-Red** color scale
4. This will highlight high/low consumption values

5. Select the renewable_share_percent column (K)
6. Go to **Conditional Formatting** → **Color Scales**
7. Choose **Green-Yellow-Red** (higher renewable = greener)

### 6.4 Copy Charts to Dashboard
1. Copy the charts from Pivot_Analysis sheet
2. Paste them onto the Dashboard sheet
3. Arrange them neatly:
   - KPI cards at top
   - Column chart (State × Sector) on left
   - Line chart (Monthly trend) on right
   - Pie chart (Sector distribution) at bottom

---

## Step 7: Final Touches

### 7.1 Add Slicers (Optional - for interactivity)
1. Click on any pivot table
2. Go to **PivotTable Analyze** tab → **Insert Slicer**
3. Select **year** and **region**
4. Position slicers on the Dashboard sheet
5. Connect slicers to all pivot tables:
   - Right-click slicer → **Report Connections**
   - Check all pivot tables
   - Click **OK**

### 7.2 Protect Formulas (Optional)
1. Select all cells with formulas
2. Right-click → **Format Cells** → **Protection** tab
3. Uncheck **Locked** (to unlock them)
4. Click **OK**
5. Go to **Review** tab → **Protect Sheet**
6. Set a password if desired
7. This prevents accidental deletion of formulas

---

## Summary of Your Excel Dashboard

Your completed Excel workbook should have:
- **Raw_Data**: Cleaned dataset with merged reference data
- **State_Reference**: State mapping table
- **Pivot_Analysis**: Pivot tables for analysis
- **Dashboard**: Visual dashboard with KPIs and charts

You can now filter by year/region using slicers and see the data update dynamically!
