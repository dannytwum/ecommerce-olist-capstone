import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Olist Analytics", page_icon="🛒", layout="wide")
st.title("🛒 Olist E-Commerce Analytics Dashboard")
st.markdown("**Thrive Data Science Capstone 2026 — Group [Your Number]**")

# Connect to your local database
con = duckdb.connect("project.duckdb")

# --- Monthly Revenue ---
st.header("📈 Monthly Revenue Trend")
try:
    monthly = con.sql("""
        WITH monthly AS (
            SELECT DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
                   SUM(oi.price + oi.freight_value) AS revenue
            FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.order_status = 'delivered'
            GROUP BY 1
        )
        SELECT month, revenue, SUM(revenue) OVER (ORDER BY month) AS running_total
        FROM monthly ORDER BY month
    """).df()

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(monthly["month"], monthly["revenue"], color="steelblue", alpha=0.8)
    ax.set_title("Monthly Revenue (Delivered Orders)")
    ax.set_xlabel("Month"); ax.set_ylabel("Revenue (BRL)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"R${monthly['revenue'].sum():,.0f}")
    col2.metric("Peak Month Revenue", f"R${monthly['revenue'].max():,.0f}")
    col3.metric("Total Months", len(monthly))
except Exception as e:
    st.error(f"Could not load Monthly Revenue. Error: {e}")

# --- Customer Tiers ---
st.header("👥 Customer Value Tiers")
try:
    tiers = con.sql("""
        WITH spend AS (
            SELECT c.customer_unique_id, SUM(oi.price + oi.freight_value) AS total_spend
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.order_status = 'delivered' 
            GROUP BY c.customer_unique_id
        ),
        ranked_spend AS (
            SELECT total_spend,
                   CASE NTILE(4) OVER (ORDER BY total_spend DESC)
                       WHEN 1 THEN 'Tier 1 — Top Spenders'
                       WHEN 2 THEN 'Tier 2 — High Spenders'
                       WHEN 3 THEN 'Tier 3 — Mid Spenders'
                       WHEN 4 THEN 'Tier 4 — Low Spenders' 
                   END AS tier
            FROM spend
        )
        SELECT tier, 
               COUNT(*) AS customers, 
               ROUND(AVG(total_spend), 2) AS avg_spend
        FROM ranked_spend 
        GROUP BY tier 
        ORDER BY tier
    """).df()
    st.dataframe(tiers, use_container_width=True)
except Exception as e:
    st.error(f"Could not load Customer Tiers. Error: {e}")

# --- Top Categories ---
st.header("🏆 Top Product Categories")
try:
    top_cats = con.sql("""
        SELECT COALESCE(t.product_category_name_english, p.product_category_name) AS category,
               ROUND(SUM(oi.price + oi.freight_value),2) AS revenue,
               COUNT(DISTINCT oi.order_id) AS orders
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
        GROUP BY 1 ORDER BY 2 DESC LIMIT 10
    """).df()

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.barh(top_cats["category"], top_cats["revenue"], color="coral")
    ax2.set_title("Top 10 Categories by Revenue")
    ax2.set_xlabel("Revenue (BRL)")
    ax2.invert_yaxis()
    st.pyplot(fig2)
except Exception as e:
    st.error(f"Could not load Top Categories. Error: {e}")

st.markdown("---")
st.caption("Built with DuckDB · Python · Streamlit | Thrive Capstone 2026")