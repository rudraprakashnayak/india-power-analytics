import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="India Power Consumption Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 18px 20px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 1.7rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-subtitle {
        color: #38BDF8;
        font-size: 0.8rem;
        margin-top: 4px;
    }
    .badge-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Database Initialization & Data Loading
# ---------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_POWER = os.path.join(DATA_DIR, "power_consumption.csv")
CSV_STATES = os.path.join(DATA_DIR, "state_region_mapping.csv")
DB_PATH = os.path.join(DATA_DIR, "power_consumption.db")

@st.cache_resource
def get_database_connection():
    """Create or connect to SQLite database and ensure tables are populated."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='consumption_records'")
    if cursor.fetchone()[0] == 0:
        # Load schema
        schema_file = os.path.join(os.path.dirname(__file__), "sql", "schema.sql")
        if os.path.exists(schema_file):
            with open(schema_file, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())
        else:
            # Fallback schema
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS state_master (
                state_id INTEGER PRIMARY KEY AUTOINCREMENT,
                state TEXT NOT NULL UNIQUE,
                state_code TEXT NOT NULL UNIQUE,
                region TEXT NOT NULL,
                capital TEXT NOT NULL
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS consumption_records (
                record_id INTEGER PRIMARY KEY,
                state TEXT NOT NULL,
                region TEXT NOT NULL,
                sector TEXT NOT NULL,
                month TEXT NOT NULL,
                year INTEGER NOT NULL,
                consumption_units_mwh REAL NOT NULL,
                per_capita_consumption REAL NOT NULL,
                tariff_rate_per_unit REAL NOT NULL,
                renewable_share_percent REAL NOT NULL
            );
            """)
        
        # Populate from CSV
        if os.path.exists(CSV_STATES):
            df_states = pd.read_csv(CSV_STATES)
            df_states.to_sql("state_master", conn, if_exists="append", index=False)
            
        if os.path.exists(CSV_POWER):
            df_power = pd.read_csv(CSV_POWER)
            df_power.to_sql("consumption_records", conn, if_exists="append", index=False)
            
        conn.commit()
        
    return conn

@st.cache_data
def load_datasets():
    df_power = pd.read_csv(CSV_POWER)
    df_states = pd.read_csv(CSV_STATES)
    merged_df = pd.merge(df_power, df_states[["state", "state_code", "capital"]], on="state", how="left")
    
    # Month ordering helper
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    merged_df["month_num"] = merged_df["month"].map(lambda m: month_order.index(m) + 1 if m in month_order else 0)
    
    # Calculate revenue/billing proxy
    merged_df["estimated_revenue_cr"] = (merged_df["consumption_units_mwh"] * 1000 * merged_df["tariff_rate_per_unit"]) / 1e7
    return merged_df, df_states

# Initialize database and load datasets
conn = get_database_connection()
df_all, df_states_ref = load_datasets()

# ---------------------------------------------------------
# Sidebar Controls & Filters
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/electricity.png", width=64)
    st.title("⚡ Filter Analytics")
    st.markdown("Filter consumption data across regions, states, sectors, and years.")
    
    # Year Filter
    available_years = sorted(df_all["year"].unique())
    selected_year = st.selectbox(
        "📅 Select Year",
        options=["All Years"] + [str(y) for y in available_years],
        index=0
    )
    
    # Region Filter
    available_regions = sorted(df_all["region"].unique())
    selected_regions = st.multiselect(
        "📍 Geographic Region(s)",
        options=available_regions,
        default=available_regions
    )
    
    # Filter states dynamically based on selected regions
    if selected_regions:
        states_in_regions = sorted(df_all[df_all["region"].isin(selected_regions)]["state"].unique())
    else:
        states_in_regions = sorted(df_all["state"].unique())
        
    selected_states = st.multiselect(
        "🏛️ Specific States",
        options=states_in_regions,
        default=[]
    )
    
    # Sector Filter
    available_sectors = sorted(df_all["sector"].unique())
    selected_sectors = st.multiselect(
        "🏭 Consumer Sector(s)",
        options=available_sectors,
        default=available_sectors
    )
    
    st.markdown("---")
    st.markdown("### 📌 About Dataset")
    st.caption("**Coverage**: 16 Indian States across 5 regions\n\n**Period**: 2023 - 2025\n\n**Source**: Synthesized Indian Power Sector Database")
    
    if st.button("🔄 Reset Filters", use_container_width=True):
        st.rerun()

# ---------------------------------------------------------
# Filter Dataset
# ---------------------------------------------------------
df_filtered = df_all.copy()

if selected_year != "All Years":
    df_filtered = df_filtered[df_filtered["year"] == int(selected_year)]

if selected_regions:
    df_filtered = df_filtered[df_filtered["region"].isin(selected_regions)]

if selected_states:
    df_filtered = df_filtered[df_filtered["state"].isin(selected_states)]

if selected_sectors:
    df_filtered = df_filtered[df_filtered["sector"].isin(selected_sectors)]

if df_filtered.empty:
    st.warning("⚠️ No data matches the selected filter criteria. Please adjust your filters.")
    st.stop()

# ---------------------------------------------------------
# Top Header Banner
# ---------------------------------------------------------
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between;">
    <div>
        <div class="main-header">⚡ India Power Consumption Analytics Dashboard</div>
        <div class="sub-header">Comprehensive insights into electricity demand, seasonal trends, sectoral distribution, and renewable energy adoption across Indian states.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# KPI Metric Cards
# ---------------------------------------------------------
total_consumption = df_filtered["consumption_units_mwh"].sum()
avg_per_capita = df_filtered["per_capita_consumption"].mean()
avg_tariff = df_filtered["tariff_rate_per_unit"].mean()
avg_renewable = df_filtered["renewable_share_percent"].mean()
total_records = len(df_filtered)
active_states = df_filtered["state"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Consumption</div>
        <div class="metric-value">{total_consumption:,.1f}</div>
        <div class="metric-subtitle">MWh Across Selection</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Per Capita</div>
        <div class="metric-value">{avg_per_capita:.1f}</div>
        <div class="metric-subtitle">kWh per person</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Tariff Rate</div>
        <div class="metric-value">₹ {avg_tariff:.2f}</div>
        <div class="metric-subtitle">per unit (kWh)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Renewable Share</div>
        <div class="metric-value">{avg_renewable:.1f}%</div>
        <div class="metric-subtitle">Green Energy Penetration</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Scope / States</div>
        <div class="metric-value">{active_states} States</div>
        <div class="metric-subtitle">{total_records:,} Observations</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabbed Navigation
# ---------------------------------------------------------
tabs = st.tabs([
    "📊 Overview & Regional",
    "📈 Trend & Seasonality",
    "🏭 Sector Breakdown",
    "🗺️ State Comparisons & Green Energy",
    "💻 SQL Analytics & Data Explorer"
])

# Consistent Palette
COLOR_MAP = {
    "West": "#3B82F6",
    "South": "#10B981",
    "North": "#F59E0B",
    "East": "#8B5CF6",
    "Northeast": "#EC4899",
    "Industrial": "#3B82F6",
    "Residential": "#10B981",
    "Commercial": "#F59E0B",
    "Agricultural": "#EF4444"
}

# =========================================================
# TAB 1: OVERVIEW & REGIONAL
# =========================================================
with tabs[0]:
    st.subheader("Regional Consumption Disparity & Top Consumers")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        # Regional Share Donut
        region_df = df_filtered.groupby("region")["consumption_units_mwh"].sum().reset_index()
        fig_region = px.pie(
            region_df,
            names="region",
            values="consumption_units_mwh",
            title="⚡ Power Consumption Share by Region",
            hole=0.45,
            color="region",
            color_discrete_map=COLOR_MAP
        )
        fig_region.update_traces(textposition='inside', textinfo='percent+label')
        fig_region.update_layout(showlegend=False, margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_region, use_container_width=True)
        
    with col_b:
        # Top 10 States Consumption Bar
        top_states_df = df_filtered.groupby(["state", "region"])["consumption_units_mwh"].sum().reset_index()
        top_states_df = top_states_df.sort_values(by="consumption_units_mwh", ascending=True).tail(10)
        
        fig_states = px.bar(
            top_states_df,
            x="consumption_units_mwh",
            y="state",
            orientation="h",
            color="region",
            color_discrete_map=COLOR_MAP,
            title="🏆 Top States by Total Power Consumption (MWh)",
            labels={"consumption_units_mwh": "Total Consumption (MWh)", "state": "State"}
        )
        fig_states.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_states, use_container_width=True)

    # Regional Aggregation Table & Insights
    st.markdown("### 📋 Regional Performance Matrix")
    reg_summary = df_filtered.groupby("region").agg(
        Total_Consumption_MWh=("consumption_units_mwh", "sum"),
        Avg_Per_Capita_kWh=("per_capita_consumption", "mean"),
        Avg_Tariff_INR=("tariff_rate_per_unit", "mean"),
        Avg_Renewable_Pct=("renewable_share_percent", "mean"),
        States_Count=("state", "nunique")
    ).reset_index()
    
    reg_summary["Share_of_Total_Pct"] = (reg_summary["Total_Consumption_MWh"] / reg_summary["Total_Consumption_MWh"].sum()) * 100
    reg_summary = reg_summary.sort_values(by="Total_Consumption_MWh", ascending=False)
    
    formatted_reg = reg_summary.copy()
    formatted_reg["Total_Consumption_MWh"] = formatted_reg["Total_Consumption_MWh"].map("{:,.1f}".format)
    formatted_reg["Avg_Per_Capita_kWh"] = formatted_reg["Avg_Per_Capita_kWh"].map("{:.2f}".format)
    formatted_reg["Avg_Tariff_INR"] = formatted_reg["Avg_Tariff_INR"].map("₹ {:.2f}".format)
    formatted_reg["Avg_Renewable_Pct"] = formatted_reg["Avg_Renewable_Pct"].map("{:.1f}%".format)
    formatted_reg["Share_of_Total_Pct"] = formatted_reg["Share_of_Total_Pct"].map("{:.1f}%".format)
    
    st.dataframe(formatted_reg, use_container_width=True, hide_index=True)
    
    st.info("""
    💡 **Key Insights & Takeaways:**
    - **Industrial Hubs Dominate**: The Western region (Maharashtra & Gujarat) accounts for the largest share of national energy demand due to intensive manufacturing clusters.
    - **Green Energy Champions**: Southern states (Tamil Nadu, Karnataka, and Kerala) lead significantly in renewable energy generation share (>26%).
    - **Per-Capita Disparity**: Per-capita consumption in western industrialized states is over 2.5× higher than in northeastern states like Assam.
    """)

# =========================================================
# TAB 2: TREND & SEASONALITY
# =========================================================
with tabs[1]:
    st.subheader("Temporal Demand Curves & Seasonal Fluctuations")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        # Monthly trend across years
        month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        monthly_df = df_filtered.groupby(["year", "month", "month_num"])["consumption_units_mwh"].sum().reset_index()
        monthly_df = monthly_df.sort_values(by=["year", "month_num"])
        
        fig_trend = px.line(
            monthly_df,
            x="month",
            y="consumption_units_mwh",
            color="year",
            markers=True,
            title="📅 Monthly Consumption Trajectory by Year (MWh)",
            labels={"consumption_units_mwh": "Total Consumption (MWh)", "month": "Month"},
            category_orders={"month": month_order}
        )
        fig_trend.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_t2:
        # Sector monthly trend stacked area
        sec_monthly = df_filtered.groupby(["month", "month_num", "sector"])["consumption_units_mwh"].sum().reset_index()
        sec_monthly = sec_monthly.sort_values(by="month_num")
        
        fig_sec_trend = px.area(
            sec_monthly,
            x="month",
            y="consumption_units_mwh",
            color="sector",
            color_discrete_map=COLOR_MAP,
            title="🏭 Sector-wise Monthly Consumption Load (MWh)",
            labels={"consumption_units_mwh": "Consumption (MWh)", "month": "Month"},
            category_orders={"month": month_order}
        )
        fig_sec_trend.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_sec_trend, use_container_width=True)

    # YoY Annual Growth Rate
    st.markdown("### 📈 Year-over-Year Growth Comparison")
    yoy_df = df_all.groupby(["state", "year"])["consumption_units_mwh"].sum().unstack()
    if 2023 in yoy_df.columns and 2024 in yoy_df.columns:
        yoy_df["YoY_Growth_2023_2024_%"] = ((yoy_df[2024] - yoy_df[2023]) / yoy_df[2023]) * 100
        growth_display = yoy_df.reset_index().sort_values(by="YoY_Growth_2023_2024_%", ascending=False)
        
        fig_yoy = px.bar(
            growth_display,
            x="state",
            y="YoY_Growth_2023_2024_%",
            title="State-wise Annual Consumption Growth Rate (2023 to 2024)",
            labels={"YoY_Growth_2023_2024_%": "Growth Rate (%)", "state": "State"},
            color="YoY_Growth_2023_2024_%",
            color_continuous_scale="Viridis"
        )
        fig_yoy.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_yoy, use_container_width=True)

# =========================================================
# TAB 3: SECTOR BREAKDOWN
# =========================================================
with tabs[2]:
    st.subheader("Consumer Sector Dynamics & Tariff Structures")
    
    col_s1, col_s2 = st.columns([1, 1.3])
    
    with col_s1:
        sector_summary = df_filtered.groupby("sector").agg(
            Total_MWh=("consumption_units_mwh", "sum"),
            Avg_Tariff=("tariff_rate_per_unit", "mean"),
            Avg_Per_Capita=("per_capita_consumption", "mean")
        ).reset_index()
        
        fig_sec_pie = px.pie(
            sector_summary,
            names="sector",
            values="Total_MWh",
            hole=0.4,
            title="⚡ Total Electricity Consumption by Sector",
            color="sector",
            color_discrete_map=COLOR_MAP
        )
        fig_sec_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_sec_pie, use_container_width=True)
        
    with col_s2:
        # State vs Sector Stacked Bar
        state_sec = df_filtered.groupby(["state", "sector"])["consumption_units_mwh"].sum().reset_index()
        # Sort states by total consumption
        state_totals = state_sec.groupby("state")["consumption_units_mwh"].sum().sort_values(ascending=False).index
        
        fig_state_sec = px.bar(
            state_sec,
            x="state",
            y="consumption_units_mwh",
            color="sector",
            color_discrete_map=COLOR_MAP,
            title="🏛️ State-wise Sector Composition (MWh)",
            category_orders={"state": state_totals},
            labels={"consumption_units_mwh": "MWh", "state": "State"}
        )
        fig_state_sec.update_layout(xaxis_tickangle=-45, margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_state_sec, use_container_width=True)

    # Tariff Structure Analysis
    st.markdown("### 💰 Tariff Rate Comparison by Consumer Category")
    col_tar1, col_tar2 = st.columns([1, 1])
    
    with col_tar1:
        fig_tariff_bar = px.bar(
            sector_summary.sort_values(by="Avg_Tariff", ascending=False),
            x="sector",
            y="Avg_Tariff",
            color="sector",
            color_discrete_map=COLOR_MAP,
            title="Average Tariff Rate by Sector (₹ / kWh)",
            labels={"Avg_Tariff": "Tariff (₹/unit)", "sector": "Sector"},
            text_auto=".2f"
        )
        st.plotly_chart(fig_tariff_bar, use_container_width=True)
        
    with col_tar2:
        fig_box = px.box(
            df_filtered,
            x="sector",
            y="tariff_rate_per_unit",
            color="sector",
            color_discrete_map=COLOR_MAP,
            title="Tariff Distribution & Cross-State Variation (₹ / kWh)",
            labels={"tariff_rate_per_unit": "Tariff Rate (₹)", "sector": "Sector"}
        )
        st.plotly_chart(fig_box, use_container_width=True)

# =========================================================
# TAB 4: STATE COMPARISONS & GREEN ENERGY
# =========================================================
with tabs[3]:
    st.subheader("State-level Benchmarks, Tariffs, and Clean Energy Transition")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        # Renewable energy share leaderboard
        renew_df = df_filtered.groupby(["state", "region"])["renewable_share_percent"].mean().reset_index()
        renew_df = renew_df.sort_values(by="renewable_share_percent", ascending=True)
        
        fig_renew = px.bar(
            renew_df,
            x="renewable_share_percent",
            y="state",
            orientation="h",
            color="renewable_share_percent",
            color_continuous_scale="Greens",
            title="🌱 Clean Energy Adoption Leaderboard (% Renewable)",
            labels={"renewable_share_percent": "Renewable Share (%)", "state": "State"}
        )
        fig_renew.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_renew, use_container_width=True)
        
    with col_c2:
        # Scatter: Per-Capita vs Tariff with bubble size
        scatter_df = df_filtered.groupby(["state", "region"]).agg(
            Avg_Per_Capita=("per_capita_consumption", "mean"),
            Avg_Tariff=("tariff_rate_per_unit", "mean"),
            Total_MWh=("consumption_units_mwh", "sum"),
            Avg_Renewable=("renewable_share_percent", "mean")
        ).reset_index()
        
        fig_scatter = px.scatter(
            scatter_df,
            x="Avg_Per_Capita",
            y="Avg_Tariff",
            size="Total_MWh",
            color="region",
            color_discrete_map=COLOR_MAP,
            hover_name="state",
            hover_data={"Avg_Renewable": ":.1f%"},
            title="🎯 Per-Capita Consumption vs Average Tariff Rate",
            labels={"Avg_Per_Capita": "Avg Per-Capita (kWh)", "Avg_Tariff": "Avg Tariff (₹/unit)"}
        )
        fig_scatter.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_scatter, use_container_width=True)

    # State Deep Dive Card
    st.markdown("---")
    st.markdown("### 🔍 Individual State Spotlight")
    spotlight_state = st.selectbox("Select State for Detailed Dossier:", options=sorted(df_all["state"].unique()))
    
    state_sub = df_all[df_all["state"] == spotlight_state]
    st_meta = df_states_ref[df_states_ref["state"] == spotlight_state].iloc[0]
    
    col_meta1, col_meta2, col_meta3, col_meta4 = st.columns(4)
    with col_meta1:
        st.metric("State Code & Capital", f"{st_meta['state_code']} - {st_meta['capital']}")
    with col_meta2:
        st.metric("Region", st_meta['region'])
    with col_meta3:
        st.metric("Total Historical MWh", f"{state_sub['consumption_units_mwh'].sum():,.1f}")
    with col_meta4:
        st.metric("Avg Renewable Share", f"{state_sub['renewable_share_percent'].mean():.1f}%")
        
    # State sector chart
    st_sec_pie = px.pie(
        state_sub.groupby("sector")["consumption_units_mwh"].sum().reset_index(),
        names="sector",
        values="consumption_units_mwh",
        title=f"Sector Distribution in {spotlight_state}",
        color="sector",
        color_discrete_map=COLOR_MAP,
        hole=0.35
    )
    st.plotly_chart(st_sec_pie, use_container_width=True)

# =========================================================
# TAB 5: SQL ANALYTICS LAB & DATA EXPLORER
# =========================================================
with tabs[4]:
    st.subheader("Interactive SQL Analytics Lab (SQLite 3)")
    st.markdown("Execute analytical queries directly against the relational `power_consumption.db` database.")
    
    PRESET_QUERIES = {
        "Query 1: Top 5 States by Total Consumption": """SELECT 
    state,
    region,
    ROUND(SUM(consumption_units_mwh), 2) as total_consumption_mwh,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff
FROM consumption_records
GROUP BY state, region
ORDER BY total_consumption_mwh DESC
LIMIT 5;""",

        "Query 2: Year-over-Year Consumption Growth by State": """SELECT 
    state,
    year,
    ROUND(SUM(consumption_units_mwh), 2) as annual_consumption_mwh,
    ROUND(SUM(consumption_units_mwh) * 100.0 / LAG(SUM(consumption_units_mwh)) OVER (PARTITION BY state ORDER BY year) - 100, 2) as yoy_growth_percent
FROM consumption_records
GROUP BY state, year
ORDER BY state, year;""",

        "Query 3: Sector-wise Consumption Split": """SELECT 
    sector,
    ROUND(SUM(consumption_units_mwh), 2) as total_consumption_mwh,
    ROUND(SUM(consumption_units_mwh) * 100.0 / (SELECT SUM(consumption_units_mwh) FROM consumption_records), 2) as percentage_share,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita
FROM consumption_records
GROUP BY sector
ORDER BY total_consumption_mwh DESC;""",

        "Query 4: Seasonal Trend - Monthly Average Across Years": """SELECT 
    month,
    ROUND(AVG(consumption_units_mwh), 2) as avg_consumption_mwh,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff
FROM consumption_records
GROUP BY month
ORDER BY 
    CASE month
        WHEN 'January' THEN 1 WHEN 'February' THEN 2 WHEN 'March' THEN 3
        WHEN 'April' THEN 4 WHEN 'May' THEN 5 WHEN 'June' THEN 6
        WHEN 'July' THEN 7 WHEN 'August' THEN 8 WHEN 'September' THEN 9
        WHEN 'October' THEN 10 WHEN 'November' THEN 11 WHEN 'December' THEN 12
    END;""",

        "Query 5: States with Highest Renewable Energy Share": """SELECT 
    state,
    region,
    ROUND(AVG(renewable_share_percent), 2) as avg_renewable_percent,
    ROUND(SUM(consumption_units_mwh), 2) as total_consumption_mwh
FROM consumption_records
GROUP BY state, region
ORDER BY avg_renewable_percent DESC
LIMIT 10;""",

        "Query 6: Per-Capita Consumption Ranking by State": """SELECT 
    state,
    region,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita_consumption,
    ROUND(SUM(consumption_units_mwh), 2) as total_consumption_mwh
FROM consumption_records
GROUP BY state, region
ORDER BY avg_per_capita_consumption DESC;""",

        "Query 7: Tariff vs Consumption Correlation by State": """SELECT 
    state,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff,
    ROUND(SUM(consumption_units_mwh), 2) as total_consumption_mwh,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita
FROM consumption_records
GROUP BY state
ORDER BY avg_tariff DESC;""",

        "Query 8: Region-wise Summary": """SELECT 
    region,
    COUNT(DISTINCT state) as num_states,
    ROUND(SUM(consumption_units_mwh), 2) as total_consumption_mwh,
    ROUND(SUM(consumption_units_mwh) * 100.0 / (SELECT SUM(consumption_units_mwh) FROM consumption_records), 2) as regional_share_percent,
    ROUND(AVG(per_capita_consumption), 2) as avg_per_capita,
    ROUND(AVG(renewable_share_percent), 2) as avg_renewable_percent
FROM consumption_records
GROUP BY region
ORDER BY total_consumption_mwh DESC;""",

        "Query 9: Top 5 States by Industrial Consumption": """SELECT 
    state,
    region,
    ROUND(SUM(consumption_units_mwh), 2) as industrial_consumption_mwh,
    ROUND(AVG(tariff_rate_per_unit), 2) as avg_tariff
FROM consumption_records
WHERE sector = 'Industrial'
GROUP BY state, region
ORDER BY industrial_consumption_mwh DESC
LIMIT 5;""",

        "Query 10: Monthly Consumption Trend by Sector": """SELECT 
    month,
    sector,
    ROUND(AVG(consumption_units_mwh), 2) as avg_consumption_mwh
FROM consumption_records
GROUP BY month, sector
ORDER BY 
    CASE month
        WHEN 'January' THEN 1 WHEN 'February' THEN 2 WHEN 'March' THEN 3
        WHEN 'April' THEN 4 WHEN 'May' THEN 5 WHEN 'June' THEN 6
        WHEN 'July' THEN 7 WHEN 'August' THEN 8 WHEN 'September' THEN 9
        WHEN 'October' THEN 10 WHEN 'November' THEN 11 WHEN 'December' THEN 12
    END,
    sector;"""
    }
    
    selected_query_title = st.selectbox("Select SQL Query to Run:", options=list(PRESET_QUERIES.keys()))
    query_code = PRESET_QUERIES[selected_query_title]
    
    query_input = st.text_area("SQL Code (Editable):", value=query_code, height=140)
    
    if st.button("▶️ Execute SQL Query", type="primary"):
        try:
            res_df = pd.read_sql_query(query_input, conn)
            st.success(f"Query returned {len(res_df)} rows successfully.")
            st.dataframe(res_df, use_container_width=True)
            
            # Auto-visualize if numeric columns exist
            numeric_cols = res_df.select_dtypes(include=[np.number]).columns.tolist()
            text_cols = res_df.select_dtypes(include=['object']).columns.tolist()
            
            if len(text_cols) >= 1 and len(numeric_cols) >= 1:
                auto_bar = px.bar(
                    res_df,
                    x=text_cols[0],
                    y=numeric_cols[0],
                    title=f"Chart: {text_cols[0].title()} vs {numeric_cols[0].title()}",
                    color=numeric_cols[0],
                    color_continuous_scale="Blues"
                )
                st.plotly_chart(auto_bar, use_container_width=True)
        except Exception as e:
            st.error(f"SQL Error: {e}")
            
    st.markdown("---")
    st.markdown("### 📥 Raw Data Explorer & Export")
    st.dataframe(df_filtered.drop(columns=["month_num", "estimated_revenue_cr"], errors="ignore"), use_container_width=True)
    
    csv_bytes = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="filtered_power_consumption.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem;">
    ⚡ <b>India Power Consumption Analytics</b> | Built with Streamlit, Plotly & SQLite | Author: <b>Rudra Prakash Nayak</b>
</div>
""", unsafe_allow_html=True)
