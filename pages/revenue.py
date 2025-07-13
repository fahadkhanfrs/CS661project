# # revenue by state (annual, quaterly, monthly)
# #revenue by product category
# # revenue by cities

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import requests

# Register the page
dash.register_page(__name__, path="/revenue")

# Load and preprocess data
df = pd.read_csv("data/E-commerse.csv")

# Calculate revenue = price * order_item_id
df['revenue'] = df['price'] * df['order_item_id']

# Standardize state names to match GeoJSON
state_name_map = {
    "Andaman and Nicobar Islands": "Andaman & Nicobar Island",
    "Arunachal Pradesh": "Arunanchal Pradesh",
    "Chhattisgarh": "Chhattisgarh",
    "Delhi": "NCT of Delhi",
    "Jammu and Kashmir": "Jammu & Kashmir",
    "Orissa": "Odisha",
    "Pondicherry": "Puducherry",
    "Uttaranchal": "Uttarakhand"
}
df["customer_state"] = df["customer_state"].replace(state_name_map)

# Grouped data
state_grouped = df.groupby("customer_state")["revenue"].sum().reset_index(name="total_revenue")
category_grouped = df.groupby("product_category_name_english")["revenue"].sum().reset_index(name="total_revenue")

# Dropdown options
dropdown_options = sorted(df["customer_state"].dropna().unique())

# Layout
layout = html.Div([
    html.H3("Revenue Analysis (Based on Total Sales ₹)", className="mb-4 text-center text-success"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Choropleth Map: Revenue by State"),
            dbc.CardBody(dcc.Graph(id="revenue-map"))
        ]), width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Bar Chart: Revenue by Product Category"),
            dbc.CardBody(dcc.Graph(id="revenue-bar"))
        ]), width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Select State for Treemap"),
            dbc.CardBody([
                dcc.Dropdown(
                    id='revenue-state-dropdown',
                    options=[{"label": s, "value": s} for s in dropdown_options],
                    value=dropdown_options[0],
                    clearable=False,
                    style={"width": "300px"}
                )
            ])
        ]), width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Treemap: City-wise Revenue in Selected State"),
            dbc.CardBody(dcc.Graph(id="revenue-treemap"))
        ]), width=12)
    ])
])

# Choropleth Map
@callback(
    Output("revenue-map", "figure"),
    Input("revenue-state-dropdown", "value")
)
def update_revenue_choropleth(_):
    geojson_url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_states.geojson"
    india_states_geojson = requests.get(geojson_url).json()

    fig = px.choropleth(
        state_grouped,
        geojson=india_states_geojson,
        featureidkey="properties.ST_NM",
        locations="customer_state",
        color="total_revenue",
        color_continuous_scale="Greens",
        title="Total Revenue by State (₹)"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, template="plotly_white")
    return fig

# Bar Chart
@callback(
    Output("revenue-bar", "figure"),
    Input("revenue-state-dropdown", "value")
)
def update_revenue_bar(_):
    top_categories = category_grouped.sort_values("total_revenue", ascending=False).head(20)
    fig = px.bar(
        top_categories,
        x="product_category_name_english",
        y="total_revenue",
        labels={"product_category_name_english": "Product Category", "total_revenue": "Revenue (₹)"},
        title="Top 20 Product Categories by Revenue",
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=45)
    return fig

# Treemap
@callback(
    Output("revenue-treemap", "figure"),
    Input("revenue-state-dropdown", "value")
)
def update_revenue_treemap(selected_state):
    filtered = df[df["customer_state"] == selected_state]
    city_grouped = filtered.groupby(["customer_city", "product_category_name_english"])["revenue"].sum().reset_index()
    fig = px.treemap(
        city_grouped,
        path=["customer_city", "product_category_name_english"],
        values="revenue",
        title=f"City-wise Revenue in {selected_state}",
        template="plotly_white"
    )
    return fig


