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
page = st.sidebar.radio("Navigation", ("KPI Global", "Produits", "Clients"))

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

if page == "KPI Global":
    st.title("📊 Tableau de bord des indicateurs globaux")

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

    @st.cache_data(ttl=600, show_spinner=False)
    def fetch_average_per_ship_mode(year):
        return fetch_data("average_per_ship_mode", year)

    # Récupération des données
    kpis = get_global_kpis(selected_year)
    avg_ship_mode_data = fetch_average_per_ship_mode(selected_year)

    def afficher_carte_kpi(titre, valeur, description):
        st.markdown(
            f"""
            <div style="
                background-color: #2A2A2A; 
                padding: 20px; 
                border-radius: 10px; 
                text-align: center; 
                margin-bottom: 15px; 
                height: 170px; 
                display: flex; 
                flex-direction: column; 
                justify-content: space-between;">
                <h5 style="color: white; margin: 0; font-size: 18px;">{titre}</h5>
                <p style="font-size: 28px; font-weight: bold; color: white; margin: 5px 0;">{valeur}</p>
                <p style="font-size: 14px; color: #cccccc; margin: 5px 0;">{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Affichage des cartes KPI
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        afficher_carte_kpi(
            "💰 Ventes totales",
            f"{kpis['total_sales'][0].get('totalSales', 0):,.2f} €" if kpis['total_sales'] else "N/A",
            "Revenus totaux générés par les commandes."
        )
    with col2:
        afficher_carte_kpi(
            "💸 Profits totaux",
            f"{kpis['total_profits'][0].get('totalProfit', 0):,.2f} €" if kpis['total_profits'] else "N/A",
            "Profits nets après dépenses."
        )
    with col3:
        afficher_carte_kpi(
            "🛒 Commandes totales",
            f"{kpis['total_orders'][0].get('Order ID', 0):,}" if kpis['total_orders'] else "N/A",
            "Nombre total de commandes traitées."
        )

    col4, col5, col6 = st.columns(3, gap="large")
    with col4:
        afficher_carte_kpi(
            "📦 Quantité totale",
            f"{kpis['total_quantity'][0].get('totalQuantity', 0):,}" if kpis['total_quantity'] else "N/A",
            "Nombre total d'articles vendus."
        )
    with col5:
        afficher_carte_kpi(
            "👥 Clients uniques",
            f"{kpis['total_clients'][0].get('Customers ID', 0):,}" if kpis['total_clients'] else "N/A",
            "Nombre de clients ayant passé des commandes."
        )
    with col6:
        afficher_carte_kpi(
            "📈 Moyenne commandes/client",
            f"{kpis['avg_orders_by_customers'][0].get('averageOrdersPerCustomer', 0):.2f}" if kpis['avg_orders_by_customers'] else "N/A",
            "Nombre moyen de commandes par client."
        )

    # Affichage du graphique "Temps moyen par mode de livraison"
    st.subheader("⏱️ Temps moyen de livraison par mode de livraison")
    if avg_ship_mode_data:
        df_ship_mode = pd.DataFrame(avg_ship_mode_data)
        fig = px.bar(
            df_ship_mode,
            x="_id",
            y="AverageDaysDifference",
            title="Temps moyen de livraison par mode de livraison",
            labels={"_id": "Mode de livraison", "AverageDaysDifference": "Temps moyen (jours)"},
            color="AverageDaysDifference",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Aucune donnée disponible pour le temps moyen par mode de livraison.")



elif page == "Produits":
    st.title("🛍️ Tableau de bord des produits ")

    product_data = [
        {"data": fetch_data("revenue_by_category", selected_year), "x": "Category", "y": "totalSales", "chart_type": "bar"},
        {"data": fetch_data("total_orders_by_category", selected_year), "x": "Category", "y": "totalOrders", "chart_type": "bar"},
        {"data": fetch_data("quantity_by_category", selected_year), "x": "Category", "y": "totalQuantity", "chart_type": "doughnut"},  # Modifié ici pour un diagramme en anneau
    ]
    product_charts = {
        "titles": ["Revenus par catégories", "Nombres de commandes par catégories", "Nombres de produits vendus par catégories"],
    }

    def render_chart(data, x_col, y_col, title, chart_type="bar"):
        if data:
            df = pd.DataFrame(data)
            if chart_type == "bar":
                fig = px.bar(df, x=x_col, y=y_col, title=title, color=y_col)
            elif chart_type == "doughnut":
                # Diagramme en anneau pour le 3ème graphique
                fig = px.pie(df, names=x_col, values=y_col, title=title, hole=0.4)
                fig.update_traces(textinfo="percent+label")  # Affiche les pourcentages et les étiquettes
            else:
                st.warning(f"Type de graphique '{chart_type}' non pris en charge.")
                return
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Aucune donnée disponible pour {title}.")

    # Navigation entre les graphiques
    display_chart_with_navigation(product_data, product_charts, "products")


elif page == "Clients":
    st.title("📊 Tableau de bord des segments ")

    # Préparation des données
    segment_data = [
        {"data": fetch_data("revenue_by_segment", selected_year), "x": "Segment", "y": "totalRevenue",
         "chart_type": "bar"},
        {"data": fetch_data("total_orders_by_segment", selected_year), "x": "Segment", "y": "TotalOrders",
         "chart_type": "doughnut"},
        {"data": fetch_data("category_by_segment", selected_year), "x": "Segment", "y": "TopCategory",
         "chart_type": "cards"},  # Spécifie que ce sera affiché avec des cards
    ]
    segment_charts = {
        "titles": ["Revenue by Segment", "Total Orders by Segment", "Top Categories by Segment"],
    }

    def render_chart(data, x_col, y_col, title, chart_type="bar"):
        if data:
            df = pd.DataFrame(data)
            if chart_type == "bar":
                fig = px.bar(df, x=x_col, y=y_col, title=title, color=y_col)
            elif chart_type == "doughnut":
                if y_col:
                    # Doughnut pour les commandes totales (avec valeurs numériques)
                    fig = px.pie(df, names=x_col, values=y_col, title=title, hole=0.4)
                else:
                    # Doughnut pour les catégories par segment
                    if x_col in df.columns:
                        fig = px.pie(df, names=x_col, title=title, hole=0.4)
                        fig.update_traces(textinfo="percent+label")  # Affiche pourcentages et étiquettes
                    else:
                        st.warning(f"Clé '{x_col}' non trouvée dans les données.")
                        return
            elif chart_type == "horizontal_bar":
                # Graphique en barres horizontales pour les catégories
                if y_col in df.columns and x_col in df.columns:
                    fig = px.bar(df, x=y_col, y=x_col, orientation='h', title=title, color=x_col)
                else:
                    st.warning(f"Colonnes '{x_col}' ou '{y_col}' non trouvées dans les données.")
                    return
            elif chart_type == "cards":
                # Affichage des cards pour les catégories les plus achetées
                st.subheader(title)
                for _, row in df.iterrows():
                    afficher_carte_segment(row[x_col], row[y_col])
                return  # Pas besoin de graphique Plotly ici
            else:
                st.warning(f"Type de graphique '{chart_type}' non pris en charge.")
                return

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Aucune donnée disponible pour {title}.")

    def afficher_carte_segment(segment, category):
        """Affiche une carte avec le segment et sa catégorie la plus achetée."""
        st.markdown(
            f"""
            <div style="
                background-color: #2A2A2A; 
                padding: 20px; 
                border-radius: 10px; 
                text-align: center; 
                margin-bottom: 15px;
                color: white;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            ">
                <h4 style="margin: 0;">Segment : {segment}</h4>
                <p style="font-size: 20px; font-weight: bold; margin: 10px 0;">Catégorie la plus achetée : {category}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Navigation entre les graphiques
    display_chart_with_navigation(segment_data, segment_charts, "segments")




