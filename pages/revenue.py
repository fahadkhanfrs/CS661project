# # revenue by state (annual, quaterly, monthly)
# #revenue by product category
# # revenue by cities

# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc

# dash.register_page(__name__, path="/revenue-city")

# # Load data
# df = pd.read_csv("data/final_olist_dataset.csv", parse_dates=["order_purchase_timestamp"])

# # Add time columns
# df["year"] = df["order_purchase_timestamp"].dt.year
# df["quarter"] = df["order_purchase_timestamp"].dt.to_period("Q").astype(str)
# df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

# # Compute revenue
# df["revenue"] = df["price"] + df["freight_value"]

# # Layout
# layout = html.Div([
#     html.H3("Revenue Analysis", className="text-center text-primary mb-4"),

#     html.Div([
#         html.Label("Select Time Granularity:", className="fw-bold"),
#         dcc.Dropdown(
#             id="revenue-time-dropdown",
#             options=[
#                 {"label": "Monthly", "value": "month"},
#                 {"label": "Quarterly", "value": "quarter"},
#                 {"label": "Yearly", "value": "year"},
#             ],
#             value="month",
#             clearable=False,
#             style={"width": "300px"}
#         ),
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col(dcc.Graph(id="revenue-state-graph"), width=12),
#     ]),

#     dbc.Row([
#         dbc.Col(dcc.Graph(id="revenue-city-bar"), width=6),
#         dbc.Col(dcc.Graph(id="revenue-category-pie"), width=6),
#     ], className="mt-4"),

#     dbc.Row([
#         dbc.Col(dcc.Graph(id="sunburst-revenue"), width=12)
#     ], className="mt-4")
# ])

# # Revenue by state and time granularity
# @callback(
#     Output("revenue-state-graph", "figure"),
#     Input("revenue-time-dropdown", "value")
# )
# def update_state_revenue(time_col):
#     state_rev = df.groupby([time_col, "customer_state"])["revenue"].sum().reset_index()
#     fig = px.line(
#         state_rev,
#         x=time_col,
#         y="revenue",
#         color="customer_state",
#         title=f"Revenue by State ({time_col.capitalize()})",
#         labels={"revenue": "Revenue (₹)", time_col: time_col.capitalize()},
#         markers=True,
#         template="plotly_white"
#     )
#     fig.update_layout(xaxis_tickangle=45)
#     return fig

# # Revenue by top cities
# @callback(
#     Output("revenue-city-bar", "figure"),
#     Input("revenue-time-dropdown", "value")  # Dummy trigger
# )
# def update_city_revenue(_):
#     city_rev = df.groupby("customer_city")["revenue"].sum().sort_values(ascending=False).head(15).reset_index()
#     fig = px.bar(
#         city_rev,
#         x="customer_city",
#         y="revenue",
#         title="Top 15 Cities by Total Revenue",
#         labels={"revenue": "Revenue (₹)", "customer_city": "City"},
#         template="plotly_white",
#         color="customer_city"
#     )
#     fig.update_layout(showlegend=False, xaxis_tickangle=45)
#     return fig

# # Revenue by product category
# @callback(
#     Output("revenue-category-pie", "figure"),
#     Input("revenue-time-dropdown", "value")  # Dummy trigger
# )
# def update_category_revenue(_):
#     cat_rev = df.groupby("product_category_name_english")["revenue"].sum().sort_values(ascending=False).head(10).reset_index()
#     fig = px.pie(
#         cat_rev,
#         values="revenue",
#         names="product_category_name_english",
#         title="Top 10 Product Categories by Revenue",
#         hole=0.4,
#         template="plotly_white"
#     )
#     return fig

# # Sunburst Chart for revenue breakdown
# @callback(
#     Output("sunburst-revenue", "figure"),
#     Input("revenue-time-dropdown", "value")  # Dummy trigger
# )
# def update_sunburst(_):
#     sunburst_df = df.groupby(["customer_state", "customer_city", "product_category_name_english"])["revenue"].sum().reset_index()
#     fig = px.sunburst(
#         sunburst_df,
#         path=["customer_state", "customer_city", "product_category_name_english"],
#         values="revenue",
#         title="Revenue Breakdown: State → City → Category",
#         template="plotly_white"
#     )
#     return fig


import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/revenue-city")

# Load data
df = pd.read_csv("data/E-commerse.csv", parse_dates=["order_purchase_timestamp"])

# Preprocess
df["year"] = df["order_purchase_timestamp"].dt.year
df["quarter"] = df["order_purchase_timestamp"].dt.to_period("Q").astype(str)
df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
df["revenue"] = df["price"] + df["freight_value"]

# Layout
layout = html.Div([
    html.H3("Revenue Analysis", className="text-center text-primary mb-4"),

    html.Div([
        html.Label("Select Time Granularity:", className="fw-bold"),
        dcc.Dropdown(
            id="revenue-time-dropdown",
            options=[
                {"label": "Monthly", "value": "month"},
                {"label": "Quarterly", "value": "quarter"},
                {"label": "Yearly", "value": "year"},
            ],
            value="month",
            clearable=False,
            style={"width": "300px"}
        ),
    ], className="mb-4"),

    # Card: Revenue by State
    dbc.Card([
        dbc.CardHeader("Revenue by State Over Time"),
        dbc.CardBody([
            dcc.Graph(id="revenue-state-graph")
        ])
    ], className="mb-4 shadow"),

    # Card: Revenue by City
    dbc.Card([
        dbc.CardHeader("Top 15 Cities by Revenue"),
        dbc.CardBody([
            dcc.Graph(id="revenue-city-bar")
        ])
    ], className="mb-4 shadow"),

    # Card: Revenue by Product Category
    dbc.Card([
        dbc.CardHeader("Top 10 Product Categories by Revenue"),
        dbc.CardBody([
            dcc.Graph(id="revenue-category-pie")
        ])
    ], className="mb-4 shadow"),

    # Card: Sunburst Revenue Breakdown
    dbc.Card([
        dbc.CardHeader("Sunburst: State → City → Product Category"),
        dbc.CardBody([
            dcc.Graph(id="sunburst-revenue")
        ])
    ], className="mb-4 shadow")
])

# Callbacks
@callback(
    Output("revenue-state-graph", "figure"),
    Input("revenue-time-dropdown", "value")
)
def update_state_revenue(time_col):
    state_rev = df.groupby([time_col, "customer_state"])["revenue"].sum().reset_index()
    fig = px.line(
        state_rev,
        x=time_col,
        y="revenue",
        color="customer_state",
        title=f"Revenue by State ({time_col.capitalize()})",
        labels={"revenue": "Revenue (₹)", time_col: time_col.capitalize()},
        markers=True,
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=45)
    return fig

@callback(
    Output("revenue-city-bar", "figure"),
    Input("revenue-time-dropdown", "value")  # dummy trigger
)
def update_city_revenue(_):
    city_rev = df.groupby("customer_city")["revenue"].sum().sort_values(ascending=False).head(15).reset_index()
    fig = px.bar(
        city_rev,
        x="customer_city",
        y="revenue",
        title="Top 15 Cities by Total Revenue",
        labels={"revenue": "Revenue (₹)", "customer_city": "City"},
        template="plotly_white",
        color="customer_city"
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=45)
    return fig

@callback(
    Output("revenue-category-pie", "figure"),
    Input("revenue-time-dropdown", "value")
)
def update_category_revenue(_):
    cat_rev = df.groupby("product_category_name_english")["revenue"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.pie(
        cat_rev,
        values="revenue",
        names="product_category_name_english",
        title="Top Product Categories",
        hole=0.4,
        template="plotly_white"
    )
    return fig

@callback(
    Output("sunburst-revenue", "figure"),
    Input("revenue-time-dropdown", "value")
)
def update_sunburst(_):
    sunburst_df = df.groupby(["customer_state", "customer_city", "product_category_name_english"])["revenue"].sum().reset_index()
    fig = px.sunburst(
        sunburst_df,
        path=["customer_state", "customer_city", "product_category_name_english"],
        values="revenue",
        title="Revenue Breakdown by Region & Category",
        template="plotly_white"
    )
    return fig

