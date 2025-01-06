import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# Base API URL
API_URL = "http://localhost:8000"

# Streamlit Page Config
st.set_page_config(page_title="E-commerce KPI Dashboard", layout="wide")


# Caching Data Fetching
@st.cache_data(ttl=600, show_spinner=False)
def fetch_data(endpoint, year):
    params = {"year": year if year != "All" else None}
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
        return []


# Caching Chart Rendering
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


    @st.cache_data(ttl=600, show_spinner=False)
    def get_global_kpis(year):
        return {
            "total_sales": fetch_data("total_sales", year),
            "total_profits": fetch_data("total_profits", year),
            "total_orders": fetch_data("total_orders", year),
            "total_quantity": fetch_data("total_quantity", year),
            "total_clients": fetch_data("total_client", year),
            "avg_orders_by_customers": fetch_data("average_orders_by_customers", year),
        }


    kpis = get_global_kpis(selected_year)
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("💰 Total Sales",
                f"${kpis['total_sales'][0].get('totalSales', 0):,.2f}" if kpis['total_sales'] else "N/A")
    col2.metric("💸 Total Profits",
                f"${kpis['total_profits'][0].get('totalProfit', 0):,.2f}" if kpis['total_profits'] else "N/A")
    col3.metric("🛒 Total Orders", kpis['total_orders'][0].get("Order ID", 0) if kpis['total_orders'] else "N/A")
    col4.metric("📦 Total Quantity",
                kpis['total_quantity'][0].get("totalQuantity", 0) if kpis['total_quantity'] else "N/A")
    col5.metric("👥 Total Clients", kpis['total_clients'][0].get("Customers ID", 0) if kpis['total_clients'] else "N/A")
    col6.metric("📈 Avg Orders/Customer",
                f"{kpis['avg_orders_by_customers'][0].get('averageOrdersPerCustomer', 0):.2f}" if kpis[
                    'avg_orders_by_customers'] else "N/A")

elif page == "Customers":
    st.title("👥 Customers Dashboard")


    @st.cache_data(ttl=600, show_spinner=False)
    def get_customer_data(year):
        return {
            "revenue_by_customer": fetch_data("revenue_by_customer", year),
            "total_orders_per_customer": fetch_data("total_orders_per_customer", year),
            "quantity_per_customer": fetch_data("quantity_per_customer", year),
            "retention_by_customers": fetch_data("retention_by_customers", year),
        }


    customer_data = get_customer_data(selected_year)

    render_chart(customer_data["revenue_by_customer"], "_id", "totalSales", "Revenue by Customer")
    render_chart(customer_data["total_orders_per_customer"], "_id", "totalOrders", "Total Orders by Customer")
    render_chart(customer_data["quantity_per_customer"], "_id", "totalQuantity", "Quantity per Customer")
    render_chart(customer_data["retention_by_customers"], "_id", "retentionPeriodDays", "Retention by Customers",
                 chart_type="scatter")

elif page == "Products":
    st.title("🛍️ Products Dashboard")


    @st.cache_data(ttl=600, show_spinner=False)
    def get_product_data(year):
        return {
            "revenue_by_category": fetch_data("revenue_by_category", year),
            "total_orders_by_category": fetch_data("total_orders_by_category", year),
            "quantity_by_category": fetch_data("quantity_by_category", year),
        }


    product_data = get_product_data(selected_year)

    render_chart(product_data["revenue_by_category"], "_id", "totalSales", "Revenue by Category")
    render_chart(product_data["total_orders_by_category"], "_id", "totalOrders", "Total Orders by Category")
    render_chart(product_data["quantity_by_category"], "_id", "totalQuantity", "Quantity by Category")
