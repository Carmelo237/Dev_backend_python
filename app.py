import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# Base API URL
API_URL = "http://localhost:8000"

# Set Streamlit Page Config
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Title
st.title("📊 E-commerce KPI Dashboard")

# Sidebar for Navigation
menu = st.sidebar.selectbox(
    "Select a KPI",
    [
        "Orders with Details",
        "Total Sales",
        "Total Profits",
        "Total Orders",
        "Average Sales per Order",
        "Total Quantity",
        "Total Clients",
        "Orders by Customers",
        "Average Orders per Customer",
        "Retention by Customers",
        "Quantity per Product",
        "Total Orders per Product",
        "Revenue by Product"
    ]
)

def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=60)  # Increased timeout to 60 seconds
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error(f"Error: Request to {endpoint} timed out.")
    except requests.exceptions.ConnectionError:
        st.error(f"Error: Unable to connect to FastAPI server at {API_URL}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
    return []


# Dashboard UI Logic
with st.spinner("Fetching data..."):
    if menu == "Orders with Details":
        data = fetch_data("orders-with-details")
        df = pd.DataFrame(data)
        st.dataframe(df)

    elif menu == "Total Sales":
        data = fetch_data("total_sales")
        total_sales = data[0].get("totalSales", 0) if data else 0
        st.metric("💰 Total Sales", f"${total_sales:,.2f}")

    elif menu == "Total Profits":
        data = fetch_data("total_profits")
        total_profits = data[0].get("totalProfit", 0) if data else 0
        st.metric("💸 Total Profits", f"${total_profits:,.2f}")

    elif menu == "Total Orders":
        data = fetch_data("total_orders")
        total_orders = data[0].get("Order ID", 0)
        st.metric("🛒 Total Orders", total_orders)

    elif menu == "Average Sales per Order":
        data = fetch_data("average_sales")
        avg_sales = data[0].get("averageSalesPerOrder", 0)
        st.metric("📊 Average Sales per Order", f"${avg_sales:,.2f}")

    elif menu == "Total Quantity":
        data = fetch_data("total_quantity")
        total_quantity = data[0].get("totalQuantity", 0)
        st.metric("📦 Total Quantity Sold", total_quantity)

    elif menu == "Total Clients":
        data = fetch_data("total_client")
        total_clients = data[0].get("Customers ID", 0)
        st.metric("👥 Total Clients", total_clients)

    elif menu == "Orders by Customers":
        data = fetch_data("orders_by_customers")
        df = pd.DataFrame(data)
        if not df.empty:
            fig = px.bar(df, x="_id", y="orderCount", title="Orders by Customers")
            st.plotly_chart(fig, use_container_width=True)

    elif menu == "Average Orders per Customer":
        data = fetch_data("average_orders_by_customers")
        avg_orders = data[0].get("averageOrdersPerCustomer", 0)
        st.metric("🧑‍🤝‍🧑 Average Orders per Customer", avg_orders)

    elif menu == "Retention by Customers":
        data = fetch_data("retention_by_customers")
        df = pd.DataFrame(data)
        if not df.empty:
            fig = px.scatter(
                df,
                x="retentionPeriodDays",
                y="orderCount",
                size="orderCount",
                title="Customer Retention",
                labels={"retentionPeriodDays": "Retention Period (Days)", "orderCount": "Order Count"}
            )
            st.plotly_chart(fig, use_container_width=True)

    elif menu == "Quantity per Product":
        data = fetch_data("quantity_per_products")
        df = pd.DataFrame(data)
        if not df.empty:
            fig = px.bar(
                df, x="_id", y="quantity_per_products",
                title="Quantity Sold per Product"
            )
            st.plotly_chart(fig, use_container_width=True)

    elif menu == "Total Orders per Product":
        data = fetch_data("total_orders_per_products")
        df = pd.DataFrame(data)
        if not df.empty:
            fig = px.bar(
                df, x="_id", y="total_orders_per_products",
                title="Total Orders per Product"
            )
            st.plotly_chart(fig, use_container_width=True)

    elif menu == "Revenue by Product":
        data = fetch_data("revenus_by_products")
        df = pd.DataFrame(data)
        if not df.empty:
            fig = px.bar(
                df, x="_id", y="totalRevenue",
                title="Revenue by Product",
                color="totalRevenue"
            )
            st.plotly_chart(fig, use_container_width=True)
