# payment method unique
# payment method with city, product category (bar chart)

# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc

# dash.register_page(__name__, path="/payment-method")

# # Load the dataset
# df = pd.read_csv("data/final_olist_dataset.csv")

# # Clean if needed
# df.dropna(subset=["payment_type", "customer_city", "product_category_name_english", "payment_value"], inplace=True)

# # Mapping options for dropdown
# dimension_options = {
#     "customer_city": "City",
#     "product_category_name_english": "Product Category"
# }

# layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             html.H3("Payment Method Analysis", className="text-center mb-4", style={"color": "#2c3e50"})
#         ])
#     ]),

#     dbc.Row([
#         dbc.Col([
#             html.H5("Unique Payment Methods:", className="fw-bold"),
#             html.Ul([html.Li(method) for method in sorted(df["payment_type"].unique())])
#         ], width=6)
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col([
#             html.Label("Select Dimension:", className="mb-2 fw-bold"),
#             dcc.Dropdown(
#                 id="payment-dimension-dropdown",
#                 options=[{"label": v, "value": k} for k, v in dimension_options.items()],
#                 value="customer_city",
#                 clearable=False
#             )
#         ], width=4)
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardHeader("Payment Value by Payment Method & Selected Dimension", className="fw-bold"),
#                 dbc.CardBody([
#                     dcc.Graph(id="payment-bar-chart", style={"height": "400px"})
#                 ])
#             ])
#         ])
#     ])
# ], fluid=True)

# @callback(
#     Output("payment-bar-chart", "figure"),
#     Input("payment-dimension-dropdown", "value")
# )
# def update_payment_chart(dimension):
#     df_grouped = (
#         df.groupby(["payment_type", dimension])["payment_value"]
#         .sum()
#         .reset_index()
#         .sort_values("payment_value", ascending=False)
#     )

#     top_items = df_grouped[dimension].value_counts().head(15).index
#     df_filtered = df_grouped[df_grouped[dimension].isin(top_items)]

#     fig = px.bar(
#         df_filtered,
#         x="payment_value",
#         y=dimension,
#         color="payment_type",
#         orientation="h",
#         title=f"Payment Value by {dimension_options[dimension]} and Payment Method",
#         labels={"payment_value": "Total Payment (₹)", dimension: dimension_options[dimension]},
#         template="plotly_white"
#     )

#     fig.update_layout(yaxis=dict(categoryorder="total ascending"))
#     return fig

# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc

# # Register the page
# dash.register_page(__name__, path="/payment-method")

# # Load data
# df = pd.read_csv("data/final_olist_dataset.csv")

# # Dropdown dimension options
# dimension_options = {
#     "customer_city": "City",
#     "product_category_name_english": "Product Category"
# }

# # Layout
# layout = html.Div([
#     html.H3("Payment Method Analysis", className="mb-4 text-center text-primary"),

#     # Row for Cards
#     dbc.Row([
#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Total Transactions", className="text-center"),
#             dbc.CardBody(html.H5(id="total-transactions", className="card-title text-center"))
#         ]), width=3),

#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Total Payment Value (₹)", className="text-center"),
#             dbc.CardBody(html.H5(id="total-value", className="card-title text-center"))
#         ]), width=3),

#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Avg Payment per Transaction (₹)", className="text-center"),
#             dbc.CardBody(html.H5(id="avg-payment", className="card-title text-center"))
#         ]), width=3),

#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Most Used Payment Method", className="text-center"),
#             dbc.CardBody(html.H5(id="top-method", className="card-title text-center"))
#         ]), width=3),
#     ], className="mb-4"),

#     # Dropdown selector
#     html.Div([
#         html.Label("View By:", className="fw-bold"),
#         dcc.Dropdown(
#             id='payment-dimension-dropdown',
#             options=[{"label": v, "value": k} for k, v in dimension_options.items()],
#             value='customer_city',
#             clearable=False,
#             style={"width": "300px"}
#         )
#     ], className="mb-4"),

#     # Graph
#     dcc.Graph(id="payment-bar-chart")
# ])

# # Callback to update bar chart
# @callback(
#     Output("payment-bar-chart", "figure"),
#     Input("payment-dimension-dropdown", "value")
# )
# def update_bar_chart(dimension):
#     agg = df.groupby([dimension, "payment_type"])["payment_value"].sum().reset_index()
#     agg = agg.sort_values("payment_value", ascending=False)

#     fig = px.bar(
#         agg,
#         x=dimension,
#         y="payment_value",
#         color="payment_type",
#         barmode="group",
#         title=f"Payment Method Distribution by {dimension_options[dimension]}",
#         labels={"payment_value": "Total Payment (₹)", dimension: dimension_options[dimension]},
#         template="plotly_white"
#     )
#     fig.update_layout(xaxis_tickangle=45)
#     return fig

# # Callback to update stats
# @callback(
#     Output("total-transactions", "children"),
#     Output("total-value", "children"),
#     Output("avg-payment", "children"),
#     Output("top-method", "children"),
#     Input("payment-dimension-dropdown", "value")
# )
# def update_stats(_):
#     total_txn = len(df)
#     total_val = df["payment_value"].sum()
#     avg_val = df["payment_value"].mean()
#     top_method = df["payment_type"].value_counts().idxmax()

#     return (
#         f"{total_txn:,}",
#         f"₹{total_val:,.2f}",
#         f"₹{avg_val:,.2f}",
#         top_method.replace("_", " ").title()
#     )


# import dash
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc

# # Register the page
# dash.register_page(__name__, path="/payment-method")

# # Load data
# df = pd.read_csv("data/E-commerse.csv")

# # Dropdown options
# dimension_options = {
#     "customer_city": "City",
#     "product_category_name_english": "Product Category"
# }

# # Layout
# layout = html.Div([
#     html.H3("Payment Method Analysis", className="mb-4 text-center text-primary"),

#     # Row 1: Pie and Value Bar Chart as Cards
#     dbc.Row([
#         dbc.Col(
#             dbc.Card([
#                 dbc.CardHeader("Payment Method Distribution"),
#                 dbc.CardBody(dcc.Graph(id="payment-method-pie"))
#             ], className="h-100"),
#             width=6
#         ),
#         dbc.Col(
#             dbc.Card([
#                 dbc.CardHeader("Total Payment Value by Method"),
#                 dbc.CardBody(dcc.Graph(id="payment-value-bar"))
#             ], className="h-100"),
#             width=6
#         ),
#     ], className="mb-4"),

#     # Row 2: Dropdown inside a Card
#     dbc.Row([
#         dbc.Col(
#             dbc.Card([
#                 dbc.CardHeader("Select Dimension for Grouped View"),
#                 dbc.CardBody([
#                     html.Label("View By:", className="fw-bold mb-2"),
#                     dcc.Dropdown(
#                         id='payment-dimension-dropdown',
#                         options=[{"label": v, "value": k} for k, v in dimension_options.items()],
#                         value='customer_city',
#                         clearable=False,
#                         style={"width": "300px"}
#                     )
#                 ])
#             ]),
#             width=12
#         )
#     ], className="mb-4"),

#     # Row 3: Grouped Bar Chart in Card
#     dbc.Row([
#         dbc.Col(
#             dbc.Card([
#                 dbc.CardHeader(id="dimension-card-header", className="fw-bold"),
#                 dbc.CardBody(dcc.Graph(id="payment-dimension-bar"))
#             ]),
#             width=12
#         )
#     ])
# ])


# # Donut Chart of Payment Method Distribution
# @callback(
#     Output("payment-method-pie", "figure"),
#     Input("payment-dimension-dropdown", "value")
# )
# def update_pie_chart(_):
#     method_counts = df["payment_type"].value_counts().reset_index()
#     method_counts.columns = ["payment_type", "count"]

#     fig = px.pie(
#         method_counts,
#         values="count",
#         names="payment_type",
#         title="Distribution of Payment Methods",
#         hole=0.45,
#         template="plotly_white"
#     )
#     return fig


# # Bar Chart of Total Value by Payment Method
# @callback(
#     Output("payment-value-bar", "figure"),
#     Input("payment-dimension-dropdown", "value")
# )
# def update_value_bar_chart(_):
#     value_df = df.groupby("payment_type")["payment_value"].sum().reset_index()
#     fig = px.bar(
#         value_df,
#         x="payment_type",
#         y="payment_value",
#         title="Total Payment Value by Method",
#         labels={"payment_value": "Total Value (₹)", "payment_type": "Payment Method"},
#         template="plotly_white",
#         color="payment_type"
#     )
#     fig.update_layout(xaxis_tickangle=0)
#     return fig


# # Grouped Bar Chart by City or Product Category
# @callback(
#     Output("payment-dimension-bar", "figure"),
#     Output("dimension-card-header", "children"),
#     Input("payment-dimension-dropdown", "value")
# )
# def update_grouped_bar(dimension):
#     agg = df.groupby([dimension, "payment_type"])["payment_value"].sum().reset_index()
#     top_n = agg.groupby(dimension)["payment_value"].sum().nlargest(15).index.tolist()
#     filtered = agg[agg[dimension].isin(top_n)]

#     fig = px.bar(
#         filtered,
#         x=dimension,
#         y="payment_value",
#         color="payment_type",
#         barmode="group",
#         title=None,
#         labels={"payment_value": "Total Payment (₹)", dimension: dimension_options[dimension]},
#         template="plotly_white"
#     )
#     fig.update_layout(xaxis_tickangle=45)

#     card_header = f"Top 15 {dimension_options[dimension]}s by Payment Value (Grouped by Payment Method)"
#     return fig, card_header
# -----------------------------
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Register the page
dash.register_page(__name__, path="/payment") 

# Load data
df = pd.read_csv("data/E-commerse.csv")

# Fill missing values
df["product_category_name_english"] = df["product_category_name_english"].fillna("Unknown")

# Precompute grouped data
category_payment = df.groupby(["product_category_name_english", "payment_type"]).size().reset_index(name="count")
payment_type_counts = df["payment_type"].value_counts().reset_index()
payment_type_counts.columns = ["payment_type", "count"]

# Layout
layout = html.Div([
    html.H4("Payment Type Distribution per Product Category", className="mb-4 text-primary"),
    
    dcc.Graph(id="stacked-payment-bar"),

    html.Hr(),

    html.H5("Overall Payment Type Usage", className="mb-3 text-success"),
    dcc.Graph(id="payment-type-pie")
])

# Callback
@callback(
    Output("stacked-payment-bar", "figure"),
    Output("payment-type-pie", "figure"),
    Input("stacked-payment-bar", "id")  # dummy input to trigger once on load
)
def update_charts(_):
    # Stacked bar chart
    bar_fig = px.bar(
        category_payment,
        x="product_category_name_english",
        y="count",
        color="payment_type",
        title="Stacked Bar Chart: Payment Types by Product Category",
        labels={"count": "Number of Orders", "product_category_name_english": "Product Category"},
        barmode="stack"
    )
    bar_fig.update_layout(
        xaxis_tickangle=45,
        template="plotly_white",
        legend_title_text="Payment Type",
        margin=dict(l=20, r=20, t=60, b=120)
    )

    # Pie chart
    pie_fig = px.pie(
        payment_type_counts,
        values="count",
        names="payment_type",
        title="Overall Payment Type Usage (Percentage)",
        hole=0.3
    )
    pie_fig.update_traces(textinfo='percent+label')
    pie_fig.update_layout(template="plotly_white")

    return bar_fig, pie_fig

