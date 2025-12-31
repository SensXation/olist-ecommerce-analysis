import streamlit as st
import pandas as pd
import toml
from sqlalchemy import create_engine, text
import plotly.express as px

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(page_title="Olist Executive Dashboard", layout="wide")

# Load Secrets (Securely)
try:
    secrets = toml.load(".streamlit/secrets.toml")
    DB_URL = secrets["database"]["url"]
except Exception as e:
    st.error(f"❌ Error loading secrets: {e}")
    st.stop()

# Cache the database connection (so we don't reconnect every time we click a button)
@st.cache_resource
def get_engine():
    return create_engine(DB_URL)

engine = get_engine()

# --- 2. SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
# We'll fetch the available states from the DB to populate the filter
with engine.connect() as conn:
    states = pd.read_sql("SELECT DISTINCT customer_state FROM analytics_orders ORDER BY customer_state", conn)
    
selected_states = st.sidebar.multiselect(
    "Select States", 
    options=states['customer_state'].unique(),
    default=states['customer_state'].unique()[:5] # Default to first 5
)

if not selected_states:
    st.warning("Please select at least one state.")
    st.stop()

# --- 3. MAIN DASHBOARD ---
st.title("🇧🇷 Olist E-Commerce Executive Dashboard")
st.markdown("Live view of order performance from the **Enterprise Data Warehouse**.")

# A. KEY PERFORMANCE INDICATORS (KPIs)
# We write SQL to calculate these aggregations instantly
kpi_query = text(f"""
    SELECT 
        COUNT(order_id) as total_orders,
        SUM(total_order_value) as total_revenue,
        AVG(total_order_value) as avg_order_value
    FROM analytics_orders
    WHERE customer_state IN :states
""")

with engine.connect() as conn:
    # We pass the python list `selected_states` safely into the SQL query
    kpi_data = pd.read_sql(kpi_query, conn, params={"states": tuple(selected_states)})

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", f"{kpi_data['total_orders'][0]:,}")
col2.metric("Total Revenue", f"R$ {kpi_data['total_revenue'][0]:,.2f}")
col3.metric("Avg Order Value", f"R$ {kpi_data['avg_order_value'][0]:,.2f}")

st.divider()

# B. REVENUE BY STATE (Bar Chart)
col_chart, col_map = st.columns([2, 1])

with col_chart:
    st.subheader("Revenue by State")
    chart_query = text(f"""
        SELECT customer_state, SUM(total_order_value) as revenue
        FROM analytics_orders
        WHERE customer_state IN :states
        GROUP BY customer_state
        ORDER BY revenue DESC
        LIMIT 10
    """)
    
    with engine.connect() as conn:
        chart_data = pd.read_sql(chart_query, conn, params={"states": tuple(selected_states)})
        
    fig = px.bar(
        chart_data, 
        x="customer_state", 
        y="revenue",
        color="revenue",
        title="Top 10 States by Revenue",
        labels={"revenue": "Revenue (R$)", "customer_state": "State"}
    )
    st.plotly_chart(fig, use_container_width=True)

# C. TOP PAYMENT METHODS (Pie Chart)
with col_map:
    st.subheader("Payment Methods")
    # This requires a bit of string parsing since we aggregated them, 
    # but for a dashboard, we can query the raw payments table if we wanted.
    # For now, let's just query the simplified view.
    payment_query = text(f"""
        SELECT payment_types, count(*) as count
        FROM analytics_orders
        WHERE customer_state IN :states
        GROUP BY payment_types
        ORDER BY count DESC
        LIMIT 5
    """)
    
    with engine.connect() as conn:
        payment_data = pd.read_sql(payment_query, conn, params={"states": tuple(selected_states)})
        
    fig_pie = px.pie(payment_data, values='count', names='payment_types', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# D. RECENT LARGE ORDERS (Data Grid)
st.subheader("🔍 Recent High-Value Orders (> R$ 500)")
raw_data_query = text(f"""
    SELECT order_id, customer_city, customer_state, total_order_value, payment_types
    FROM analytics_orders
    WHERE customer_state IN :states
    AND total_order_value > 500
    ORDER BY total_order_value DESC
    LIMIT 100
""")

with engine.connect() as conn:
    orders_df = pd.read_sql(raw_data_query, conn, params={"states": tuple(selected_states)})

st.dataframe(orders_df, use_container_width=True)