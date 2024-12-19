import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# Base API URL
API_URL = "http://localhost:8000"

# Streamlit Page Config
st.set_page_config(page_title="E-commerce KPI Dashboard", layout="wide")

@st.cache_data(ttl=600, show_spinner=False)
def fetch_data(endpoint, year):
    params = {"year": year if year != "All" else None}
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
        return []

@st.cache_data(ttl=600, show_spinner=False)
def render_chart(data, x_col, y_col, title, chart_type="bar"):
    if data:
        df = pd.DataFrame(data)
        if chart_type == "bar":
            fig = px.bar(df, x=x_col, y=y_col, title=title, color=y_col)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col, title=title)
        st.plotly_chart(fig, use_container_width=True)

# Sidebar Filters
years = requests.get(f"{API_URL}/years").json()
selected_year = st.sidebar.selectbox("Select Year", ["All"] + years)

# Page Navigation
page = st.sidebar.radio("Navigation", ("Global KPIs", "Customers", "Products"))

if page == "Global KPIs":
    st.title("📊 Global KPIs Dashboard")

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    total_sales = fetch_data("total_sales", selected_year)
    total_profits = fetch_data("total_profits", selected_year)
    total_orders = fetch_data("total_orders", selected_year)
    total_quantity = fetch_data("total_quantity", selected_year)
    total_clients = fetch_data("total_client", selected_year)
    avg_orders_by_customers = fetch_data("average_orders_by_customers", selected_year)

    col1.metric("💰 Total Sales", f"${total_sales[0].get('totalSales', 0):,.2f}" if total_sales else "N/A")
    col2.metric("💸 Total Profits", f"${total_profits[0].get('totalProfit', 0):,.2f}" if total_profits else "N/A")
    col3.metric("🛒 Total Orders", total_orders[0].get("Order ID", 0) if total_orders else "N/A")
    col4.metric("📦 Total Quantity", total_quantity[0].get("totalQuantity", 0) if total_quantity else "N/A")
    col5.metric("👥 Total Clients", total_clients[0].get("Customers ID", 0) if total_clients else "N/A")
    col6.metric("📈 Avg Orders/Customer", f"{avg_orders_by_customers[0].get('averageOrdersPerCustomer', 0):.2f}" if avg_orders_by_customers else "N/A")

elif page == "Customers":
    st.title("👥 Customers Dashboard")

    render_chart(fetch_data("revenue_by_customer", selected_year), "_id", "totalSales", "Revenue by Customer")
    render_chart(fetch_data("total_orders_per_customer", selected_year), "_id", "totalOrders", "Total Orders by Customer")
    render_chart(fetch_data("quantity_per_customer", selected_year), "_id", "totalQuantity", "Quantity per Customer")
    render_chart(fetch_data("retention_by_customers", selected_year), "_id", "retentionPeriodDays", "Retention by Customers", chart_type="scatter")

elif page == "Products":
    st.title("🛍️ Products Dashboard")

    render_chart(fetch_data("revenue_by_category", selected_year), "_id", "totalSales", "Revenue by Category")
    render_chart(fetch_data("total_orders_by_category", selected_year), "_id", "totalOrders", "Total Orders by Category")
    render_chart(fetch_data("quantity_by_category", selected_year), "_id", "totalQuantity", "Quantity by Category")
