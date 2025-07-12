# sales with state, product category, city (with dropdown)
# monthly trends
# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback

# dash.register_page(__name__, path="/sales")

# # Load the dataset
# df = pd.read_csv("data/final_olist_dataset.csv", parse_dates=['order_purchase_timestamp'])

# # Clean and prepare
# df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

# # Dropdown options
# dimension_options = {
#     'customer_state': 'State',
#     'customer_city': 'City',
#     'product_category_name_english': 'Product Category'
# }

# layout = html.Div([
#     html.H3("Sales Analysis", className="mb-4", style={"textAlign": "center", "color": "#2c3e50"}),

#     html.Div([
#         html.Label("Select Dimension:", className="mb-2"),
#         dcc.Dropdown(
#             id='sales-dimension-dropdown',
#             options=[{"label": v, "value": k} for k, v in dimension_options.items()],
#             value='customer_state',
#             clearable=False,
#             style={"width": "300px"}
#         )
#     ], style={"marginBottom": "30px"}),

#     dcc.Graph(id='sales-bar-graph'),
#     html.Hr(),
#     dcc.Graph(id='monthly-sales-trend')
# ])

# @callback(
#     Output('sales-bar-graph', 'figure'),
#     Input('sales-dimension-dropdown', 'value')
# )
# def update_sales_bar(dimension):
#     sales_summary = df.groupby(dimension)['price'].sum().sort_values(ascending=False).head(15).reset_index()
#     fig = px.bar(
#         sales_summary,
#         x=dimension,
#         y='price',
#         title=f"Top 15 {dimension_options[dimension]}s by Total Sales",
#         labels={'price': 'Total Sales (₹)', dimension: dimension_options[dimension]},
#         template='plotly_white'
#     )
#     fig.update_layout(xaxis_tickangle=45)
#     return fig

# @callback(
#     Output('monthly-sales-trend', 'figure'),
#     Input('sales-dimension-dropdown', 'value')
# )
# def update_monthly_sales(_):
#     monthly = df.groupby('month')['price'].sum().reset_index()
#     fig = px.line(
#         monthly,
#         x='month',
#         y='price',
#         title="Monthly Sales Trend",
#         labels={'price': 'Total Sales (₹)', 'month': 'Month'},
#         markers=True,
#         template='plotly_white'
#     )
#     fig.update_layout(xaxis_tickangle=45)
#     return fig


import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/sales")

# Load the dataset
df = pd.read_csv("data/final_olist_dataset.csv", parse_dates=['order_purchase_timestamp'])
df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

# Dropdown options
dimension_options = {
    'customer_state': 'State',
    'customer_city': 'City',
    'product_category_name_english': 'Product Category'
}

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("Sales Analysis", className="text-center mb-4", style={"color": "#2c3e50"})
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("Select Dimension:", className="mb-2 fw-bold"),
            dcc.Dropdown(
                id='sales-dimension-dropdown',
                options=[{"label": v, "value": k} for k, v in dimension_options.items()],
                value='customer_state',
                clearable=False,
                style={"width": "100%"}
            )
        ], width=4)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top 15 by Total Sales", className="fw-bold"),
                dbc.CardBody([
                    dcc.Graph(id='sales-bar-graph', config={'displayModeBar': True}, style={"height": "400px"})
                ])
            ])
        ], width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Sales Trend", className="fw-bold"),
                dbc.CardBody([
                    dcc.Graph(id='monthly-sales-trend', config={'displayModeBar': True}, style={"height": "400px"})
                ])
            ])
        ], width=12)
    ])
], fluid=True)


@callback(
    Output('sales-bar-graph', 'figure'),
    Input('sales-dimension-dropdown', 'value')
)
def update_sales_bar(dimension):
    sales_summary = df.groupby(dimension)['price'].sum().sort_values(ascending=False).head(15).reset_index()
    fig = px.bar(
        sales_summary,
        x=dimension,
        y='price',
        title=f"Top 15 {dimension_options[dimension]}s by Total Sales",
        labels={'price': 'Total Sales (₹)', dimension: dimension_options[dimension]},
        template='plotly_white'
    )
    fig.update_layout(xaxis_tickangle=45)
    return fig


@callback(
    Output('monthly-sales-trend', 'figure'),
    Input('sales-dimension-dropdown', 'value')
)
def update_monthly_sales(_):
    monthly = df.groupby('month')['price'].sum().reset_index()
    fig = px.line(
        monthly,
        x='month',
        y='price',
        title="Monthly Sales Trend",
        labels={'price': 'Total Sales (₹)', 'month': 'Month'},
        markers=True,
        template='plotly_white'
    )
    fig.update_layout(xaxis_tickangle=45)
    return fig
