# CFPB Analytics Dashboard

**A high-performance interactive dashboard for exploring Consumer Financial Protection Bureau (CFPB) complaint data. This application runs locally to visualize trends, company performance, and product friction points.**

---

## 📖 Dashboard Overview

This dashboard serves as the front-end layer for the CFPB ELT pipeline. It is designed to help analysts and stakeholders answer key questions:
* **Macro Trends:** How is complaint volume changing over time?
* **Company Benchmarking:** Which companies handle complaints most effectively?
* **Root Cause Analysis:** What specific products or issues are causing consumer friction?
* **Geographic Distribution:** Where are complaints originating from?

---

## 📊 Page Guide

Below is a breakdown of each page in the dashboard. You can insert screenshots in the placeholders provided.

### 1. Home (Landing Page)
The central navigation hub that introduces the available analysis modules.
* **Function:** Routes users to specific analytical contexts.
* **Key Elements:** Overview cards for Executive, Company, Product, and Geographic modules.

<img src="../images/dashboard/Home.png" width="800" alt="Home Page Screenshot">

### 2. Executive Summary (`1_Executive_Summary.py`)
A high-level view for decision-makers to monitor overall system health.
* **Key Metrics (KPIs):** Total Complaints, Timely Response Rate, and Consumer Disputed Rate.
* **Visualizations:** * **Volume Trends:** Time-series charts showing complaint spikes over time.
    * **Response Breakdown:** Donut chart showing how companies are closing tickets (e.g., "Closed with explanation").

<img src="../images/dashboard/1_Executive_Summary.png" width="800" alt="Executive Summary Screenshot">

### 3. Company Performance (`2_Company_Performance.py`)
A benchmarking tool to compare financial institutions against one another.
* **Leaderboard:** Ranks companies by total complaint volume.
* **Performance Matrix:** A scatter plot analyzing the relationship between **Complaint Volume** and **Timeliness**. This helps identify companies that are overwhelmed vs. those that are efficient.

<img src="../images/dashboard/2_Company_Performance.png" width="800" alt="Company Performance Screenshot">

### 4. Product Friction Points (`3_Product_Issues.py`)
A deep-dive tool for Product Managers to identify root causes.
* **Focus:** Breaks down complaints by specific Products (e.g., "Credit Card", "Mortgage").
* **Issue Analysis:** visualizes the most common specific issues (e.g., "Trouble during payment process") to help prioritize fixes.

<img src="../images/dashboard/3_Product_Issues.png" width="800" alt="Product Issues Screenshot">

### 5. Geographic Trends (`4_Geographic_Trends.py`)
A regional analysis of consumer sentiment and submission channels.
* **Channel Analysis:** Breakdown of how users submitted complaints (Web, Phone, Referral).
* **Regional Heatmaps:** Visualizes complaint density across different states to identify regional hotspots.

<img src="../images/dashboard/4_Geographic_Trends.png" width="800" alt="Geographic Trends Screenshot">

---

## 🚀 How to Run

**Prerequisite:** This guide assumes you have already run the data extraction pipeline and the `cfpb_complaints.duckdb` database file exists in the `database/` folder.

### Step 1: Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### Step 2: Install dependencies:

```bash
uv sync
```

### Step 3: Running the dashboard

```bash
uv run streamlit run app/dashboard/Home.py
```