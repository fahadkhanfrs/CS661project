import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

dash.register_page(__name__, path="/")

layout = html.Div(
    style={"textAlign": "center"},
    children=[
        # html.Img(
        #     src="/assets/ecommerce_img.png",
        #     style={
        #         "background-color": "blue",
        #         "maxWidth": "50%",
        #         "height": "20%",
        #         "borderRadius": "12px",
        #         "marginBottom": "30px",
        #         "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
        #     }
        # ),
        html.H2("Welcome to the E-Commerce Sales Dashboard", style={"marginTop": "20px", "color": "#333"}),
        html.P(
            "Explore interactive insights into sales performance, delivery timelines, customer feedback, and much more.",
            style={"fontSize": "18px", "maxWidth": "70%", "margin": "auto", "color": "#555"}
        )
    ]
)
