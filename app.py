import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# Base API URL
API_URL = "http://localhost:8000"

# Streamlit Page Config
st.set_page_config(page_title="E-commerce KPI Dashboard", layout="wide")

# Title
st.title("📊 E-commerce KPI Dashboard")

# Sidebar Filters
years = requests.get(f"{API_URL}/years").json()
selected_year = st.sidebar.selectbox("Select Year", ["All"] + years)

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
        return []


# Display Metrics
with st.spinner("Fetching data..."):
    # Create Layout
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    # Fetch Data for KPIs
    total_sales = fetch_data("total_sales", {"year": selected_year if selected_year != "All" else None})
    total_profits = fetch_data("total_profits", {"year": selected_year if selected_year != "All" else None})
    total_orders = fetch_data("total_orders", {"year": selected_year if selected_year != "All" else None})
    total_quantity = fetch_data("total_quantity", {"year": selected_year if selected_year != "All" else None})
    total_clients = fetch_data("total_client", {"year": selected_year if selected_year != "All" else None})
    avg_orders_by_customers = fetch_data("average_orders_by_customers", {"year": selected_year if selected_year != "All" else None})

    # Display KPIs
    col1.metric("💰 Total Sales", f"${total_sales[0].get('totalSales', 0):,.2f}" if total_sales else "N/A")
    col2.metric("💸 Total Profits", f"${total_profits[0].get('totalProfit', 0):,.2f}" if total_profits else "N/A")
    col3.metric("🛒 Total Orders", total_orders[0].get("Order ID", 0) if total_orders else "N/A")
    col4.metric("📦 Total Quantity", total_quantity[0].get("totalQuantity", 0) if total_quantity else "N/A")
    col5.metric("👥 Total Clients", total_clients[0].get("Customers ID", 0) if total_clients else "N/A")
    col6.metric("📈 Avg Orders/Customer", f"{avg_orders_by_customers[0].get('averageOrdersPerCustomer', 0):.2f}" if avg_orders_by_customers else "N/A")

    # Charts Section
    st.subheader("📊 Data Visualizations")

    # Revenue by Category
    revenue_by_category = fetch_data("revenue_by_category", {"year": selected_year if selected_year != "All" else None})
    if revenue_by_category:
        df = pd.DataFrame(revenue_by_category)
        fig = px.bar(df, x="_id", y="totalSales", title="Revenue by Category", color="totalSales")
        st.plotly_chart(fig, use_container_width=True)

    total_orders_by_category = fetch_data("total_orders_by_category", {"year": selected_year if selected_year != "All" else None})
    if total_orders_by_category:
        df = pd.DataFrame(total_orders_by_category)
        fig = px.bar(df, x="_id", y="totalOrders", title="Total Orders by Category", color="totalOrders")
        st.plotly_chart(fig, use_container_width=True)

    quantity_by_category = fetch_data("quantity_by_category", {"year": selected_year if selected_year != "All" else None})
    if quantity_by_category:
        df = pd.DataFrame(quantity_by_category)
        fig = px.bar(df, x="_id", y="totalQuantity", title="Quantity by Category", color="totalQuantity")
        st.plotly_chart(fig, use_container_width=True)

    # Revenue by Customer
    revenue_by_customer = fetch_data("revenue_by_customer", {"year": selected_year if selected_year != "All" else None})
    if revenue_by_customer:
        df = pd.DataFrame(revenue_by_customer)
        fig = px.bar(df, x="_id", y="totalSales", title="Revenue by Customer", color="totalSales")
        st.plotly_chart(fig, use_container_width=True)

    # Total Orders by Customer
    total_orders_per_customer = fetch_data("total_orders_per_customer", {"year": selected_year if selected_year != "All" else None})
    if total_orders_per_customer:
        df = pd.DataFrame(total_orders_per_customer)
        fig = px.bar(df, x="_id", y="totalOrders", title="Total Orders by Customer", color="totalOrders")
        st.plotly_chart(fig, use_container_width=True)

    # Quantity per Customer
    quantity_per_customer = fetch_data("quantity_per_customer", {"year": selected_year if selected_year != "All" else None})
    if quantity_per_customer:
        df = pd.DataFrame(quantity_per_customer)
        fig = px.bar(df, x="_id", y="totalQuantity", title="Quantity per Customer", color="totalQuantity")
        st.plotly_chart(fig, use_container_width=True)

    # Retention by Customers
    retention_by_customers = fetch_data("retention_by_customers", {"year": selected_year if selected_year != "All" else None})
    if retention_by_customers:
        df = pd.DataFrame(retention_by_customers)
        fig = px.scatter(df, x="_id", y="retentionPeriodDays", title="Retention by Customers")
        st.plotly_chart(fig, use_container_width=True)
