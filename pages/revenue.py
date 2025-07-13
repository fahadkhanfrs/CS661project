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


# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc

# dash.register_page(__name__, path="/revenue-city")

# # Load data
# df = pd.read_csv("data/E-commerse.csv", parse_dates=["order_purchase_timestamp"])

# # Preprocess
# df["year"] = df["order_purchase_timestamp"].dt.year
# df["quarter"] = df["order_purchase_timestamp"].dt.to_period("Q").astype(str)
# df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
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

#     # Card: Revenue by State
#     dbc.Card([
#         dbc.CardHeader("Revenue by State Over Time"),
#         dbc.CardBody([
#             dcc.Graph(id="revenue-state-graph")
#         ])
#     ], className="mb-4 shadow"),

#     # Card: Revenue by City
#     dbc.Card([
#         dbc.CardHeader("Top 15 Cities by Revenue"),
#         dbc.CardBody([
#             dcc.Graph(id="revenue-city-bar")
#         ])
#     ], className="mb-4 shadow"),

#     # Card: Revenue by Product Category
#     dbc.Card([
#         dbc.CardHeader("Top 10 Product Categories by Revenue"),
#         dbc.CardBody([
#             dcc.Graph(id="revenue-category-pie")
#         ])
#     ], className="mb-4 shadow"),

#     # Card: Sunburst Revenue Breakdown
#     dbc.Card([
#         dbc.CardHeader("Sunburst: State → City → Product Category"),
#         dbc.CardBody([
#             dcc.Graph(id="sunburst-revenue")
#         ])
#     ], className="mb-4 shadow")
# ])

# # Callbacks
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

# @callback(
#     Output("revenue-city-bar", "figure"),
#     Input("revenue-time-dropdown", "value")  # dummy trigger
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

# @callback(
#     Output("revenue-category-pie", "figure"),
#     Input("revenue-time-dropdown", "value")
# )
# def update_category_revenue(_):
#     cat_rev = df.groupby("product_category_name_english")["revenue"].sum().sort_values(ascending=False).head(10).reset_index()
#     fig = px.pie(
#         cat_rev,
#         values="revenue",
#         names="product_category_name_english",
#         title="Top Product Categories",
#         hole=0.4,
#         template="plotly_white"
#     )
#     return fig

# @callback(
#     Output("sunburst-revenue", "figure"),
#     Input("revenue-time-dropdown", "value")
# )
# def update_sunburst(_):
#     sunburst_df = df.groupby(["customer_state", "customer_city", "product_category_name_english"])["revenue"].sum().reset_index()
#     fig = px.sunburst(
#         sunburst_df,
#         path=["customer_state", "customer_city", "product_category_name_english"],
#         values="revenue",
#         title="Revenue Breakdown by Region & Category",
#         template="plotly_white"
#     )
#     return fig
# ------------------------------
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


