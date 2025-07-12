import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/top-sellers")

# Load dataset
df = pd.read_csv("data/final_olist_dataset.csv")

# Seller summary
seller_summary = df.groupby(['seller_id', 'seller_state', 'product_category_name_english']).agg({
    'price': 'sum',
    'order_id': 'count'
}).reset_index()
seller_summary.rename(columns={'price': 'total_sales', 'order_id': 'orders'}, inplace=True)

# Dropdown options
dimension_options = {
    'seller_state': 'State',
    'product_category_name_english': 'Product Category'
}

# Layout
layout = html.Div([
    html.H3("Top Sellers Analysis", className="text-center text-primary mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Group Sellers By:", className="fw-bold"),
            dcc.Dropdown(
                id="seller-dimension-dropdown",
                options=[{"label": v, "value": k} for k, v in dimension_options.items()],
                value="seller_state",
                clearable=False,
                style={"width": "100%"}
            )
        ], width=6),
        dbc.Col([
            html.Label("Minimum Sales Filter (₹):", className="fw-bold"),
            dcc.Slider(
                id="min-sales-slider",
                min=0,
                max=200000,
                step=10000,
                value=50000,
                marks={i: f"{i//1000}K" for i in range(0, 210000, 50000)},
                tooltip={"placement": "bottom"}
            )
        ], width=6)
    ], className="mb-4"),

    # Cards stacked vertically
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top Sellers by Sales"),
                dbc.CardBody([
                    dcc.Graph(id="seller-bar-chart")
                ])
            ], className="mb-4")
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Treemap of Sales Contribution"),
                dbc.CardBody([
                    dcc.Graph(id="seller-treemap")
                ])
            ], className="mb-4")
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top Sellers by Order Volume"),
                dbc.CardBody([
                    dcc.Graph(id="seller-pie-chart")
                ])
            ])
        ])
    ])
])

@callback(
    Output("seller-bar-chart", "figure"),
    Output("seller-treemap", "figure"),
    Output("seller-pie-chart", "figure"),
    Input("seller-dimension-dropdown", "value"),
    Input("min-sales-slider", "value")
)
def update_seller_charts(dimension, min_sales):
    filtered = seller_summary[seller_summary["total_sales"] >= min_sales]

    # Bar chart
    top_groups = filtered.groupby(dimension)["total_sales"].sum().nlargest(10).reset_index()
    fig_bar = px.bar(
        top_groups,
        x=dimension,
        y="total_sales",
        title=f"Top 10 {dimension_options[dimension]}s by Sales (≥ ₹{min_sales:,})",
        labels={"total_sales": "Total Sales (₹)", dimension: dimension_options[dimension]},
        color=dimension,
        template="plotly_white"
    )
    fig_bar.update_layout(xaxis_tickangle=45)

    # Treemap
    fig_tree = px.treemap(
        filtered,
        path=[dimension, "seller_id"],
        values="total_sales",
        title="Sales Contribution Treemap",
        color="total_sales",
        color_continuous_scale="Blues",
        template="plotly_white"
    )

    # Pie chart
    top_sellers = filtered.groupby("seller_id")["orders"].sum().nlargest(10).reset_index()
    fig_pie = px.pie(
        top_sellers,
        names="seller_id",
        values="orders",
        title="Top 10 Sellers by Order Volume",
        hole=0.4,
        template="plotly_white"
    )

    return fig_bar, fig_tree, fig_pie
