import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# --- Load and preprocess your data ---
df = pd.read_csv("data/Sample - Superstore.csv")

# Clean column names (remove spaces, replace with underscores)
df.columns = [col.strip().replace(" ", "_") for col in df.columns]

# Remove rows with any null values
df = df.dropna()

# (Optional) Convert dates to datetime
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], errors='coerce')

# (Optional) Remove rows with invalid dates
df = df.dropna(subset=['Order_Date', 'Ship_Date'])

# Now df is ready for your dashboard!

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],suppress_callback_exceptions=True)

# Hamburger button (three dashes)
hamburger = html.Button(
    html.Span(className="navbar-toggler-icon"),
    className="navbar-toggler",
    id="open-offcanvas",
    style={"position": "fixed", "top": "1rem", "left": "1rem", "zIndex": 1050}
)

# Offcanvas sidebar
sidebar = dbc.Offcanvas(
    [
        html.H2("E-Commerce", className="display-6"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", id="nav-home", active="exact"),
                dbc.NavLink("Sales by Sub-Category", href="/sales-subcat", id="nav-sales-subcat", active="exact"),
                dbc.NavLink("Profit Over Time", href="/profit-time", id="nav-profit-time", active="exact"),
                dbc.NavLink("Profit by State", href="/profit-state", id="nav-profit-state", active="exact"),
                dbc.NavLink("Sales by State (Map)", href="/sales-map", id="nav-sales-map", active="exact"),
                dbc.NavLink("Sales Over Time", href="/sales-time", id="nav-sales-time", active="exact"),
                dbc.NavLink("Discount vs Sales (Bubble Plot)", href="/discount-bubble", id="nav-discount-bubble", active="exact"),
                dbc.NavLink("Category Treemap", href="/category-treemap", id="nav-category-treemap", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="offcanvas",
    is_open=False,
    style={"width": "18rem", "background-color": "#222", "color": "#fff"},
)

content = html.Div(id="page-content", style={"padding": "2rem 1rem"})

app.layout = html.Div([
    dcc.Location(id="url"),
    hamburger,
    sidebar,
    content
])

# Callback to open/close sidebar
@app.callback(
    Output("offcanvas", "is_open"),
    [Input("open-offcanvas", "n_clicks")] +
    [Input(f"nav-{page}", "n_clicks") for page in [
        "home", "sales-subcat", "profit-time", "profit-state", "sales-map", "sales-time", "discount-bubble", "category-treemap"
    ]],
    [State("offcanvas", "is_open")]
)
def toggle_offcanvas(open_click, *args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "open-offcanvas":
        return True
    elif button_id.startswith("nav-"):
        return False
    return False

# Callback for page content

# ...existing code...

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H1("E-Commerce Sales Dashboard"),
            html.P("Project introduction and overview.")
        ])
    elif pathname == "/sales-subcat":
        return html.Div([
            html.H2("Sales by Sub-Category"),
            html.Label("Select Category:"),
            dcc.Dropdown(
                id="filter-category",
                options=[{"label": c, "value": c} for c in sorted(df['Category'].unique())],
                value=df['Category'].unique()[0],
                clearable=False,
                style={"width": "300px"}
            ),
            dcc.Graph(id="sales-subcat-graph")
        ])
    elif pathname == "/profit-time":
        return html.Div([
            html.H2("Profit Over Time"),
            html.Label("Select Year:"),
            dcc.Dropdown(
                id="filter-year",
                options=[{"label": str(y), "value": y} for y in sorted(df['Order_Date'].dt.year.unique())],
                value=int(df['Order_Date'].dt.year.min()),
                clearable=False,
                style={"width": "200px"}
            ),
            dcc.Graph(id="profit-time-graph")
        ])
    elif pathname == "/profit-state":
        return html.Div([
            html.H2("Profit by State"),
            html.Label("Select Region:"),
            dcc.Dropdown(
                id="filter-region",
                options=[{"label": r, "value": r} for r in sorted(df['Region'].unique())],
                value=df['Region'].unique()[0],
                clearable=False,
                style={"width": "200px"}
            ),
            dcc.Graph(id="profit-state-graph")
        ])
    elif pathname == "/sales-map":
        return html.Div([
            html.H2("Sales by State (Map)"),
            html.Label("Select Year:"),
            dcc.Dropdown(
                id="filter-map-year",
                options=[{"label": str(y), "value": y} for y in sorted(df['Order_Date'].dt.year.unique())],
                value=int(df['Order_Date'].dt.year.min()),
                clearable=False,
                style={"width": "200px"}
            ),
            dcc.Graph(id="sales-map-graph")
        ])
    elif pathname == "/sales-time":
        return html.Div([
            html.H2("Sales Over Time"),
            html.Label("Select Category:"),
            dcc.Dropdown(
                id="filter-sales-category",
                options=[{"label": c, "value": c} for c in sorted(df['Category'].unique())],
                value=df['Category'].unique()[0],
                clearable=False,
                style={"width": "300px"}
            ),
            dcc.Graph(id="sales-time-graph")
        ])
    elif pathname == "/discount-bubble":
        return html.Div([
            html.H2("Discount vs Sales (Bubble Plot)"),
            html.Label("Select Segment:"),
            dcc.Dropdown(
                id="filter-segment",
                options=[{"label": s, "value": s} for s in sorted(df['Segment'].unique())],
                value=df['Segment'].unique()[0],
                clearable=False,
                style={"width": "200px"}
            ),
            dcc.Graph(id="discount-bubble-graph")
        ])
    elif pathname == "/category-treemap":
        return html.Div([
            html.H2("Category Treemap"),
            html.Label("Select Region:"),
            dcc.Dropdown(
                id="filter-treemap-region",
                options=[{"label": r, "value": r} for r in sorted(df['Region'].unique())],
                value=df['Region'].unique()[0],
                clearable=False,
                style={"width": "200px"}
            ),
            dcc.Graph(id="category-treemap-graph")
        ])
    else:
        return html.Div([
            html.H1("404: Not found"),
            html.P("The page you are looking for does not exist.")
        ])

# --- Callbacks for each contextual filter and plot ---

@app.callback(
    Output("sales-subcat-graph", "figure"),
    Input("filter-category", "value"),
    prevent_initial_call=True
)
def update_sales_subcat(selected_category):
    dff = df[df['Category'] == selected_category]
    sales_by_subcat = dff.groupby("Sub-Category")["Sales"].sum().reset_index()
    fig = px.bar(sales_by_subcat, x="Sub-Category", y="Sales", title=f"Sales by Sub-Category ({selected_category})")
    return fig

@app.callback(
    Output("profit-time-graph", "figure"),
    Input("filter-year", "value"),
    prevent_initial_call=True
)
def update_profit_time(selected_year):
    dff = df[df['Order_Date'].dt.year == selected_year]
    profit_by_month = dff.groupby(dff['Order_Date'].dt.to_period('M').astype(str))["Profit"].sum().reset_index()
    fig = px.line(profit_by_month, x="Order_Date", y="Profit", title=f"Profit Over Time ({selected_year})")
    fig.update_xaxes(type='category')
    return fig

@app.callback(
    Output("profit-state-graph", "figure"),
    Input("filter-region", "value"),
    prevent_initial_call=True
)
def update_profit_state(selected_region):
    dff = df[df['Region'] == selected_region]
    state_profit = dff.groupby("State")["Profit"].sum().reset_index()
    fig = px.bar(state_profit, x="State", y="Profit", title=f"Profit by State ({selected_region})")
    return fig

@app.callback(
    Output("sales-map-graph", "figure"),
    Input("filter-map-year", "value"),
    prevent_initial_call=True
)
def update_sales_map(selected_year):
    state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }
    dff = df[df['Order_Date'].dt.year == selected_year].copy()
    dff['State_Code'] = dff['State'].map(state_abbrev)
    state_sales = dff.groupby(["State", "State_Code"])["Sales"].sum().reset_index()
    fig = px.choropleth(
        state_sales,
        locations='State_Code',
        locationmode='USA-states',
        color='Sales',
        hover_name='State',
        scope='usa',
        color_continuous_scale='Blues',
        title=f'Sales by State (Choropleth Map, {selected_year})'
    )
    return fig

@app.callback(
    Output("sales-time-graph", "figure"),
    Input("filter-sales-category", "value"),
    prevent_initial_call=True
)
def update_sales_time(selected_category):
    dff = df[df['Category'] == selected_category]
    sales_by_date = dff.groupby("Order_Date")["Sales"].sum().reset_index()
    fig = px.line(sales_by_date, x="Order_Date", y="Sales", title=f"Sales Over Time ({selected_category})")
    return fig

@app.callback(
    Output("discount-bubble-graph", "figure"),
    Input("filter-segment", "value"),
    prevent_initial_call=True
)
def update_discount_bubble(selected_segment):
    dff = df[df['Segment'] == selected_segment]
    fig = px.scatter(
        dff,
        x='Discount',
        y='Sales',
        size=dff['Profit'].abs(),
        color='Profit',
        hover_data=['Sub-Category', 'State'],
        color_continuous_scale='RdYlGn',
        title=f'Discount vs Sales (Bubble Size = |Profit|, {selected_segment})'
    )
    return fig

@app.callback(
    Output("category-treemap-graph", "figure"),
    Input("filter-treemap-region", "value"),
    prevent_initial_call=True
)
def update_category_treemap(selected_region):
    dff = df[df['Region'] == selected_region]
    fig = px.treemap(
        dff,
        path=['Category'],
        values='Sales',
        color='Profit',
        color_continuous_scale='RdYlGn',
        title=f'Category-wise Sales and Profit ({selected_region})'
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)