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
page = st.sidebar.radio("Navigation", ("Global KPIs", "Customers", "Products", "Segments"))

# Function for chart navigation
def display_chart_with_navigation(data, charts, session_key):
    # Initialize an index in the session state if not already done
    if f"{session_key}_index" not in st.session_state:
        st.session_state[f"{session_key}_index"] = 0

    index = st.session_state[f"{session_key}_index"]

    # Display the title of the current chart
    st.title(charts["titles"][index])

    # Display the chart corresponding to the current index
    if data[index]["data"]:
        render_chart(
            data[index]["data"],
            data[index]["x"],
            data[index]["y"],
            charts["titles"][index],
            data[index].get("chart_type", "bar"),
        )
    else:
        st.warning(f"No data available for {charts['titles'][index]}.")

    # Add navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous", key=f"{session_key}_prev") and index > 0:
            st.session_state[f"{session_key}_index"] -= 1

    with col3:
        if st.button("➡️ Next", key=f"{session_key}_next") and index < len(data) - 1:
            st.session_state[f"{session_key}_index"] += 1

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
                f"{kpis['avg_orders_by_customers'][0].get('averageOrdersPerCustomer', 0):.2f}" if kpis[ 'avg_orders_by_customers'] else "N/A")

elif page == "Customers":
    st.title("👥 Customers Dashboard")

    customer_data = [
        {"data": fetch_data("revenue_by_customer", selected_year), "x": "Customer Name", "y": "totalSales", "chart_type": "bar"},
        {"data": fetch_data("total_orders_per_customer", selected_year), "x": "Customer Name", "y": "totalOrders", "chart_type": "bar"},
        {"data": fetch_data("quantity_per_customer", selected_year), "x": "Customer Name", "y": "totalQuantity", "chart_type": "bar"},
        {"data": fetch_data("retention_by_customers", selected_year), "x": "Customer Name", "y": "retentionPeriodDays", "chart_type": "scatter"},
    ]
    customer_charts = {
        "titles": ["Revenue by Customer", "Total Orders by Customer", "Quantity per Customer", "Retention by Customers"],
    }

    display_chart_with_navigation(customer_data, customer_charts, "customers")

elif page == "Products":
    st.title("🛍️ Products Dashboard")

    product_data = [
        {"data": fetch_data("revenue_by_category", selected_year), "x": "Category", "y": "totalSales", "chart_type": "bar"},
        {"data": fetch_data("total_orders_by_category", selected_year), "x": "Category", "y": "totalOrders", "chart_type": "bar"},
        {"data": fetch_data("quantity_by_category", selected_year), "x": "Category", "y": "totalQuantity", "chart_type": "bar"},
    ]
    product_charts = {
        "titles": ["Revenue by Category", "Total Orders by Category", "Quantity by Category"],
    }

    display_chart_with_navigation(product_data, product_charts, "products")

elif page == "Segments":
    st.title("📊 Segments Dashboard")

    segment_data = [
        {"data": fetch_data("revenue_by_segment", selected_year), "x": "Segment", "y": "totalRevenue", "chart_type": "bar"},
        {"data": fetch_data("total_orders_by_segment", selected_year), "x": "Segment", "y": "TotalOrders", "chart_type": "bar"},
        {"data": fetch_data("category_by_segment", selected_year), "x": "TopCategory", "y": "TotalOrders", "chart_type": "bar"},
    ]
    segment_charts = {
        "titles": ["Revenue by Segment", "Total Orders by Segment", "Top Categories by Segment"],
    }

    display_chart_with_navigation(segment_data, segment_charts, "segments")
