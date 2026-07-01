# 🛒 E-Commerce Analytics — Olist Capstone

## Business Question
Who are our best customers, why do deliveries slip, 
and which sellers and categories drive growth?

## Dataset
Olist Brazilian E-Commerce — 9 related tables, ~100k orders (2016–2018)  
Source: kaggle.com/datasets/olistbr/brazilian-ecommerce

## Pipeline
Raw CSVs → DuckDB → SQL Transforms → Analysis → ML Model → Dashboard

## Key Findings
- Top 25% of customers (Tier 1) generate the majority of revenue
- Late deliveries strongly correlate with lower review scores
- A small number of product categories drive most revenue
- Logistic Regression outperforms baseline in predicting late deliveries

## Recommendation
1. Launch a loyalty programme for Tier 1 customers
2. Fix logistics in high-risk delivery corridors
3. Focus marketing on top-performing categories

## How to Run
1. Install requirements: `pip install -r requirements.txt`
2. Upload Olist CSVs into `olist/` folder
3. Open and run `01_ecommerce_olist_STARTER.ipynb` top to bottom

## Tech Stack
- Python · DuckDB · pandas · scikit-learn · matplotlib · Streamlit

## Team
Group [your group number] — Thrive Data Science Capstone, 2026