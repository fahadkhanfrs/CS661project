# review score with product category

# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc

# dash.register_page(__name__, path="/review-score")

# # Load data
# df = pd.read_csv("data/final_olist_dataset.csv")

# # Drop NA reviews if any
# df = df.dropna(subset=["review_score", "product_category_name_english"])

# # Convert review_score to integer (sometimes it's float due to missing values)
# df["review_score"] = df["review_score"].astype(int)

# # Layout
# layout = html.Div([
#     html.H3("Customer Review Analysis", className="text-center text-primary mb-4"),

#     # Card 1: Distribution of Review Scores
#     dbc.Card([
#         dbc.CardHeader("Distribution of Review Scores"),
#         dbc.CardBody([
#             dcc.Graph(id="review-distribution", figure=px.histogram(
#                 df,
#                 x="review_score",
#                 nbins=5,
#                 title="Review Score Distribution",
#                 labels={"review_score": "Review Score"},
#                 template="plotly_white",
#                 color="review_score",
#                 color_discrete_sequence=px.colors.qualitative.Set2
#             ).update_layout(bargap=0.3))
#         ])
#     ], className="mb-4 shadow"),

#     # Card 2: Avg Review Score by Product Category
#     dbc.Card([
#         dbc.CardHeader("Average Review Score by Product Category"),
#         dbc.CardBody([
#             dcc.Graph(id="avg-review-by-category", figure=px.bar(
#                 df.groupby("product_category_name_english")["review_score"].mean()
#                   .sort_values(ascending=False)
#                   .head(15)
#                   .reset_index(),
#                 x="product_category_name_english",
#                 y="review_score",
#                 title="Top 15 Categories with Highest Avg Review Score",
#                 labels={"product_category_name_english": "Product Category", "review_score": "Average Score"},
#                 template="plotly_white",
#                 color="review_score",
#                 color_continuous_scale="Blues"
#             ).update_layout(xaxis_tickangle=45))
#         ])
#     ], className="mb-4 shadow"),

#     # Card 3: Review Score Pie Chart
#     dbc.Card([
#         dbc.CardHeader("Share of Each Review Score"),
#         dbc.CardBody([
#             dcc.Graph(id="review-pie", figure=px.pie(
#                 df["review_score"]
#                 .value_counts()
#                 .sort_index()
#                 .rename_axis("score")
#                 .reset_index(name="review_count"),
#                 values="review_count",
#                 names="score",
#                 hole=0.4,
#                 title="Proportion of Review Scores",
#                 template="plotly_white"
#             ))
#         ])
#     ], className="mb-4 shadow"),


#     # Card 4: Avg Review Score by Payment Type (Bonus insight)
#     dbc.Card([
#         dbc.CardHeader("Average Review Score by Payment Method"),
#         dbc.CardBody([
#             dcc.Graph(id="review-by-payment", figure=px.bar(
#                 df.groupby("payment_type")["review_score"].mean().reset_index(),
#                 x="payment_type",
#                 y="review_score",
#                 title="Average Review Score by Payment Type",
#                 labels={"review_score": "Average Score", "payment_type": "Payment Method"},
#                 template="plotly_white",
#                 color="review_score",
#                 color_continuous_scale="Oranges"
#             ))
#         ])
#     ], className="mb-4 shadow")
# ])


# import dash
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.express as px

# # Register page
# dash.register_page(__name__, path="/review-score")

# # Load data
# df = pd.read_csv("data/final_olist_dataset.csv")
# df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], format='mixed', errors='coerce')

# # Layout
# layout = html.Div([
#     html.H3("Review Score Analysis", className="text-center text-primary mb-4"),

#     dbc.Row([
#         dbc.Col(dcc.Graph(id="review-pie"), width=6),
#         dbc.Col(dcc.Graph(id="review-timeline"), width=6),
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col(dcc.Graph(id="review-bar-category"), width=12),
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col(dcc.Graph(id="review-box-category"), width=12),
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col(dcc.Graph(id="review-heatmap"), width=12),
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col(dcc.Graph(id="review-radar"), width=12),
#     ], className="mb-4"),
# ])

# # Donut chart of review scores
# @callback(
#     Output("review-pie", "figure"),
#     Input("review-pie", "id")
# )
# def update_pie(_):
#     pie_df = df["review_score"].value_counts().sort_index().reset_index()
#     pie_df.columns = ["score", "count"]
#     fig = px.pie(
#         pie_df,
#         values="count",
#         names="score",
#         hole=0.4,
#         title="Review Score Distribution",
#         template="plotly_white",
#         color_discrete_sequence=px.colors.qualitative.Set3
#     )
#     return fig

# # Timeline of average score
# @callback(
#     Output("review-timeline", "figure"),
#     Input("review-timeline", "id")
# )
# def update_timeline(_):
#     avg_score = df.groupby("review_creation_date")["review_score"].mean().reset_index()
#     fig = px.line(
#         avg_score,
#         x="review_creation_date",
#         y="review_score",
#         title="Average Review Score Over Time",
#         labels={"review_score": "Avg Score", "review_creation_date": "Date"},
#         markers=True,
#         template="plotly_white"
#     )
#     return fig

# # Stacked bar chart by category
# @callback(
#     Output("review-bar-category", "figure"),
#     Input("review-bar-category", "id")
# )
# def update_bar(_):
#     grouped = df.groupby(["product_category_name_english", "review_score"]).size().reset_index(name="count")
#     top_categories = grouped.groupby("product_category_name_english")["count"].sum().nlargest(10).index
#     grouped = grouped[grouped["product_category_name_english"].isin(top_categories)]
#     fig = px.bar(
#         grouped,
#         x="product_category_name_english",
#         y="count",
#         color="review_score",
#         title="Top Product Categories by Review Score",
#         labels={"count": "Review Count", "product_category_name_english": "Product Category"},
#         template="plotly_white"
#     )
#     return fig

# # Boxplot of scores by category
# @callback(
#     Output("review-box-category", "figure"),
#     Input("review-box-category", "id")
# )
# def update_box(_):
#     top = df["product_category_name_english"].value_counts().head(10).index
#     filtered = df[df["product_category_name_english"].isin(top)]
#     fig = px.box(
#         filtered,
#         x="product_category_name_english",
#         y="review_score",
#         title="Review Score Distribution by Top Categories",
#         points="all",
#         template="plotly_white"
#     )
#     fig.update_layout(xaxis_tickangle=45)
#     return fig

# # Heatmap of review scores by state
# @callback(
#     Output("review-heatmap", "figure"),
#     Input("review-heatmap", "id")
# )
# def update_heatmap(_):
#     heat_df = df.groupby(["customer_state", "review_score"]).size().reset_index(name="count")
#     fig = px.density_heatmap(
#         heat_df,
#         x="review_score",
#         y="customer_state",
#         z="count",
#         color_continuous_scale="Blues",
#         title="Review Score Frequency by Customer State",
#         template="plotly_white"
#     )
#     return fig

# # Radar chart of avg scores
# @callback(
#     Output("review-radar", "figure"),
#     Input("review-radar", "id")
# )
# def update_radar(_):
#     top = df["product_category_name_english"].value_counts().head(5).index
#     radar_df = df[df["product_category_name_english"].isin(top)].groupby("product_category_name_english")["review_score"].mean().reset_index()
#     fig = px.line_polar(
#         radar_df,
#         r="review_score",
#         theta="product_category_name_english",
#         line_close=True,
#         title="Avg Review Score of Top Product Categories",
#         template="plotly_white"
#     )
#     return fig


import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Register page
dash.register_page(__name__, path="/review-score")

# Load and preprocess data
df = pd.read_csv("data/E-commerse.csv")
df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], format='mixed', errors='coerce')
df["review_score"] = df["review_score"].astype("int")

# Card generator function
def create_card(title, graph_id):
    return dbc.Card([
        dbc.CardHeader(title, className="bg-primary text-white text-center fw-bold"),
        dbc.CardBody(dcc.Graph(id=graph_id))
    ], className="mb-4 shadow")

# Layout
layout = html.Div([
    html.H3("Review Score Analysis", className="text-center text-primary mb-4"),

    dbc.Row([
        dbc.Col(create_card("Review Score Distribution", "review-pie"), width=6),
        dbc.Col(create_card("Average Review Score Over Time", "review-timeline"), width=6),
    ]),

    dbc.Row([
        dbc.Col(create_card("Top Product Categories by Review Score", "review-bar-category"), width=12),
    ]),

    dbc.Row([
        dbc.Col(create_card("Review Score Distribution by Top Categories", "review-box-category"), width=12),
    ]),

    dbc.Row([
        dbc.Col(create_card("Review Score Frequency by Customer State", "review-heatmap"), width=12),
    ]),

    dbc.Row([
        dbc.Col(create_card("Radar View of Avg Review Scores (Top 10 Categories)", "review-radar"), width=12),
    ])
])

# Donut chart
@callback(
    Output("review-pie", "figure"),
    Input("review-pie", "id")
)
def update_pie(_):
    pie_df = df["review_score"].value_counts().sort_index().reset_index()
    pie_df.columns = ["score", "count"]
    fig = px.pie(
        pie_df,
        values="count",
        names="score",
        hole=0.4,
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

# Timeline line plot
@callback(
    Output("review-timeline", "figure"),
    Input("review-timeline", "id")
)
def update_timeline(_):
    avg_score = df.groupby("review_creation_date")["review_score"].mean().reset_index()
    fig = px.line(
        avg_score,
        x="review_creation_date",
        y="review_score",
        markers=True,
        template="plotly_white"
    )
    fig.update_layout(title="Average Review Score Over Time", xaxis_title="Date", yaxis_title="Avg Score")
    return fig

# Stacked bar chart
@callback(
    Output("review-bar-category", "figure"),
    Input("review-bar-category", "id")
)
def update_bar(_):
    grouped = df.groupby(["product_category_name_english", "review_score"]).size().reset_index(name="count")
    top_categories = grouped.groupby("product_category_name_english")["count"].sum().nlargest(10).index
    grouped = grouped[grouped["product_category_name_english"].isin(top_categories)]
    fig = px.bar(
        grouped,
        x="product_category_name_english",
        y="count",
        color="review_score",
        template="plotly_white"
    )
    fig.update_layout(title="Top Product Categories by Review Score", xaxis_title="Product Category", yaxis_title="Review Count")
    return fig

# Boxplot
@callback(
    Output("review-box-category", "figure"),
    Input("review-box-category", "id")
)
def update_box(_):
    top = df["product_category_name_english"].value_counts().head(10).index
    filtered = df[df["product_category_name_english"].isin(top)]
    fig = px.box(
        filtered,
        x="product_category_name_english",
        y="review_score",
        points="all",
        template="plotly_white",
        color="product_category_name_english",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_layout(title="Review Score Distribution by Top Categories", xaxis_tickangle=45)
    return fig

# Heatmap
@callback(
    Output("review-heatmap", "figure"),
    Input("review-heatmap", "id")
)
def update_heatmap(_):
    heat_df = df.groupby(["customer_state", "review_score"]).size().reset_index(name="count")
    fig = px.density_heatmap(
        heat_df,
        x="review_score",
        y="customer_state",
        z="count",
        color_continuous_scale="Blues",
        template="plotly_white"
    )
    fig.update_layout(title="Review Score Frequency by Customer State")
    return fig

# Radar plot with top 10 categories
@callback(
    Output("review-radar", "figure"),
    Input("review-radar", "id")
)
def update_radar(_):
    top = df["product_category_name_english"].value_counts().head(10).index
    radar_df = df[df["product_category_name_english"].isin(top)].groupby("product_category_name_english")["review_score"].mean().reset_index()
    fig = px.line_polar(
        radar_df,
        r="review_score",
        theta="product_category_name_english",
        line_close=True,
        template="plotly",
        color_discrete_sequence=["#3B82F6"]
    )
    fig.update_layout(title="Radar View of Avg Review Scores (Top 10 Categories)")
    return fig
