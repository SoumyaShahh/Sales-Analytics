# 🛒 Store Sales Performance Analytics | Power BI

**Author:** Soumya Shah | [GitHub](https://github.com/SoumyaShahh)

> An end-to-end retail analytics project processing **$39.2M in revenue** across **151 stores**, **9 agents**, and **47 states** (2018–2022) — built with Python for data preprocessing & EDA, SQL for analytical queries, and Power BI for interactive dashboards.

---

## 📌 Project Overview

This project transforms raw multi-table retail sales data into a full analytics stack — from Python-based data merging and EDA through SQL-based analysis to a production-ready Power BI dashboard. It enables store managers, regional directors, and sales leadership to monitor performance, identify top agents, optimize product strategy, and track shipping efficiency across the US.

---

## 🔢 Key Metrics

| Metric | Value |
|---|---|
| Total Revenue | **$39,202,329** |
| Total Profit | **$11,131,000** |
| Profit Margin | **28.4%** |
| Total Orders | 14,059 |
| Stores | 151 |
| States Covered | 47 |
| Regions | 4 (North, South, East, West) |
| Sales Agents | 9 |
| Products | 246 across 8 categories |
| Customers | 6,954 |
| Time Period | 2018 – 2022 |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Analytics Pipeline                        │
│                                                              │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │  Raw Excel  │    │   Python     │    │     SQL        │  │
│  │  5 tables   │───▶│  Merge + EDA │───▶│  12 Analytical │  │
│  │  14K rows   │    │  + KPIs      │    │  Queries       │  │
│  └─────────────┘    └──────────────┘    └───────┬────────┘  │
│                                                  │           │
│                                                  ▼           │
│                                       ┌─────────────────┐   │
│                                       │    Power BI      │   │
│                                       │  2 Dashboards    │   │
│                                       │  DAX Measures    │   │
│                                       │  Dynamic Filters │   │
│                                       └─────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Data Sources | Microsoft Excel (5 tables — Sales, Products, Agents, Locations, Stores) |
| Preprocessing & EDA | Python (Pandas, NumPy) |
| Analytical Queries | SQL (12 queries — KPIs, trends, rankings, outlier detection) |
| BI Dashboard | Power BI Desktop |
| Data Modeling | Star Schema (Fact + 5 Dimension tables) |
| Calculations | DAX (KPIs, calculated measures, dynamic filters) |
| Data Transformation | Power Query |

---

## 📊 Dashboard Previews

### Dashboard 1 — Revenue, Profit & Agent Performance
![Sales Analytics Dashboard 1](Sales%20Analytics%20Dashboard-1.png)

### Dashboard 2 — Geographic Revenue & Agent Rankings
![Sales Analytics Dashboard 2](Sales%20Analytics%20Dashboard-2.png)

---

## 📁 Data Model — Star Schema

```
Sales (Fact Table — 14,059 records)
    ├── Customers    (Dim) — 6,954 unique customers
    ├── Products     (Dim) — 246 products, 8 categories
    ├── Stores       (Dim) — 151 stores
    ├── Sales Agents (Dim) — 9 agents
    └── Locations    (Dim) — 47 states, 4 regions
```

---

## 🐍 Python Analysis (`analysis.py`)

Performs end-to-end data loading, merging, cleaning, and EDA across all 5 source tables:

```python
# Key outputs:
Total Revenue:     $39,202,329
Total Profit:      $11,131,000
Profit Margin:          28.4%
Avg Order Value:       $2,789
Avg Shipping Days:        14.2
```

**Run it:**
```bash
pip install pandas numpy openpyxl
python analysis.py
```

---

## 🗄️ SQL Queries (`queries.sql`)

12 analytical queries covering the full business picture:

| Query | Purpose |
|---|---|
| Overall KPIs | Revenue, profit, margin, shipping efficiency |
| Regional Performance | Revenue share and margin by region |
| Agent Rankings | Revenue, profit, and rank by agent |
| Product Categories | Revenue and profitability by category |
| YoY Growth | Year-over-year revenue trend with growth % |
| Monthly Trends | Monthly revenue and profit breakdown |
| Top 10 Products | Highest revenue-generating products |
| High-Value Customers | Top 20 customers by lifetime value |
| Shipping Efficiency | Avg/min/max shipping days by region |
| Agent × Region | Cross-analysis of agents across regions |
| Quarterly Breakdown | Q1-Q4 performance by year |
| Store Outliers | Below-average margin stores flagged |

---

## 💡 Key Insights

| Insight | Business Impact |
|---|---|
| **Jessica Diaz** — $7.8M, 19.9% of revenue | Top agent driving nearly 1 in 5 revenue dollars |
| **North & South** = 65.6% of total revenue | Resource and headcount should prioritize these regions |
| **2021 revenue spiked to $17.6M** vs $5.3M avg | Post-pandemic recovery — key planning benchmark |
| **28.4% consistent profit margin** across all agents | Healthy margins regardless of volume |
| **Tamara Caldwell** — highest margin at 29.1% | Most cost-efficient agent despite lower volume |
| **Toys & Games + Outdoor** — highest order volume | Top categories for inventory prioritization |

---

## 🔍 Dashboard Modules

**Store Sales Performance Overview**
Revenue and profit summaries with dynamic drill-down by agent, region, category, and time.

**Agent Performance Rankings**
9 agents ranked by revenue and margin — enables targeted coaching and incentive planning.

**Product & Category Analysis**
246 products across 8 categories — identifies high-margin vs high-volume products.

**Regional Revenue Distribution**
4-region breakdown with state-level granularity across 47 states.

**Time Series Analysis**
Monthly and annual trends 2018–2022 — 2021 peak at $17.6M reveals post-pandemic recovery pattern.

**Shipping Efficiency**
Order volume vs. average shipping time by region — identifies operational bottlenecks.

---

## 📁 Repository Structure

```
Sales-Analytics/
├── analysis.py                      # Python EDA — merge, clean, KPIs
├── queries.sql                      # 12 SQL analytical queries
├── Sales Analytics Dashboard-1.png  # Revenue & agent performance
├── Sales Analytics Dashboard-2.png  # Geographic & agent rankings
└── README.md
```

---

*Built by Soumya Shah | [GitHub](https://github.com/SoumyaShahh)*
