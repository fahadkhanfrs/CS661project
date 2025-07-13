# monthly Orders by statesfor its cities
# monthly orders product category wise
# monthly Orders all states
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import requests

# Register the page
dash.register_page(__name__, path="/monthlyorders")

# Load dataset
df = pd.read_csv("data/E-commerse.csv")

# Preprocess date
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
df["year_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

# Dropdown options
states = sorted(df["customer_state"].dropna().unique())
categories = df["product_category_name_english"].dropna().unique()

layout = html.Div([
    html.H3("Monthly Order Trends", className="mb-4 text-center text-primary"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Orders for Top Product Categories"),
                dbc.CardBody(dcc.Graph(id="monthly-category-trend"))
            ])
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Orders per State"),
                dbc.CardBody(dcc.Graph(id="monthly-state-trend"))
            ])
        ])
    ])
])

@callback(
    Output("monthly-category-trend", "figure"),
    Input("monthly-category-trend", "id")
)
def plot_category_trends(_):
    # Top 6 product categories
    top_categories = df["product_category_name_english"].value_counts().nlargest(6).index
    filtered = df[df["product_category_name_english"].isin(top_categories)]
    grouped = (
        filtered.groupby(["year_month", "product_category_name_english"])["order_id"]
        .nunique()
        .reset_index(name="order_count")
    )
    fig = px.line(
        grouped,
        x="year_month",
        y="order_count",
        color="product_category_name_english",
        title="Monthly Order Trends of Top 6 Product Categories",
        markers=True,
        template="plotly_white"
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Number of Orders")
    return fig

@callback(
    Output("monthly-state-trend", "figure"),
    Input("monthly-state-trend", "id")
)
def plot_state_trends(_):
    state_monthly = (
        df.groupby(["year_month", "customer_state"])["order_id"]
        .nunique()
        .reset_index(name="order_count")
    )
    fig = px.line(
        state_monthly,
        x="year_month",
        y="order_count",
        color="customer_state",
        title="Monthly Orders Across All States",
        template="plotly_white",
        markers=True
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Number of Orders")
    return fig
