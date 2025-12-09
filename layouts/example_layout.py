from dash import html
from components.controls import (
    dataset_dropdown,
    view_type_radio,
    theme_toggle,
    chart_type_radio,
    axis_dropdown,
)
from utils.file_utils import list_available_datasets


MAIN_CONTENT_ID = "example-main-content"


def example_layout():
    dataset_options = list_available_datasets()
    default_value = "example_sales.csv"
    return html.Div(
        className="container",
        children=[
            html.H1("Example Dataset"),
            html.P(
                "This page uses the bundled example dataset. Switch views to see table, summary, or charts."
            ),
            html.Div(
                className="controls-row",
                children=[
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("Dataset"),
                            dataset_dropdown(
                                value=default_value,
                                options=dataset_options,
                            ),
                        ],
                    ),
                    html.Div(
                        className="control-card",
                        children=[html.Strong("View"), view_type_radio()],
                    ),
                    html.Div(
                        className="control-card",
                        children=[html.Strong("Theme"), theme_toggle()],
                    ),
                ],
            ),
            html.Div(
                className="controls-row",
                children=[
                    html.Div(
                        className="control-card",
                        children=[html.Strong("Chart Type"), chart_type_radio()],
                    ),
                    html.Div(
                        className="control-card",
                        children=[html.Strong("X Axis"), axis_dropdown("example-x-axis")],
                    ),
                    html.Div(
                        className="control-card",
                        children=[html.Strong("Y Axis"), axis_dropdown("example-y-axis")],
                    ),
                ],
            ),
            html.Hr(),
            html.Div(id=MAIN_CONTENT_ID, children="Loading example data..."),
        ],
    )
