 
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Chargement et préparation des données
url = "https://raw.githubusercontent.com/OusmanHamit/datasets/refs/heads/main/L3_Project.csv"
df = pd.read_csv(url)
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d/%m/%Y")
df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

# Fonction de calcul des KPI
def get_kpi(data):
    total_sales = round(data["Sales"].sum(), 2)
    total_orders = data["Order ID"].nunique()
    avg_order_value = round(total_sales / total_orders, 2)
    total_regions = data["Region"].nunique()
    return total_sales, total_orders, avg_order_value, total_regions

# Calcul des KPI
total_sales, total_orders, avg_order_value, total_regions = get_kpi(df)

# Composants Dash pour afficher les KPI
kpi_cards = dbc.Row([
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H5("Chiffre d'affaires", className="card-title"),
        html.P(f"${total_sales:,}", className="card-text")
    ])), width=3),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H5("Total Commandes", className="card-title"),
        html.P(f"{total_orders}", className="card-text")
    ])), width=3),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H5("Panier moyen", className="card-title"),
        html.P(f"${avg_order_value}", className="card-text")
    ])), width=3),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H5("Nombre de régions", className="card-title"),
        html.P(f"{total_regions}", className="card-text")
    ])), width=3),
], className="mb-4")

# Évolution mensuelle des ventes par région
def monthly_sales_by_region(data):
    monthly = data.groupby(["YearMonth", "Region"])["Sales"].sum().reset_index()
    fig = px.line(monthly, x="YearMonth", y="Sales", color="Region", markers=True,
                  title="Évolution mensuelle des ventes par région",
                  labels={"YearMonth": "Mois", "Sales": "Ventes ($)", "Region": "Région"},
                  height=500)
    fig.update_xaxes(type="category")
    return fig

# Top 20 États avec le plus de ventes
def top_20_states_plot(data):
    state_sales = data.groupby("State")["Sales"].sum().sort_values(ascending=False).head(20).reset_index()
    fig = px.bar(state_sales, x="Sales", y="State", orientation="h",
                 title="Top 20 États par ventes",
                 labels={"Sales": "Ventes ($)", "State": "État"},
                 height=500)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig

# Top 10 villes avec le plus de ventes
def top_10_cities_plot(data):
    city_sales = data.groupby("City")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(city_sales, x="City", y="Sales",
                 title="Top 10 villes par ventes",
                 labels={"Sales": "Ventes ($)", "City": "Ville"},
                 height=400)
    return fig

# Ventes par région et par ville (heatmap)
def region_city_heatmap(data):
    pivot = data.pivot_table(index="Region", columns="City", values="Sales", aggfunc="sum", fill_value=0)
    fig = px.imshow(pivot,
                    labels=dict(x="Ville", y="Région", color="Ventes ($)"),
                    title="Ventes par région et par ville",
                    aspect="auto", height=500)
    return fig

# Catégories de produits par région (filtrable)
def category_by_region_plot(data, selected_region):
    filtered = data[data["Region"] == selected_region]
    category_sales = filtered.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    fig = px.bar(category_sales, x="Category", y="Sales",
                 title=f"Catégories de produits vendues dans la région {selected_region}",
                 labels={"Sales": "Ventes ($)", "Category": "Catégorie"},
                 height=400)
    return fig

# Top 10 sous-catégories de produits tous États confondus
def top_subcategories_plot(data):
    subcat_sales = data.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(10)
    fig = px.bar(subcat_sales, x="Sub-Category", y="Sales",
                 title="Top 10 sous-catégories les plus vendues",
                 labels={"Sales": "Ventes ($)", "Sub-Category": "Sous-catégorie"},
                 height=400)
    return fig

# Montant moyen des ventes par combinaison Segment x Catégorie
def avg_sales_segment_category_plot(data):
    pivot = data.pivot_table(index="Segment", columns="Category", values="Sales", aggfunc="mean", fill_value=0)
    fig = px.imshow(pivot,
                    text_auto=".2f",
                    labels=dict(x="Catégorie", y="Segment", color="Montant moyen ($)"),
                    title="Montant moyen des ventes par segment et catégorie",
                    height=400)
    return fig

# Composant de filtre par période
date_filter = dbc.Row([
    dbc.Col([
        html.Label("Filtrer par période :"),
        dcc.DatePickerRange(
            id="date-range",
            start_date=df["Order Date"].min(),
            end_date=df["Order Date"].max(),
            display_format="DD/MM/YYYY"
        )
    ], width=6)
], className="mb-4")

# Composant de filtre par région
region_filter = dbc.Row([
    dbc.Col(html.Label("Choisir une région :"), width=3),
    dbc.Col(
        dcc.Dropdown(
            id="region-dropdown",
            options=[{"label": r, "value": r} for r in sorted(df["Region"].unique())],
            value=df["Region"].unique()[0],
            clearable=False
        ), width=6
    )
], className="mb-4")

# Initialisation de l'application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Tableau de bord commercial - Aïcha Mbaye"

# Définition de la structure visuelle
app.layout = dbc.Container([
    html.H2("Tableau de bord commercial", className="text-center mt-4 mb-4"),
    
    kpi_cards,  # Affichage des indicateurs clés

    date_filter,
    dcc.Graph(id="monthly-sales-by-region"),

    region_filter,
    dcc.Graph(id="category-by-region"),

    dcc.Graph(figure=top_subcategories_plot(df)),
    dcc.Graph(figure=avg_sales_segment_category_plot(df)),
    dcc.Graph(figure=top_20_states_plot(df)),
    dcc.Graph(figure=top_10_cities_plot(df)),
    dcc.Graph(figure=region_city_heatmap(df))
], fluid=True)



# Callback pour mettre à jour le graphique des ventes mensuelles selon la plage de dates
@app.callback(
    Output("monthly-sales-by-region", "figure"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_monthly_sales(start_date, end_date):
    filtered_df = df[(df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)]
    return monthly_sales_by_region(filtered_df)

# Callback pour mettre à jour le graphique des catégories selon la région sélectionnée
@app.callback(
    Output("category-by-region", "figure"),
    Input("region-dropdown", "value")
)
def update_category_plot(region):
    return category_by_region_plot(df, region)

# Lancement du serveur local
if __name__ == "__main__":
    app.run(debug=True)
